
from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.models.contracts import GeneratedScript, ScriptExecutionResult, TestRun
from ai_qa_tester.services.playwright_assets import PlaywrightAssetService


class PlaywrightRunner:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _resolve_command(self) -> list[str] | None:
        parts = shlex.split(self.settings.playwright_command)
        if not parts:
            return None
        binary = parts[0]
        if shutil.which(binary) is None:
            return None
        return parts

    def _build_run_dir(self, run: TestRun) -> Path:
        run_dir = Path(self.settings.playwright_work_root) / run.project_id / run.id
        tests_dir = run_dir / 'tests'
        tests_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def _write_support_files(self, run: TestRun, run_dir: Path) -> None:
        package_json = {
            'name': 'ai-qa-playwright-runner',
            'private': True,
            'devDependencies': {
                '@playwright/test': '^1.45.0'
            }
        }
        (run_dir / 'package.json').write_text(json.dumps(package_json, indent=2))
        support_dir = run_dir / 'support'
        support_dir.mkdir(parents=True, exist_ok=True)
        assets = PlaywrightAssetService().generate_ts_assets(run.project_id)
        for filename, content in assets.items():
            (support_dir / filename).write_text(content)
        (run_dir / 'playwright.config.ts').write_text(
            """
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  reporter: 'list',
  use: {
    baseURL: process.env.APP_BASE_URL || 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
});
""".strip()
        )

    def _script_filename(self, script: GeneratedScript) -> str:
        safe = ''.join(c if c.isalnum() else '_' for c in script.scenario_id)
        return f'{safe}.spec.ts'

    def execute(self, run: TestRun, scripts: list[GeneratedScript]) -> list[ScriptExecutionResult]:
        command = self._resolve_command()
        if command is None:
            return [
                ScriptExecutionResult(
                    id=f'exec_{uuid4().hex[:8]}',
                    project_id=run.project_id,
                    run_id=run.id,
                    script_id=script.id,
                    scenario_id=script.scenario_id,
                    status='blocked',
                    reason='Playwright command not available on PATH. Install Node.js and Playwright or switch execution backend to simulated.',
                )
                for script in scripts
            ]

        run_dir = self._build_run_dir(run)
        self._write_support_files(run, run_dir)

        script_map: dict[str, GeneratedScript] = {}
        for script in scripts:
            name = self._script_filename(script)
            (run_dir / 'tests' / name).write_text(script.content)
            script_map[name] = script

        env = os.environ.copy()
        env['APP_BASE_URL'] = self.settings.app_base_url
        proc = subprocess.run(
            command,
            cwd=str(run_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
        )

        status = 'passed' if proc.returncode == 0 else 'failed'
        evidence_root = run_dir / 'playwright-report'
        evidence_refs = [str(evidence_root)] if evidence_root.exists() else [str(run_dir)]
        executions: list[ScriptExecutionResult] = []
        for script in scripts:
            reason = 'Playwright script executed successfully.' if status == 'passed' else 'Playwright script failed. Inspect stdout/stderr and trace output.'
            executions.append(
                ScriptExecutionResult(
                    id=f'exec_{uuid4().hex[:8]}',
                    project_id=run.project_id,
                    run_id=run.id,
                    script_id=script.id,
                    scenario_id=script.scenario_id,
                    status=status,
                    reason=reason,
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    evidence_refs=evidence_refs,
                )
            )
        return executions
