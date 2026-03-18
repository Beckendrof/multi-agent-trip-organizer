"""FastAPI application – serves the multi-agent trip concierge."""

from __future__ import annotations

import os
import uuid

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import UPLOAD_DIR
from backend.utils.parsers import read_text_file
from backend.agents.orchestrator import orchestrate

app = FastAPI(title="Multi-Agent Trip Concierge", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _save_upload(upload: UploadFile) -> str:
    ext = os.path.splitext(upload.filename or "file")[1]
    dest = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
    with open(dest, "wb") as f:
        f.write(upload.file.read())
    return dest


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/organize")
async def organize_trip(
    chat_log: UploadFile = File(...),
    venue_pdf: UploadFile | None = File(None),
):
    """Upload a chat log and optional venue-rule PDF, then run the full agent pipeline."""
    try:
        chat_path = _save_upload(chat_log)
        chat_text = read_text_file(chat_path)

        pdf_path = None
        if venue_pdf:
            pdf_path = _save_upload(venue_pdf)

        report = await orchestrate(chat_text, pdf_path)
        return JSONResponse(content=report.model_dump(), status_code=200)

    except Exception as exc:
        return JSONResponse(
            content={"status": "error", "message": str(exc)},
            status_code=500,
        )
