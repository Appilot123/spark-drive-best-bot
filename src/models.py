from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Delivery(BaseModel):
    ts: datetime
    zone: str = Field(default="unknown")
    miles: float = 0.0
    duration_min: float = 0.0
    payout_usd: float = 0.0
    tips_usd: float = 0.0
    order_type: str = "unknown"  # batch / curbside / return etc.
    pickup_address: Optional[str] = None
    dropoff_address: Optional[str] = None

class Stats(BaseModel):
    deliveries: int
    hours: float
    miles: float
    earnings_usd: float
    tips_usd: float
    per_hour: float
    per_mile: float

class ShiftAdvice(BaseModel):
    by_hour: List[tuple]      # [(hour, avg $/hr)]
    by_weekday: List[tuple]   # [(weekday, avg $/hr)]
