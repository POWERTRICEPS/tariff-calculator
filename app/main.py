from fastapi import FastAPI
from pydantic import BaseModel
from app.duty_calc import tarriff


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
    
    res = tarriff(data.value, data.country)
    return {
        "message": "Received!",
        "description": data.description,
        "country": data.country,
        "value": data.value,
        "tarriff": res
    }