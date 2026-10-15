# WattWise AI — Smart Energy Consumption Pattern & Anomaly Discovery

A student internship prototype aligned with UN SDG 7 (Affordable and Clean Energy) and SDG 12 (Responsible Consumption and Production).

## What it does
- Displays an energy-consumption dashboard.
- Uses scikit-learn IsolationForest to flag statistically unusual readings.
- Accepts a CSV upload with the columns below.
- Shows a recent-consumption chart and lets you download scored sample records.

## Important accuracy note
The included dataset is synthetic and intended only for demonstration. The Isolation Forest model is fit to the dataset currently being analyzed, so its flags are relative to that dataset. They are not proof of equipment failure, energy waste, billing errors, or a safety issue. No real-world validation or measured energy savings are claimed.

## Run locally
Recommended: Python 3.10–3.12.
1. Extract the ZIP.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Start: `python app.py`
6. Open the local URL printed by Flask (usually http://127.0.0.1:5000).

## CSV format
Required columns:
- `timestamp` — text/date-time
- `hour` — integer 0–23
- `day_of_week` — integer 0–6 (Monday=0)
- `temperature_c` — numeric
- `consumption_kwh` — numeric hourly consumption

At least 20 valid rows are required. The app does not connect to smart meters or utility APIs. Uploaded CSVs are processed in memory for that request and are not stored by the application.

## Model
Isolation Forest is an unsupervised anomaly-detection algorithm. Features: hour, day_of_week, temperature_c, consumption_kwh. The model uses `contamination=0.025` as an initial demo setting, not a calibrated operational threshold.

## Limitations and next steps
- Validate against real, consented meter data.
- Compare against simple statistical baselines and domain-reviewed events.
- Tune thresholds using expert feedback and seasonal patterns.
- Add authentication, access controls, secure deployment, and privacy review before any public use.
- Add recommendations only after the cause of an anomaly has been investigated.

## Files
- `app.py` — Flask application and ML scoring
- `templates/index.html` — dashboard UI
- `static/style.css` — responsive styling
- `sample_energy_data.csv` — synthetic sample data
"# WattWise-AI" 
