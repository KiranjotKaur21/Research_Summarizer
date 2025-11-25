from fastapi import FastAPI
from researchSummarizer.app.api.routes import router as api_router

app = FastAPI(title="Research Summarizer", version="0.1")

app.include_router(api_router, prefix="/api")



