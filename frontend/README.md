# AWS Anomaly Detection — Frontend

React + TypeScript + Tailwind CSS v4 + Recharts. Built to match your backend's API contract exactly — point it at your running FastAPI server and it works with zero config changes.

## 1. Setup & Installation

### Step 1: Copy environment file
- **Windows (PowerShell)**:
  ```powershell
  Copy-Item .env.example .env
  ```
- **Linux / macOS**:
  ```bash
  cp .env.example .env
  ```

### Step 2: Install dependencies
```bash
npm install
```

## 2. Run Frontend Development Server

Ensure your backend is running (`uvicorn app.main:app --reload --port 8000`), then start the frontend:

```bash
npm run dev
```

Open the URL shown in the terminal (default: `http://localhost:5173`).

## 3. What's already verified working

- `npm run build` compiles clean with **zero TypeScript errors**
- Every API call in `src/api/client.ts` matches the backend's real response shapes (tested against a running backend with seeded demo data)
- Live polling every 15 seconds so the dashboard updates without a manual refresh

## 4. Design direction

The look is "mission control for a fleet of weather stations" rather than a generic SaaS dashboard:
- **Dark instrument-panel background** with two accent colors that carry real meaning — teal for nominal data, amber for a flagged anomaly. Not decorative, tied to the data itself.
- **Two type families**: Space Grotesk for headings/labels, IBM Plex Mono for every number and data readout (station codes, sensor values, timestamps, anomaly scores) — gives it a console/readout feel appropriate to the subject.
- **Left-aligned instrument layout**: station fleet list on the left (with live status dots), charts + a live anomaly feed on the right — not a centered marketing-style page.

All of this lives in `src/index.css` (`@theme` block) if you want to adjust colors or fonts — no separate `tailwind.config.js`, this project uses Tailwind v4's CSS-based config.

## 5. Project structure

```
src/
├── App.tsx                    # Main layout — sidebar + charts + anomaly feed
├── types/index.ts              # TypeScript interfaces matching the backend exactly
├── api/client.ts                # Typed functions for every backend endpoint
├── hooks/useStationData.ts       # React Query hooks — polling + explanation mutation
├── components/
│   ├── StationSidebar.tsx      # Fleet list with status indicator dots
│   ├── DashboardStats.tsx      # Summary stat strip (readings, anomalies, uptime)
│   ├── SensorChart.tsx          # Recharts line chart with anomaly markers
│   ├── AnomalyFeed.tsx           # Scrollable list of anomaly cards
│   └── AnomalyCard.tsx            # Individual card, expands to fetch/show NVIDIA explanation
└── index.css                    # Design tokens (@theme) + font imports
```

## 6. How the AI explanation flow works

Clicking an anomaly card in the feed expands it and, if no explanation is cached yet, calls `GET /api/anomalies/{id}/explain` — this is exactly the NVIDIA NIM call your backend teammate wired up. The result gets cached on the backend, so re-opening the same card later loads instantly instead of re-calling the API.

If the backend or NVIDIA call fails, the card shows a graceful "couldn't reach the explanation service" message instead of crashing — important for demo day reliability.

## 7. If something doesn't connect

- Blank sidebar / "Can't reach the backend" message → confirm `uvicorn` is actually running and `http://localhost:8000/health` returns `{"status": "ok"}` in your browser
- Empty charts for a station → your backend teammate needs to run `python scripts/seed_demo_data.py` at least once
- CORS errors in the browser console → check the backend's `CORSMiddleware` origins in `app/main.py` include your frontend's actual URL

## 8. Not built (intentionally, per the 5-day demo scope)

- No routing/multiple pages — everything lives on one dashboard view
- No authentication/login
- No mobile-specific redesign beyond basic responsiveness — desktop/projector is the target for a hackathon demo
