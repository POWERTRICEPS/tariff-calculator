from fastapi import FastAPI
from pydantic import BaseModel
from duty_calc import tarriff

from hts_search import search_hts_with_ai
from gpt.gpt_duty import gpt_details
import math



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

class TariffRequest(BaseModel):
    description: str
    country: str
    value: float
    
@app.get("/")
def home():
    return "running"

@app.post("/calculate")
def calculate_tariff(data: TariffRequest):
    
    matches = search_hts_with_ai(data.description, data.country, k=5)
    best = matches[0]
    
    
    gpt_duties = gpt_details(
        product=data.description,
        hts_code=best["hts_code"],
        country=data.country,
        base_duty=best["base_duty"],
        value_usd=data.value
    )
    
    sanitized_gpt = clean_floats(gpt_duties)

    return {
        "description": data.description,
        "country": data.country,
        "value": data.value,
        "top_matches": matches,
        "gpt_duty_breakdown": sanitized_gpt
}