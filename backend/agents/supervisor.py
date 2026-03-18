"""Agent 3 – The Conflict Resolution Supervisor

The core intelligence layer. Consumes outputs from Agents 1 & 2 and
queries the Pinecone vector store (RAG) to audit the proposed plan
against venue rules. Flags conflicts and auto-generates compliant
alternatives for each violation.
"""

import json

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseRetriever

from backend.config import OPENAI_API_KEY, LLM_MODEL
from backend.models import LogisticalOutput, BudgetOutput, SupervisorOutput
from backend.utils.parsers import parse_llm_json

SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict trip-compliance supervisor.\n\n"
            "You receive:\n"
            "1. A proposed itinerary with times and activities.\n"
            "2. A budget estimate.\n"
            "3. The OFFICIAL venue rules retrieved from a knowledge base.\n\n"
            "Your job:\n"
            "- Cross-reference every itinerary item against the venue rules.\n"
            "- For each conflict found, generate exactly 3 compliant alternatives.\n"
            "- Produce a final approved itinerary with conflicts removed and "
            "the best alternative substituted in.\n"
            "- Add a brief supervisor note summarising what was changed and why.\n\n"
            "Return a JSON object with:\n"
            '  "conflicts": [\n'
            "    {{\n"
            '      "activity": str,\n'
            '      "rule_violated": str,\n'
            '      "severity": "high"|"medium"|"low",\n'
            '      "alternatives": [str, str, str]\n'
            "    }}\n"
            "  ],\n"
            '  "approved_itinerary": [{{"time": str, "activity": str, "notes": str}}],\n'
            '  "supervisor_notes": str\n'
            "If no conflicts are found, return an empty conflicts list and the "
            "itinerary unchanged. "
            "Output valid JSON only—no markdown fences, no commentary.",
        ),
        (
            "human",
            "Proposed Itinerary:\n{itinerary}\n\n"
            "Budget Estimate:\n{budget}\n\n"
            "Venue Rules:\n{venue_rules}",
        ),
    ]
)


async def run_supervisor_agent(
    logistics: LogisticalOutput,
    budget: BudgetOutput,
    retriever: BaseRetriever | None = None,
) -> SupervisorOutput:
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )

    itinerary_text = json.dumps(
        [item.model_dump() for item in logistics.itinerary], indent=2
    )
    budget_text = json.dumps(budget.model_dump(), indent=2)

    venue_rules = "No venue rules document was provided."
    if retriever:
        activities_summary = "\n".join(
            f"- {item.time}: {item.activity}" for item in logistics.itinerary
        )
        docs = await retriever.ainvoke(activities_summary)
        venue_rules = "\n\n".join(doc.page_content for doc in docs)

    chain = SUPERVISOR_PROMPT | llm
    raw = await chain.ainvoke(
        {
            "itinerary": itinerary_text,
            "budget": budget_text,
            "venue_rules": venue_rules,
        }
    )
    parsed = parse_llm_json(raw.content)

    return SupervisorOutput(**parsed)
