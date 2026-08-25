# MonsoonMitra: Village-Level Monsoon Risk Alert

A simple prototype for sending early warnings about monsoon failure risk to rain-fed farming villages in India.

## How it works
- Uses the [Open-Meteo API](https://open-meteo.com/) to get 10-day precipitation forecasts.
- Compares the forecasted total precipitation to a threshold (default 50mm).
- Flags risk as:
  - **HIGH**: forecast < 50mm
  - **MEDIUM**: 50mm ≤ forecast < 100mm
  - **LOW**: forecast ≥ 100mm
- Outputs a CSV-like list and saves detailed results to `results.json`.

## Running the prototype
```bash
python monsoonmitra.py
```

## Sample output
```
MonsoonMitra - Village Monsoon Risk Assessment
============================================================
Ludhiana West (Punjab): 7.2 mm forecast -> Risk: HIGH
Hisar (Haryana): 45.9 mm forecast -> Risk: HIGH
Jaipur Rural (Rajasthan): 81.0 mm forecast -> Risk: MEDIUM
Indore Rural (Madhya Pradesh): 14.6 mm forecast -> Risk: HIGH
Pune Rural (Maharashtra): 92.3 mm forecast -> Risk: MEDIUM

Detailed results saved to /tmp/monsoonmitra/results.json
```

## Extending to SMS
To turn this into an actual alerting system:
1. Replace the `print` statements with an SMS gateway (e.g., Twilio, Firebase Cloud Messaging, or AWS SNS).
2. Use a list of actual village coordinates and phone numbers (from government APIs or NGOs).
3. Schedule the script to run every 3 days using `cron` or Cloud Scheduler.

## Data Sources & Improvements
- **Precipitation threshold**: Adjust per region and crop (e.g., rice needs more water than millets).
- **Data sources**: For production, use IMD radar data via ISRO's MOSDAC or satellite data from Google Earth Engine.
- **Model**: Replace the simple threshold with a Vertex AI model trained on historical yield vs. weather data.

## Disclaimer
This is a prototype for demonstration. Not for actual agricultural decision-making without further validation.