import os
import json
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

FEATURES = ["temperature", "humidity", "pressure", "wind_speed"]
MODEL_DIR = os.getenv("MODEL_DIR", "models_store")
os.makedirs(MODEL_DIR, exist_ok=True)


def _model_path(station_id: int) -> str:
    return os.path.join(MODEL_DIR, f"station_{station_id}.pkl")


def _baseline_path(station_id: int) -> str:
    return os.path.join(MODEL_DIR, f"station_{station_id}_baseline.json")


def train_isolation_forest(df: pd.DataFrame, station_id: int, contamination: float = 0.05):
    """Trains on historical data for one station and saves both the model and baseline stats
    (used later to classify *what kind* of anomaly a new flagged reading looks like)."""
    clean = df[FEATURES].ffill().bfill()
    model = IsolationForest(contamination=contamination, random_state=42, n_estimators=200)
    model.fit(clean)
    joblib.dump(model, _model_path(station_id))

    baseline = {f: {"mean": float(clean[f].mean()), "std": float(clean[f].std()) or 1.0} for f in FEATURES}
    with open(_baseline_path(station_id), "w") as fp:
        json.dump(baseline, fp)

    return model, baseline


def load_model(station_id: int):
    path, bpath = _model_path(station_id), _baseline_path(station_id)
    if os.path.exists(path) and os.path.exists(bpath):
        model = joblib.load(path)
        with open(bpath) as fp:
            baseline = json.load(fp)
        return model, baseline
    return None, None


def detect_batch(df: pd.DataFrame, model) -> pd.DataFrame:
    clean = df[FEATURES].ffill().bfill()
    out = df.copy()
    out["anomaly_score"] = model.decision_function(clean)
    out["is_anomaly"] = model.predict(clean) == -1
    return out


def classify_anomaly_type(reading: dict, baseline: dict) -> str:
    """Isolation Forest only says 'anomalous or not' — this heuristic gives a human-readable
    category for the dashboard/explanation prompt, based on which feature deviates most."""
    if reading.get("wind_speed") is None:
        return "missing"
    z_scores = {
        f: abs((reading[f] - baseline[f]["mean"]) / baseline[f]["std"])
        for f in FEATURES if reading.get(f) is not None
    }
    if not z_scores:
        return "missing"
    worst = max(z_scores, key=z_scores.get)
    return "spike" if z_scores[worst] > 4 else "drift"


def detect_single(model, baseline: dict, reading: dict):
    """Runs one new reading through an already-trained model. Returns (is_anomaly, score, type)."""
    row_df = pd.DataFrame([{f: reading.get(f) for f in FEATURES}])
    clean = row_df.ffill().fillna(0)
    score = float(model.decision_function(clean)[0])
    is_anomaly = bool(model.predict(clean)[0] == -1)
    anomaly_type = classify_anomaly_type(reading, baseline) if is_anomaly else "normal"
    return is_anomaly, score, anomaly_type
