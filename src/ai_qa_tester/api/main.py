from fastapi import FastAPI

from ai_qa_tester.api.routers import impact, projects, runs, webhooks

app = FastAPI(title="AI QA Tester API", version="0.1.0")
app.include_router(projects.router)
app.include_router(runs.router)
app.include_router(impact.router)
app.include_router(webhooks.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api"}
