import os
from dotenv import load_dotenv

# MUST BE FIRST: Load environment variables before anything else happens
load_dotenv()

from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Now import modular routes
from app.api.report_router import router as report_router
from app.middleware.request_logger import log_requests

app = FastAPI(
    title="GitHub Organization Access Report API",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Simplified for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

app.include_router(report_router, prefix="/api/v1")