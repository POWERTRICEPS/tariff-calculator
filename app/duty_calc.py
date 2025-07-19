def tarriff(value, country):
    base = 4.9
    universal = 10.0
    if country.lower() == "china":
        section_301 = 25.0
    else:
        section_301 = 0.0
    
    
    total_percent = base + universal + section_301
    duty = value *  total_percent/100
    
    return {
        "base": base,
        "universal": universal,
        "section_301": section_301,
        "total_percent": total_percent,
        "duty": round(duty, 2)
    }


    
def fetanyl(hts_code: str, country: str) -> bool:
    fentanyl_exempt_hts = {
    "4901.10.00.00",
    "8471.50.01",
    "8542.31.00",
    "8473.30.1140"
    }
    return (
        country.lower() in ["china", "hong kong"]
        and hts_code not in fentanyl_exempt_hts
    )