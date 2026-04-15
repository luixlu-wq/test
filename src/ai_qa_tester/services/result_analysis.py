from __future__ import annotations

from ai_qa_tester.models.contracts import TestRun


class ResultAnalysisService:
    def analyze(self, run: TestRun) -> dict:
        failure_summary = None
        category = None
        if run.result_details:
            first = run.result_details[0]
            failure_summary = first['reason']
            category = 'product_defect'

        return {
            'run_id': run.id,
            'failure_summary': failure_summary,
            'likely_failure_category': category,
            'failed_scenarios': run.result_details,
            'recommended_next_actions': [
                'Review traceability coverage for scenarios that were executed.',
                'Persist this run as regression baseline evidence.',
            ] + ([
                'Create or update a bug ticket for failed scenarios.'
            ] if run.result_details else []),
            'confidence': 0.9,
        }
