from __future__ import annotations
from pydantic import BaseModel


class Attendee(BaseModel):
    name: str
    arrival: str | None = None
    departure: str | None = None
    dietary_restrictions: list[str] = []


class ItineraryItem(BaseModel):
    time: str
    activity: str
    notes: str = ""


class LogisticalOutput(BaseModel):
    attendees: list[Attendee] = []
    itinerary: list[ItineraryItem] = []


class BudgetItem(BaseModel):
    category: str
    estimated_cost: float
    notes: str = ""


class BudgetOutput(BaseModel):
    stated_budget: float | None = None
    estimated_items: list[BudgetItem] = []
    total_estimated: float = 0.0
    within_budget: bool = True
    budget_summary: str = ""


class Conflict(BaseModel):
    activity: str
    rule_violated: str
    severity: str = "high"
    alternatives: list[str] = []


class SupervisorOutput(BaseModel):
    conflicts: list[Conflict] = []
    approved_itinerary: list[ItineraryItem] = []
    supervisor_notes: str = ""


class TripReport(BaseModel):
    logistics: LogisticalOutput | None = None
    budget: BudgetOutput | None = None
    supervisor: SupervisorOutput | None = None
    status: str = "pending"
    errors: list[str] = []
