import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_sensor_stream(station_code: str, hours: int = 48, freq_minutes: int = 5) -> pd.DataFrame:
    """
    Generates a realistic-looking AWS sensor time series with daily seasonality + noise,
    then injects a handful of fault types (spike, flatline, drift, missing) so the
    anomaly detector has real signal to catch, and the demo has visible, explainable anomalies.
    """
    n = int(hours * 60 / freq_minutes)
    timestamps = [datetime.utcnow() - timedelta(minutes=(n - i) * freq_minutes) for i in range(n)]

    t = np.linspace(0, hours / 24 * 2 * np.pi, n)  # daily cycle
    temperature = 25 + 5 * np.sin(t) + np.random.normal(0, 0.5, n)
    humidity = 60 + 10 * np.cos(t) + np.random.normal(0, 2, n)
    pressure = 1013 + np.random.normal(0, 1, n)
    wind_speed = np.abs(np.random.normal(5, 2, n))

    df = pd.DataFrame({
        "timestamp": timestamps,
        "station_code": station_code,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
    })

    fault_idx = np.random.choice(n, size=max(2, n // 60), replace=False)
    for i in fault_idx:
        fault_type = np.random.choice(["spike", "flatline", "drift", "missing"])
        if fault_type == "spike":
            df.loc[i, "temperature"] += np.random.choice([-1, 1]) * np.random.uniform(15, 25)
        elif fault_type == "flatline":
            end = min(i + 6, n - 1)
            df.loc[i:end, "humidity"] = df.loc[i, "humidity"]
        elif fault_type == "drift":
            df.loc[i:, "pressure"] += np.linspace(0, 8, len(df) - i)
        elif fault_type == "missing":
            df.loc[i, "wind_speed"] = np.nan

    return df
