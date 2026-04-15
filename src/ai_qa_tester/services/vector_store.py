from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from ai_qa_tester.common.config import get_settings


class LocalVectorBackend:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}")

    def read(self) -> dict[str, dict[str, Any]]:
        return json.loads(self.path.read_text() or "{}")

    def write(self, payload: dict[str, dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True))


class QdrantVectorBackend:
    def __init__(self, url: str, api_key: str | None, collection: str) -> None:
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models as qmodels
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("qdrant-client is required for qdrant vector backend") from exc
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection
        self.qmodels = qmodels
        collections = {c.name for c in self.client.get_collections().collections}
        if collection not in collections:
            self.client.create_collection(
                collection_name=collection,
                vectors_config=qmodels.VectorParams(size=256, distance=qmodels.Distance.COSINE),
            )


class VectorStoreService:
    def __init__(self) -> None:
        settings = get_settings()
        backend_name = (settings.vector_backend or "local").lower()
        self.backend_name = "local"
        self.local_backend: LocalVectorBackend | None = None
        self.qdrant_backend: QdrantVectorBackend | None = None
        if backend_name == "qdrant" and settings.qdrant_url:
            self.qdrant_backend = QdrantVectorBackend(settings.qdrant_url, settings.qdrant_api_key, settings.qdrant_collection)
            self.backend_name = "qdrant"
        else:
            self.local_backend = LocalVectorBackend(settings.vector_store_path)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [tok for tok in re.findall(r"[a-z0-9]+", text.lower()) if len(tok) > 1]

    def embed_text(self, text: str) -> dict[str, float]:
        counts = Counter(self._tokenize(text))
        total = sum(counts.values()) or 1
        return {token: count / total for token, count in counts.items()}

    def _to_dense_vector(self, sparse: dict[str, float], size: int = 256) -> list[float]:
        dense = [0.0] * size
        for token, value in sparse.items():
            dense[hash(token) % size] += value
        return dense

    def index_document(self, doc_id: str, text: str, metadata: dict[str, Any] | None = None) -> None:
        metadata = metadata or {}
        sparse = self.embed_text(text)
        if self.backend_name == "qdrant" and self.qdrant_backend is not None:
            point = self.qdrant_backend.qmodels.PointStruct(
                id=abs(hash(doc_id)) % (10**12),
                vector=self._to_dense_vector(sparse),
                payload={"doc_id": doc_id, "text": text, "metadata": metadata},
            )
            self.qdrant_backend.client.upsert(collection_name=self.qdrant_backend.collection, points=[point])
            return
        payload = self.local_backend.read() if self.local_backend else {}
        payload[doc_id] = {"text": text, "vector": sparse, "metadata": metadata}
        if self.local_backend:
            self.local_backend.write(payload)

    @staticmethod
    def _cosine_similarity(a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        dot = sum(a[t] * b[t] for t in common)
        norm_a = math.sqrt(sum(v * v for v in a.values())) or 1.0
        norm_b = math.sqrt(sum(v * v for v in b.values())) or 1.0
        return dot / (norm_a * norm_b)

    @staticmethod
    def _metadata_matches(metadata: dict[str, Any], filters: dict[str, Any] | None) -> bool:
        if not filters:
            return True
        for key, expected in filters.items():
            actual = metadata.get(key)
            if isinstance(expected, (list, tuple, set)):
                if actual not in expected:
                    return False
            else:
                if actual != expected:
                    return False
        return True

    def search_similar(self, query: str, top_k: int = 5, metadata_filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        sparse = self.embed_text(query)
        if self.backend_name == "qdrant" and self.qdrant_backend is not None:
            results = self.qdrant_backend.client.query_points(
                collection_name=self.qdrant_backend.collection,
                query=self._to_dense_vector(sparse),
                limit=max(top_k * 3, top_k),
                with_payload=True,
            )
            points = getattr(results, "points", results)
            output: list[dict[str, Any]] = []
            for point in points:
                payload = getattr(point, "payload", {}) or {}
                item = {
                    "doc_id": payload.get("doc_id"),
                    "score": round(float(getattr(point, "score", 0.0)), 4),
                    "text": payload.get("text", ""),
                    "metadata": payload.get("metadata", {}),
                }
                if self._metadata_matches(item["metadata"], metadata_filters):
                    output.append(item)
            return output[:top_k]
        payload = self.local_backend.read() if self.local_backend else {}
        scored = []
        for doc_id, item in payload.items():
            if not self._metadata_matches(item.get("metadata", {}), metadata_filters):
                continue
            score = self._cosine_similarity(sparse, item.get("vector", {}))
            if score > 0:
                scored.append({"doc_id": doc_id, "score": round(score, 4), **item})
        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def clear(self) -> None:
        if self.backend_name == "qdrant" and self.qdrant_backend is not None:
            self.qdrant_backend.client.delete_collection(self.qdrant_backend.collection)
            self.qdrant_backend.client.create_collection(
                collection_name=self.qdrant_backend.collection,
                vectors_config=self.qdrant_backend.qmodels.VectorParams(size=256, distance=self.qdrant_backend.qmodels.Distance.COSINE),
            )
            return
        if self.local_backend:
            self.local_backend.write({})


vector_store = VectorStoreService()
