# AWS Anomaly Detection — Backend

FastAPI + Isolation Forest + NVIDIA NIM. Runs entirely locally with SQLite — **no cloud, Docker, or Postgres setup required for the demo.**

## 1. Setup (one-time)

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then optionally add your NVIDIA_API_KEY inside
```

## 2. Seed demo data

This generates 48 hours of realistic simulated sensor data for 3 stations, trains an Isolation Forest per station, and populates the database with real detected anomalies — so your dashboard has data the moment you open it.

```bash
python scripts/seed_demo_data.py
```

Re-run this any time you want to reset/refresh the demo data (it's additive, so delete `aws_anomaly.db` first if you want a clean slate).

## 3. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

Visit **http://localhost:8000/docs** — FastAPI's interactive docs. Test every endpoint here before your frontend teammates even start integrating.

## 4. Endpoints (the contract your frontend teammates build against)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Uptime check |
| GET | `/api/stations` | List all AWS stations |
| GET | `/api/sensors/{station_id}/readings?hours=24` | Time-series readings for charts |
| POST | `/api/sensors/ingest` | Push a new reading (runs it through the anomaly detector live) |
| GET | `/api/anomalies?station_id=&limit=` | List detected anomalies |
| GET | `/api/anomalies/{id}/explain` | Get (or generate + cache) an NVIDIA explanation |

`station_id` everywhere means the station **code** (e.g. `AWS-001`), not the internal DB row id — that's what the seed script and frontend both use.

## 5. NVIDIA NIM (optional but recommended before demo day)

1. Sign up free at **build.nvidia.com** — no credit card needed
2. Generate an API key (`nvapi-...`)
3. Put it in `.env` as `NVIDIA_API_KEY=nvapi-...`

Without a key, `/api/anomalies/{id}/explain` still works — it returns a clearly-labeled placeholder so you and your frontend teammates can build and test the full flow before you've grabbed a real key.

## 6. Project structure

```
app/
├── main.py              # FastAPI app + router registration
├── database.py          # SQLAlchemy engine/session (SQLite by default)
├── models.py             # DB tables: Station, SensorReading, Anomaly
├── schemas.py             # Pydantic request validation
├── ml/
│   ├── simulator.py      # Generates realistic sensor data + injects faults
│   └── detector.py        # Isolation Forest training/inference + anomaly-type heuristic
├── ai/
│   └── nvidia_client.py    # NVIDIA NIM calls, with safe fallback if no key set
└── routers/
    ├── stations.py, sensors.py, anomalies.py
scripts/
└── seed_demo_data.py     # Populates realistic demo data — run this first
```

## 7. Already verified working

All 6 endpoints were tested end-to-end (health check, station list, readings, ingest, anomaly list, and explanation generation) before this was handed to you — you're starting from a known-good baseline, not untested scaffolding.

## 8. What's intentionally simple (by design, for demo speed)

- **SQLite instead of Postgres** — zero setup. Swap `DATABASE_URL` in `.env` if you want to match your tech-stack slide exactly with a real Postgres instance later; nothing else in the code changes.
- **Anomaly type is a heuristic** (based on which sensor deviates most from its trained baseline), not a separate ML classifier — Isolation Forest itself only says "anomalous or not." This is enough to drive both the dashboard label and the NVIDIA explanation prompt.
- **No Autoencoder** — Isolation Forest alone is enough for a convincing, explainable demo. Add it later only if you have spare time (see the team plan doc).

## 9. Next steps for you

- [ ] Get your NVIDIA API key and drop it in `.env`
- [ ] Run the seed script, confirm data looks right via `/docs`
- [ ] Share this repo + the endpoint table above with your 2 frontend teammates
- [ ] If time allows: add more injected fault variety to `simulator.py`, or tune `contamination` in `detector.py` if you're seeing too many/few anomalies flagged
