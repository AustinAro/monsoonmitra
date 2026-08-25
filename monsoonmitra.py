#!/usr/bin/env python3
"""
MonsoonMitra: Simple village-level monsoon risk alert using Open-Meteo API.
Fetches 10-day precipitation forecast and flags risk if forecast sum < threshold.
"""

import os
import requests
import json
from typing import List, Dict

# Threshold: total precipitation (mm) over next 10 days below which risk is HIGH
# Adjust based on region/crop; 50mm is a rough placeholder for rain-fed kharif
PRECIP_THRESHOLD_MM = 50.0

VILLAGES = [
    {"name": "Ludhiana West", "state": "Punjab", "lat": 30.9, "lon": 75.8},
    {"name": "Hisar", "state": "Haryana", "lat": 29.1, "lon": 75.7},
    {"name": "Jaipur Rural", "state": "Rajasthan", "lat": 26.9, "lon": 75.8},
    {"name": "Indore Rural", "state": "Madhya Pradesh", "lat": 22.7, "lon": 75.9},
    {"name": "Pune Rural", "state": "Maharashtra", "lat": 18.5, "lon": 73.9},
]

def fetch_forecast(lat: float, lon: float) -> List[float]:
    """Fetch daily precipitation sum (mm) for next 10 days."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_sum",
        "timezone": "Asia/Kolkata",
        "forecast_days": 10,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("daily", {}).get("precipitation_sum", [])

def assess_risk(village: Dict) -> Dict:
    try:
        precip = fetch_forecast(village["lat"], village["lon"])
        total = sum(precip) if precip else 0.0
        risk = "HIGH" if total < PRECIP_THRESHOLD_MM else "LOW"
        # Optional medium tier
        if PRECIP_THRESHOLD_MM <= total < PRECIP_THRESHOLD_MM * 2:
            risk = "MEDIUM"
        return {
            **village,
            "forecast_precip_mm": round(total, 1),
            "risk": risk,
            "daily_precip": [round(p, 1) for p in precip],
        }
    except Exception as e:
        return {
            **village,
            "error": str(e),
            "risk": "ERROR",
        }

def main():
    print("MonsoonMitra - Village Monsoon Risk Assessment")
    print("=" * 60)
    results = []
    for v in VILLAGES:
        r = assess_risk(v)
        results.append(r)
        if "error" in r:
            print(f"{r['name']} ({r['state']}): ERROR - {r['error']}")
        else:
            print(f"{r['name']} ({r['state']}): {r['forecast_precip_mm']} mm forecast -> Risk: {r['risk']}")
    # Save results to JSON for possible delivery
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to {out_path}")

if __name__ == "__main__":
    main()