from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import io
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
app.secret_key = "change-this-for-local-demo"

DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_energy_data.csv")
REQUIRED = ["timestamp", "hour", "day_of_week", "temperature_c", "consumption_kwh"]

def load_data():
    df = pd.read_csv(DATA_PATH)
    return score_data(df)

def score_data(df):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    data = df.copy()
    for col in ["hour", "day_of_week", "temperature_c", "consumption_kwh"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=["hour", "day_of_week", "temperature_c", "consumption_kwh"])
    if len(data) < 20:
        raise ValueError("Please provide at least 20 valid readings.")
    features = data[["hour", "day_of_week", "temperature_c", "consumption_kwh"]]
    model = IsolationForest(n_estimators=150, contamination=0.025, random_state=42)
    model.fit(features)
    data["anomaly"] = model.predict(features) == -1
    data["anomaly_score"] = -model.decision_function(features)
    data["timestamp"] = data["timestamp"].astype(str)
    return data.sort_values("timestamp", ascending=False).reset_index(drop=True)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Choose a CSV file first.")
            return redirect(url_for("index"))
        try:
            uploaded = pd.read_csv(file)
            data = score_data(uploaded)
            source = "Uploaded CSV"
        except Exception as exc:
            error = str(exc)
            data = load_data()
            source = "Sample dataset (upload error)"
    else:
        data = load_data()
        source = "Sample demo dataset"

    total = len(data)
    anomalies = int(data["anomaly"].sum())
    avg = float(data["consumption_kwh"].mean())
    peak = float(data["consumption_kwh"].max())
    latest = data.head(12).to_dict(orient="records")
    chart = data.sort_values("timestamp").tail(48)
    chart_labels = chart["timestamp"].astype(str).str.replace("T", " ", regex=False).tolist()
    chart_values = [round(float(x), 3) for x in chart["consumption_kwh"]]
    anomaly_points = [
        {"x": i, "y": round(float(row["consumption_kwh"]), 3)}
        for i, (_, row) in enumerate(chart.iterrows()) if bool(row["anomaly"])
    ]
    records = data.head(100).to_dict(orient="records")
    return render_template("index.html", title="WattWise AI", total=total,
        anomalies=anomalies, avg=round(avg, 3), peak=round(peak, 3),
        latest=latest, chart_labels=chart_labels, chart_values=chart_values,
        anomaly_points=anomaly_points, records=records, source=source, error=error)

@app.route("/download")
def download():
    data = load_data()
    buffer = io.BytesIO()
    data.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(buffer, mimetype="text/csv", as_attachment=True,
                     download_name="wattwise_scored_sample.csv")

if __name__ == "__main__":
    app.run(debug=True)
