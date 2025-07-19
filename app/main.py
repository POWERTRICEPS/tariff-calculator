from fastapi import FastAPI
from pydantic import BaseModel
from duty_calc import tarriff
from duty_calc import fetanyl

from hts_search import search_hts_with_ai
from gpt.gpt_duty import gpt_details
import math
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

df_hts = pd.read_csv("data/hts.csv", dtype=str).fillna("")
df_hts.columns = [col.strip() for col in df_hts.columns]

def get_base_duty_for_hts(hts_code: str) -> str:
    match = df_hts[df_hts["HTS Number"].str.strip() == hts_code.strip()]
    if not match.empty:
        return match.iloc[0]["General Rate of Duty"].strip() or "Unknown"
    return "Unknown"

    

def clean_nans(obj):
    if isinstance(obj, dict):
        return {k: clean_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nans(i) for i in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None  
    return obj


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    matches = search_hts_with_ai(data.description, data.country, k=20)
    cleaned_matches = clean_nans(matches)
    return {
        "description": data.description,
        "country": data.country,
        "value": data.value,
        "top_matches": cleaned_matches
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
    
    sanitized = clean_nans(gpt_duties)
    sanitized = clean_nans(sanitized)

    if fetanyl(data.hts_code, data.country):
        sanitized["fentanyl_tariff_percent"] = 10.0
    else:
        sanitized["fentanyl_tariff_percent"] = 0.0

    sanitized["reciprocal_tariff"] = 10.0
    sanitized["total_percent"] = (
        sanitized.get("base_duty_percent", 0) +
        sanitized.get("section_301_percent", 0) +
        sanitized.get("antidumping_percent", 0) +
        sanitized.get("other_tariffs_percent", 0) +
        sanitized.get("fentanyl_tariff_percent", 0) +
        sanitized.get("reciprocal_tariff_percent", 0) +
        sanitized.get("reciprocal_tariff", 0)
    )

    sanitized["total_duty_usd"] = round(data.value * sanitized["total_percent"] / 100, 2)
    

    


    return clean_nans({
        "hts_code": data.hts_code,
        "description": data.description,
        "country": data.country,
        "value": data.value,
        "base_duty": base_duty,
        "gpt_duty_breakdown": sanitized,

      
    })