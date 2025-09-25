from typing import List, Dict
from collections import defaultdict
from .models import Delivery, Stats, ShiftAdvice

def summarize(rows: List[Delivery]) -> Stats:
    if not rows:
        return Stats(deliveries=0, hours=0, miles=0, earnings_usd=0, tips_usd=0, per_hour=0, per_mile=0)
    deliveries = len(rows)
    hours = sum(d.duration_min for d in rows) / 60.0
    miles = sum(d.miles for d in rows)
    earnings = sum(d.payout_usd + d.tips_usd for d in rows)
    tips = sum(d.tips_usd for d in rows)
    per_hour = (earnings / hours) if hours else 0
    per_mile = (earnings / miles) if miles else 0
    return Stats(deliveries=deliveries, hours=hours, miles=miles,
                 earnings_usd=earnings, tips_usd=tips,
                 per_hour=per_hour, per_mile=per_mile)

def shift_advice(rows: List[Delivery]) -> ShiftAdvice:
    if not rows: return ShiftAdvice(by_hour=[], by_weekday=[])
    h_buckets: Dict[int, List[float]] = defaultdict(list)
    d_buckets: Dict[int, List[float]] = defaultdict(list)
    # attribute each delivery’s payout to its hour/weekday on a per-hour basis
    for d in rows:
        hr = d.ts.hour
        wd = d.ts.weekday()  # 0=Mon
        pay = d.payout_usd + d.tips_usd
        hrs = max(d.duration_min / 60.0, 0.01)
        rate = pay / hrs
        h_buckets[hr].append(rate)
        d_buckets[wd].append(rate)
    by_hour = sorted([(h, sum(v)/len(v)) for h, v in h_buckets.items()], key=lambda x: -x[1])
    by_weekday = sorted([(wd, sum(v)/len(v)) for wd, v in d_buckets.items()], key=lambda x: -x[1])
    return ShiftAdvice(by_hour=by_hour, by_weekday=by_weekday)

def maps_link(stops: List[str]) -> str:
    # Build a Google Maps directions link with optional waypoints (no API needed)
    import urllib.parse as up
    if not stops: return "https://maps.google.com/"
    base = "https://www.google.com/maps/dir/"
    encoded = "/".join(up.quote_plus(s) for s in stops)
    return base + encoded
