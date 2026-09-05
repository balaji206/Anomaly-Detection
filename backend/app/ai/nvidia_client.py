import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "meta/llama-3.2-11b-vision-instruct"


def _get_client():
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None
    return OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)


def explain_anomaly(reading: dict, anomaly_score: float, anomaly_type: str) -> str:
    """
    Calls NVIDIA NIM (build.nvidia.com) to turn a raw anomaly detection into a
    human-readable explanation for the dashboard.

    Works with no API key set too — returns a clearly-labeled placeholder so the rest
    of the app (and your frontend teammates) can build/demo against this endpoint
    before you've grabbed your NVIDIA key.
    """
    client = _get_client()
    if client is None:
        return (
            f"[Demo placeholder — set NVIDIA_API_KEY to get real explanations] "
            f"This '{anomaly_type}' anomaly (score {anomaly_score:.2f}) would normally be "
            f"explained here by an NVIDIA NIM model based on the sensor readings: {reading}."
        )

    prompt = f"""You are a meteorological sensor diagnostics assistant.

An Automatic Weather Station reported this anomaly:
- Sensor readings: {reading}
- Detected anomaly type: {anomaly_type}
- Anomaly score: {anomaly_score:.3f} (more negative = more anomalous)

In 2-3 concise sentences, explain the most likely physical cause
(sensor fault, environmental interference, calibration drift, etc.)
and suggest one corrective action for a field technician."""

    model_name = os.getenv("NVIDIA_MODEL", DEFAULT_MODEL)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"NVIDIA NIM call failed ({type(e).__name__}): {e}")
        # Never let an NVIDIA hiccup crash the demo — surface a graceful message instead.
        return f"Explanation temporarily unavailable ({type(e).__name__}). Please retry."
