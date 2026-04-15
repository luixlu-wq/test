from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator, MutableMapping
from pathlib import Path
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
try:
    from sqlalchemy import Column, Integer, MetaData, String, Table, Text, create_engine, delete, select
    from sqlalchemy.engine import Engine
    SQLALCHEMY_AVAILABLE = True
except Exception:  # pragma: no cover
    Column = Integer = MetaData = String = Table = Text = create_engine = delete = select = Engine = None
    SQLALCHEMY_AVAILABLE = False

from ai_qa_tester.common.config import get_settings
from ai_qa_tester.models.contracts import Artifact, Association, GeneratedScript, JourneyArtifact, PageModel, Project, QueueJob, RunComparisonReport, ScriptExecutionResult, SelectorLearningReport, SelectorProfile, StabilityAnalyticsReport, TestRun, TestScenario, WorkItem

T = TypeVar("T")


def _default_json(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if hasattr(value, "isoformat"):
        return value.isoformat()
    raise TypeError(f"Object of type {type(value)!r} is not JSON serializable")


class SQLitePersistence:
    def __init__(self, path: str) -> None:
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS kv_store (namespace TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, PRIMARY KEY(namespace, key))"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS list_store (namespace TEXT NOT NULL, idx INTEGER NOT NULL, value TEXT NOT NULL, PRIMARY KEY(namespace, idx))"
            )
            conn.commit()

    def load_namespace(self, namespace: str) -> dict[str, Any]:
        with self._connect() as conn:
            rows = conn.execute("SELECT key, value FROM kv_store WHERE namespace = ?", (namespace,)).fetchall()
        return {row["key"]: json.loads(row["value"]) for row in rows}

    def save_item(self, namespace: str, key: str, value: Any) -> None:
        payload = json.dumps(value, default=_default_json)
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO kv_store(namespace, key, value) VALUES(?, ?, ?) ON CONFLICT(namespace, key) DO UPDATE SET value=excluded.value",
                (namespace, key, payload),
            )
            conn.commit()

    def delete_item(self, namespace: str, key: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM kv_store WHERE namespace = ? AND key = ?", (namespace, key))
            conn.commit()

    def clear_namespace(self, namespace: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM kv_store WHERE namespace = ?", (namespace,))
            conn.commit()

    def load_list(self, namespace: str) -> list[Any]:
        with self._connect() as conn:
            rows = conn.execute("SELECT value FROM list_store WHERE namespace = ? ORDER BY idx ASC", (namespace,)).fetchall()
        return [json.loads(row["value"]) for row in rows]

    def replace_list(self, namespace: str, values: list[Any]) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM list_store WHERE namespace = ?", (namespace,))
            conn.executemany(
                "INSERT INTO list_store(namespace, idx, value) VALUES(?, ?, ?)",
                [(namespace, idx, json.dumps(value, default=_default_json)) for idx, value in enumerate(values)],
            )
            conn.commit()


class SQLAlchemyPersistence:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self._sqlite_fallback: SQLitePersistence | None = None
        if not SQLALCHEMY_AVAILABLE:
            if database_url.startswith("sqlite:///"):
                self._sqlite_fallback = SQLitePersistence(database_url.removeprefix("sqlite:///"))
                return
            raise RuntimeError("SQLAlchemy backend requested but sqlalchemy is not installed")
        if database_url.startswith("sqlite:///"):
            db_path = database_url.removeprefix("sqlite:///")
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.engine: Engine = create_engine(database_url, future=True)
        self.metadata = MetaData()
        self.kv_store = Table(
            "kv_store",
            self.metadata,
            Column("namespace", String(255), primary_key=True),
            Column("key", String(255), primary_key=True),
            Column("value", Text, nullable=False),
        )
        self.list_store = Table(
            "list_store",
            self.metadata,
            Column("namespace", String(255), primary_key=True),
            Column("idx", Integer, primary_key=True),
            Column("value", Text, nullable=False),
        )
        self.metadata.create_all(self.engine)

    def load_namespace(self, namespace: str) -> dict[str, Any]:
        if self._sqlite_fallback is not None:
            return self._sqlite_fallback.load_namespace(namespace)
        with self.engine.begin() as conn:
            rows = conn.execute(select(self.kv_store.c.key, self.kv_store.c.value).where(self.kv_store.c.namespace == namespace)).all()
        return {row.key: json.loads(row.value) for row in rows}

    def save_item(self, namespace: str, key: str, value: Any) -> None:
        if self._sqlite_fallback is not None:
            self._sqlite_fallback.save_item(namespace, key, value)
            return
        payload = json.dumps(value, default=_default_json)
        stmt = self.kv_store.insert().values(namespace=namespace, key=key, value=payload)
        if self.engine.dialect.name == "sqlite":
            from sqlalchemy.dialects.sqlite import insert as sqlite_insert
            stmt = sqlite_insert(self.kv_store).values(namespace=namespace, key=key, value=payload).on_conflict_do_update(
                index_elements=[self.kv_store.c.namespace, self.kv_store.c.key],
                set_={"value": payload},
            )
        elif self.engine.dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import insert as pg_insert
            stmt = pg_insert(self.kv_store).values(namespace=namespace, key=key, value=payload).on_conflict_do_update(
                index_elements=[self.kv_store.c.namespace, self.kv_store.c.key],
                set_={"value": payload},
            )
        with self.engine.begin() as conn:
            conn.execute(stmt)

    def delete_item(self, namespace: str, key: str) -> None:
        if self._sqlite_fallback is not None:
            self._sqlite_fallback.delete_item(namespace, key)
            return
        with self.engine.begin() as conn:
            conn.execute(delete(self.kv_store).where(self.kv_store.c.namespace == namespace, self.kv_store.c.key == key))

    def clear_namespace(self, namespace: str) -> None:
        if self._sqlite_fallback is not None:
            self._sqlite_fallback.clear_namespace(namespace)
            return
        with self.engine.begin() as conn:
            conn.execute(delete(self.kv_store).where(self.kv_store.c.namespace == namespace))

    def load_list(self, namespace: str) -> list[Any]:
        if self._sqlite_fallback is not None:
            return self._sqlite_fallback.load_list(namespace)
        with self.engine.begin() as conn:
            rows = conn.execute(select(self.list_store.c.value).where(self.list_store.c.namespace == namespace).order_by(self.list_store.c.idx.asc())).all()
        return [json.loads(row.value) for row in rows]

    def replace_list(self, namespace: str, values: list[Any]) -> None:
        if self._sqlite_fallback is not None:
            self._sqlite_fallback.replace_list(namespace, values)
            return
        with self.engine.begin() as conn:
            conn.execute(delete(self.list_store).where(self.list_store.c.namespace == namespace))
            if values:
                conn.execute(
                    self.list_store.insert(),
                    [{"namespace": namespace, "idx": idx, "value": json.dumps(value, default=_default_json)} for idx, value in enumerate(values)],
                )


class PersistedMap(MutableMapping[str, T], Generic[T]):
    def __init__(self, persistence: SQLitePersistence | SQLAlchemyPersistence, namespace: str, model_cls: type[BaseModel] | None = None) -> None:
        self.persistence = persistence
        self.namespace = namespace
        self.model_cls = model_cls
        self._data: dict[str, T] = {}
        self._load()

    def _deserialize(self, value: Any) -> T:
        if self.model_cls is None:
            return value
        return self.model_cls.model_validate(value)

    def _serialize(self, value: T) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump(mode="json")
        return value

    def _load(self) -> None:
        raw = self.persistence.load_namespace(self.namespace)
        self._data = {key: self._deserialize(value) for key, value in raw.items()}

    def __getitem__(self, key: str) -> T:
        return self._data[key]

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key] = value
        self.persistence.save_item(self.namespace, key, self._serialize(value))

    def __delitem__(self, key: str) -> None:
        del self._data[key]
        self.persistence.delete_item(self.namespace, key)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def clear(self) -> None:  # type: ignore[override]
        self._data.clear()
        self.persistence.clear_namespace(self.namespace)

    def values(self):  # noqa: ANN201
        return self._data.values()

    def items(self):  # noqa: ANN201
        return self._data.items()

    def get(self, key: str, default: Any = None) -> T | Any:
        return self._data.get(key, default)


class PersistedList:
    def __init__(self, persistence: SQLitePersistence | SQLAlchemyPersistence, namespace: str) -> None:
        self.persistence = persistence
        self.namespace = namespace
        self._data: list[Any] = self.persistence.load_list(namespace)

    def _persist(self) -> None:
        self.persistence.replace_list(self.namespace, self._data)

    def append(self, value: Any) -> None:
        self._data.append(value)
        self._persist()

    def pop(self, index: int = -1) -> Any:
        value = self._data.pop(index)
        self._persist()
        return value

    def remove(self, value: Any) -> None:
        self._data.remove(value)
        self._persist()

    def clear(self) -> None:
        self._data.clear()
        self._persist()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self) -> int:
        return len(self._data)


def build_persistence() -> SQLitePersistence | SQLAlchemyPersistence:
    settings = get_settings()
    backend = (settings.repository_backend or "sqlalchemy").lower()
    if backend == "sqlite":
        return SQLitePersistence(settings.sqlite_path)
    return SQLAlchemyPersistence(settings.resolved_database_url)


class PersistentStore:
    def __init__(self) -> None:
        self.persistence = build_persistence()
        self.projects = PersistedMap[Project](self.persistence, "projects", Project)
        self.work_items = PersistedMap[WorkItem](self.persistence, "work_items", WorkItem)
        self.artifacts = PersistedMap[Artifact](self.persistence, "artifacts", Artifact)
        self.journeys = PersistedMap[JourneyArtifact](self.persistence, "journeys", JourneyArtifact)
        self.associations = PersistedMap[Association](self.persistence, "associations", Association)
        self.scenarios = PersistedMap[TestScenario](self.persistence, "scenarios", TestScenario)
        self.scripts = PersistedMap[GeneratedScript](self.persistence, "scripts", GeneratedScript)
        self.page_models = PersistedMap[PageModel](self.persistence, "page_models", PageModel)
        self.selector_profiles = PersistedMap[SelectorProfile](self.persistence, "selector_profiles", SelectorProfile)
        self.selector_learning_reports = PersistedMap[SelectorLearningReport](self.persistence, "selector_learning_reports", SelectorLearningReport)
        self.runs = PersistedMap[TestRun](self.persistence, "runs", TestRun)
        self.script_executions = PersistedMap[ScriptExecutionResult](self.persistence, "script_executions", ScriptExecutionResult)
        self.run_comparisons = PersistedMap[RunComparisonReport](self.persistence, "run_comparisons", RunComparisonReport)
        self.stability_reports = PersistedMap[StabilityAnalyticsReport](self.persistence, "stability_reports", StabilityAnalyticsReport)
        self.jobs = PersistedMap[QueueJob](self.persistence, "jobs", QueueJob)
        self.job_queue = PersistedList(self.persistence, "job_queue")
        self.sync_state = PersistedMap[dict[str, object]](self.persistence, "sync_state", None)

    def clear_all(self) -> None:
        for namespace in [
            self.projects,
            self.work_items,
            self.artifacts,
            self.journeys,
            self.associations,
            self.scenarios,
            self.scripts,
            self.page_models,
            self.selector_profiles,
            self.selector_learning_reports,
            self.runs,
            self.script_executions,
            self.run_comparisons,
            self.stability_reports,
            self.jobs,
            self.sync_state,
        ]:
            namespace.clear()
        self.job_queue.clear()


store = PersistentStore()
