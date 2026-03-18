"""Agent 1 – The Logistical Parser

Extracts the attendee list, arrival/departure times, dietary restrictions,
and desired activities from a chaotic group-chat text export.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from backend.config import OPENAI_API_KEY, LLM_MODEL
from backend.models import LogisticalOutput
from backend.utils.parsers import parse_llm_json

EXTRACT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a precise data-extraction assistant. "
            "Given the group-chat log below, return a JSON object with:\n"
            '  "attendees": [{{"name": str, "arrival": str|null, "departure": str|null, "dietary_restrictions": [str]}}],\n'
            '  "itinerary": [{{"time": str, "activity": str, "notes": str}}]\n'
            "Extract ALL proposed plans, activities, and schedule items. "
            "Include the day/time context when mentioned (e.g. 'Friday 7pm', 'Saturday 11pm'). "
            "Only include information explicitly stated in the chat. "
            "Output valid JSON only—no markdown fences, no commentary.",
        ),
        ("human", "{chat_log}"),
    ]
)


async def run_logistical_agent(chat_log: str) -> LogisticalOutput:
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )

    chain = EXTRACT_PROMPT | llm
    raw = await chain.ainvoke({"chat_log": chat_log})
    extracted = parse_llm_json(raw.content)

    return LogisticalOutput(
        attendees=extracted.get("attendees", []),
        itinerary=extracted.get("itinerary", []),
    )
