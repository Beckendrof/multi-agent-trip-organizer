"""Agent 2 – The Financial Estimator

Parses the group's stated budget from the chat log, estimates costs for
the proposed activities, and flags whether the plan is within budget.
"""

import json

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from backend.config import OPENAI_API_KEY, LLM_MODEL
from backend.models import LogisticalOutput, BudgetOutput
from backend.utils.parsers import parse_llm_json

BUDGET_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a travel-budget estimation assistant.\n\n"
            "You receive:\n"
            "1. The original group-chat log (which may mention a budget).\n"
            "2. The extracted attendee list and proposed itinerary.\n\n"
            "Your job:\n"
            "- Identify any stated budget from the chat (or null if none mentioned).\n"
            "- Estimate realistic costs for each proposed activity and logistical need "
            "(camping fees, food, gas, gear, park entry, etc.).\n"
            "- Sum the estimates and compare against the stated budget.\n\n"
            "Return a JSON object with:\n"
            '  "stated_budget": float|null,\n'
            '  "estimated_items": [{{"category": str, "estimated_cost": float, "notes": str}}],\n'
            '  "total_estimated": float,\n'
            '  "within_budget": bool,\n'
            '  "budget_summary": str  // one-paragraph human-readable summary\n'
            "Output valid JSON only—no markdown fences, no commentary.",
        ),
        (
            "human",
            "Chat Log:\n{chat_log}\n\nExtracted Logistics:\n{logistics}",
        ),
    ]
)


async def run_financial_agent(
    chat_log: str,
    logistics: LogisticalOutput,
) -> BudgetOutput:
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )

    chain = BUDGET_PROMPT | llm
    raw = await chain.ainvoke(
        {
            "chat_log": chat_log,
            "logistics": json.dumps(logistics.model_dump(), indent=2),
        }
    )
    parsed = parse_llm_json(raw.content)

    return BudgetOutput(**parsed)
