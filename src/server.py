from fastapi import FastAPI, UploadFile, File, Query
from typing import List, Optional
from .ingest import load_csv
from .utils import summarize, shift_advice, maps_link
from .models import Delivery, Stats, ShiftAdvice

app = FastAPI(title="Spark Driver Assistant (Compliant)")

STORE: List[Delivery] = []

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/import/csv")
async def import_csv(file: UploadFile = File(...)):
    global STORE
    data = await file.read()
    path = "/tmp/spark_earnings.csv"
    with open(path, "wb") as f:
        f.write(data)
    STORE = load_csv(path)
    return {"loaded": len(STORE)}

@app.get("/deliveries", response_model=List[Delivery])
def deliveries(limit: int = 200):
    return STORE[:limit]

@app.get("/stats", response_model=Stats)
def stats(zone: Optional[str] = Query(None), order_type: Optional[str] = Query(None)):
    rows = STORE
    if zone: rows = [r for r in rows if r.zone == zone]
    if order_type: rows = [r for r in rows if r.order_type == order_type]
    return summarize(rows)

@app.get("/advice", response_model=ShiftAdvice)
def advice():
    return shift_advice(STORE)

@app.get("/route")
def route(pickup: Optional[str] = None, dropoffs: Optional[str] = None):
    """
    Build a Google Maps multi-stop link without calling any external API.
    Params:
      pickup:      pickup address string
      dropoffs:    'addr1|addr2|addr3'
    """
    stops: List[str] = []
    if pickup: stops.append(pickup)
    if dropoffs:
        stops.extend([x for x in dropoffs.split("|") if x.strip()])
    return {"maps_url": maps_link(stops)}
