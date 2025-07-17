from fastapi import FastAPI
from pydantic import BaseModel
from duty_calc import tarriff

from hts_search import search_hts_with_ai
from gpt.gpt_duty import gpt_details
import math
import pandas as pd

df_hts = pd.read_csv("data/hts.csv", dtype=str).fillna("")
df_hts.columns = [col.strip() for col in df_hts.columns]
def get_base_duty_for_hts(hts_code: str) -> str:
    match = df_hts[df_hts["HTS Number"].str.strip() == hts_code.strip()]
    if not match.empty:
        return match.iloc[0]["General Rate of Duty"].strip() or "Unknown"
    return "Unknown"

    

def clean_floats(obj):
    if isinstance(obj, dict):
        return {k: clean_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_floats(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return "Unknown"
        return round(obj, 2) 
    return obj

app = FastAPI()

class MatchRequest(BaseModel):
    description: str
    country: str
    value: float

class TariffRequest(BaseModel):
    hts_code: str
    description: str
    country: str
    value: float
    
@app.get("/")
def home():
    return "running"


@app.post("/match")
def match(data: MatchRequest):
    matches = search_hts_with_ai(data.description, data.country, k=5)
    return {
        "description": data.description,
        "country": data.country,
        "value": data.value,
        "top_matches": matches
    }




@app.post("/calculate")
def calculate_tariff(data: TariffRequest):
    
    base_duty = get_base_duty_for_hts(data.hts_code) or "Unknown"

    gpt_duties = gpt_details(
        product=data.description,
        hts_code=data.hts_code,
        country=data.country,
        base_duty=base_duty,
        value_usd=data.value
    )
    
    sanitized = clean_floats(gpt_duties)

    return {
        "hts_code": data.hts_code,
        "description": data.description,
        "country": data.country,
        "value": data.value,
        "base_duty": base_duty,
        "gpt_duty_breakdown": sanitized
    }