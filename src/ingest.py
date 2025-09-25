import pandas as pd
from dateutil import parser
from typing import List
from .models import Delivery

# Expected columns (rename in a sheet if needed):
# timestamp, zone, miles, duration_min, payout_usd, tips_usd, order_type,
# pickup_address?, dropoff_address?
def load_csv(path: str) -> List[Delivery]:
    df = pd.read_csv(path)
    df = df.fillna({"tips_usd": 0})
    out: List[Delivery] = []
    for _, r in df.iterrows():
        out.append(Delivery(
            ts=parser.parse(str(r["timestamp"])),
            zone=str(r.get("zone", "unknown")),
            miles=float(r.get("miles", 0) or 0),
            duration_min=float(r.get("duration_min", 0) or 0),
            payout_usd=float(r.get("payout_usd", 0) or 0),
            tips_usd=float(r.get("tips_usd", 0) or 0),
            order_type=str(r.get("order_type", "unknown")),
            pickup_address=str(r.get("pickup_address")) if "pickup_address" in df.columns else None,
            dropoff_address=str(r.get("dropoff_address")) if "dropoff_address" in df.columns else None,
        ))
    return out
