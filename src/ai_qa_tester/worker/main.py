from fastapi import FastAPI

from ai_qa_tester.worker.routers import analysis, scripts

app = FastAPI(title="AI QA Tester Worker", version="0.1.0")
app.include_router(scripts.router)
app.include_router(analysis.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "worker"}
