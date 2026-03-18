"""Orchestrator – Coordinates the three agents in sequence.

Flow:
  1. Ingest the venue-rule PDF into Pinecone (RAG).
  2. Run the Logistical Parser on the chat log.
  3. Run the Financial Estimator using the chat log + logistics.
  4. Run the Conflict Resolution Supervisor with RAG retrieval to
     audit the plan and flag/fix rule violations.
"""

from __future__ import annotations

from backend.models import TripReport, BudgetOutput
from backend.rag.ingest import ingest_pdf
from backend.rag.retriever import get_retriever
from backend.agents.logistical import run_logistical_agent
from backend.agents.financial import run_financial_agent
from backend.agents.supervisor import run_supervisor_agent


async def orchestrate(
    chat_log: str,
    pdf_path: str | None = None,
) -> TripReport:
    report = TripReport(status="running")
    errors: list[str] = []

    # Step 1 – RAG ingestion
    retriever = None
    if pdf_path:
        try:
            ingest_pdf(pdf_path)
            retriever = get_retriever()
        except Exception as exc:
            errors.append(f"RAG ingestion failed: {exc}")

    # Step 2 – Logistical Parser
    try:
        logistics = await run_logistical_agent(chat_log)
        report.logistics = logistics
    except Exception as exc:
        errors.append(f"Logistical Parser failed: {exc}")
        report.errors = errors
        report.status = "partial_failure"
        return report

    # Step 3 – Financial Estimator
    try:
        budget = await run_financial_agent(chat_log, logistics)
        report.budget = budget
    except Exception as exc:
        errors.append(f"Financial Estimator failed: {exc}")

    # Step 4 – Conflict Resolution Supervisor
    try:
        budget_for_supervisor = report.budget or BudgetOutput()
        supervisor = await run_supervisor_agent(
            logistics, budget_for_supervisor, retriever
        )
        report.supervisor = supervisor
    except Exception as exc:
        errors.append(f"Conflict Supervisor failed: {exc}")

    report.errors = errors
    report.status = "complete" if not errors else "partial_failure"
    return report
