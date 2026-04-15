from fastapi import FastAPI

from ai_qa_tester.intelligence.routers import associations, scenarios

app = FastAPI(title="AI QA Tester Intelligence", version="0.1.0")
app.include_router(associations.router)
app.include_router(scenarios.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "intelligence"}
