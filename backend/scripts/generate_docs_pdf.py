import os
import sys
import subprocess
import time
import json
import urllib.request
import asyncio
import websockets
import tempfile
import base64

# Define the comprehensive HTML documentation
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Mavericks — AWS Anomaly Detection Master Documentation</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {
      content: counter(page);
    }
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1a202c;
    background: #ffffff;
    line-height: 1.6;
    font-size: 10pt;
  }

  .cover-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 85vh;
    padding: 40px 20px;
    border-bottom: 2px solid #e2e8f0;
  }

  .badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 8.5pt;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 16px;
  }

  .badge-primary {
    background: #ebf8ff;
    color: #2b6cb0;
    border: 1px solid #bee3f8;
  }

  .badge-success {
    background: #f0fff4;
    color: #276749;
    border: 1px solid #c6f6d5;
  }

  .badge-warn {
    background: #fffaf0;
    color: #9c4221;
    border: 1px solid #feebc8;
  }

  .badge-info {
    background: #edf2f7;
    color: #4a5568;
    border: 1px solid #e2e8f0;
  }

  h1.cover-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.15;
    margin-bottom: 12px;
  }

  .cover-subtitle {
    font-size: 13pt;
    color: #475569;
    margin-bottom: 28px;
    font-weight: 400;
  }

  .cover-meta {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px 20px;
    margin-top: 24px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    font-size: 9.5pt;
  }

  .cover-meta div strong {
    color: #0f172a;
  }

  h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 17pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 24px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1.5px solid #cbd5e1;
    page-break-after: avoid;
  }

  h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13pt;
    font-weight: 600;
    color: #1e293b;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }

  h3 {
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }

  p {
    margin-bottom: 10px;
    color: #334155;
  }

  ul, ol {
    margin-left: 22px;
    margin-bottom: 12px;
    color: #334155;
  }

  li {
    margin-bottom: 4px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 18px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }

  th, td {
    padding: 8px 10px;
    border: 1px solid #cbd5e1;
    text-align: left;
    vertical-align: top;
  }

  th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }

  tr:nth-child(even) {
    background-color: #f8fafc;
  }

  code {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }

  pre {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8pt;
    background: #0f172a;
    color: #f8fafc;
    padding: 12px 14px;
    border-radius: 6px;
    margin: 10px 0 14px 0;
    overflow-x: auto;
    line-height: 1.45;
    page-break-inside: avoid;
  }

  pre code {
    background: transparent;
    border: none;
    color: inherit;
    padding: 0;
  }

  .callout {
    background: #f8fafc;
    border-left: 4px solid #3b82f6;
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0 16px 0;
    page-break-inside: avoid;
  }

  .callout-warn {
    border-left-color: #f59e0b;
    background: #fffbeb;
  }

  .callout-success {
    border-left-color: #10b981;
    background: #f0fdf4;
  }

  .section-break {
    page-break-before: always;
  }

  .flow-box {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 8px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    line-height: 1.4;
    page-break-inside: avoid;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    page-break-inside: avoid;
  }
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <span class="badge badge-primary">SIH26073 &bull; Hackathon Master Documentation</span>
  <h1 class="cover-title">Mavericks &mdash; AWS Anomaly Detection</h1>
  <p class="cover-subtitle">AI/ML-Based Intelligent Telemetry Monitoring & NVIDIA NIM Diagnostics for Automatic Weather Stations</p>
  
  <div class="callout callout-success">
    <strong>Prototype Status:</strong> 100% Fully Functional Local Prototype (FastAPI Backend + React 19 / Vite / Tailwind v4 Frontend + Scikit-Learn Isolation Forest + NVIDIA NIM LLM Diagnostics).
  </div>

  <div class="cover-meta">
    <div><strong>Problem Statement:</strong> SIH26073 &mdash; Anomaly Detection for AWS</div>
    <div><strong>Team Name:</strong> Mavericks (Team Size: 6)</div>
    <div><strong>Backend Engine:</strong> Python 3.13 / FastAPI / Scikit-learn / SQLAlchemy</div>
    <div><strong>Frontend Interface:</strong> React 19 / Vite / Recharts / Tailwind CSS v4</div>
    <div><strong>ML Architecture:</strong> Unsupervised Isolation Forest (200 Estimators)</div>
    <div><strong>AI Diagnostic Copilot:</strong> NVIDIA NIM (meta/llama-3.2-11b-vision-instruct)</div>
    <div><strong>Local Database:</strong> SQLite (aws_anomaly.db) / Postgres-Ready</div>
    <div><strong>Documentation Date:</strong> September 2026</div>
  </div>
</div>

<!-- PART 1 -->
<h1>PART 1 &mdash; PROJECT OVERVIEW</h1>

<h3>1.1 Project Name</h3>
<p><strong>Mavericks &mdash; AWS Anomaly Detection</strong> (Internal Competition ID: <em>SIH26073 &mdash; AI/ML-Based Intelligent Anomaly Detection for Automatic Weather Stations</em>). The frontend dashboard is branded as <strong>Mavericks &mdash; AWS Fleet Monitor</strong>.</p>

<h3>1.2 One-Line Explanation</h3>
<p><em>"This application helps meteorological authorities and field technicians monitor remote Automatic Weather Stations by automatically detecting multi-sensor malfunctions using Machine Learning and translating raw telemetry faults into plain-English diagnostics and repair actions using NVIDIA AI."</em></p>

<h3>1.3 Problem Being Solved</h3>
<p>Automatic Weather Stations (AWS) are deployed across India in isolated terrains (high mountains, remote coastlines, agricultural belts) to capture critical meteorological parameters: temperature, humidity, atmospheric pressure, and wind speed. Due to harsh environmental exposure, sensors regularly degrade, suffer calibration drift, flatline, spike from electrical surges, or disconnect entirely.</p>
<ul>
  <li><strong>Who has this problem:</strong> National weather agencies (e.g., IMD), disaster management divisions, agricultural forecast planners, and field maintenance engineers.</li>
  <li><strong>Why it is important:</strong> Inaccurate telemetry pollutes numerical weather prediction models, leading to missed flood/cyclone warnings or false alerts that cost lives and economic damage.</li>
  <li><strong>What happens without this application:</strong> Failures go unnoticed for weeks until corrupted datasets are discovered manually, or technicians waste massive resources conducting blind physical inspections across healthy towers.</li>
</ul>

<h3>1.4 Solution & User Journey</h3>
<p>Mavericks automates end-to-end station surveillance without manual data science overhead:</p>
<div class="flow-box">
[Remote Weather Sensors] &rarr; Telemetry Ingestion API (FastAPI) &rarr; Isolation Forest ML Engine &rarr; Anomaly Scoring &rarr; Heuristic Fault Classification &rarr; NVIDIA NIM Diagnostic LLM &rarr; Mission-Control React Dashboard &rarr; Technician Dispatches Targeted Field Fix
</div>

<h3>1.5 Main Purpose</h3>
<p>To provide a zero-configuration, live fleet monitoring dashboard that continuously checks sensor integrity, visually marks aberrant timestamps on interactive curves, and provides instant, plain-English troubleshooting advice.</p>

<h3>1.6 Target Users</h3>
<ol>
  <li><strong>Field Technicians:</strong> Require immediate physical diagnosis (e.g., "radiation shield detached") before traveling to remote towers.</li>
  <li><strong>Meteorological Analysts:</strong> Require flagged anomalous timestamps to filter out corrupted data from forecasting simulations.</li>
  <li><strong>Fleet Supervisors:</strong> Need station uptime percentages, 24h reading counts, and multi-station health statuses.</li>
</ol>

<h3>1.7 Main Features Matrix</h3>
<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>What It Does</th>
      <th>User Benefit</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Fleet Navigation Sidebar</strong></td>
      <td>Lists all AWS stations with dynamic green/amber health status dots</td>
      <td>One-click station switching; immediately reveals which stations have unresolved faults</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>Fleet Health KPI Cards</strong></td>
      <td>Computes 24h packet count, total anomalies, uptime %, and latest temperature</td>
      <td>Instant high-level operational overview of active station</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>Multi-Sensor Visualizer</strong></td>
      <td>Interactive 24h time-series line charts for Temperature, Humidity, Pressure, Wind</td>
      <td>Visual validation of daily seasonal curves and environmental behavior</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>In-Chart Anomaly Pinpointing</strong></td>
      <td>Renders custom amber circular markers on the exact timestamps where readings failed</td>
      <td>Instantly identifies the timing and severity of sensor failures</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>Live Anomaly Feed</strong></td>
      <td>Scrollable incident queue showing fault type, timestamp, station ID, and score</td>
      <td>Chronological audit trail of all detected anomalies requiring attention</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>NVIDIA NIM AI Explanations</strong></td>
      <td>Invokes Llama-3.2 vision-instruct to generate physical root-cause & field action</td>
      <td>Converts cryptic ML math into actionable instructions for maintenance crews</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>15s Background Polling</strong></td>
      <td>Auto-refreshes data using TanStack React Query without manual page reload</td>
      <td>Live mission-control experience with zero manual intervention</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>Sensor Simulator & Fault Injector</strong></td>
      <td>Generates realistic seasonal telemetry with injected spikes, drifts, flatlines, missing data</td>
      <td>Allows end-to-end testing and demo demonstration without real hardware connected</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
    </tr>
    <tr>
      <td><strong>Autoencoder Deep Learning</strong></td>
      <td>Neural network reconstruction error for anomaly detection</td>
      <td>Advanced alternative anomaly detector</td>
      <td><span class="badge badge-info">&bull; Planned (Cut for 5-Day)</span></td>
    </tr>
    <tr>
      <td><strong>Azure Cloud Deployment</strong></td>
      <td>Dockerized deployment to Azure App Service and Static Web Apps</td>
      <td>Public web access</td>
      <td><span class="badge badge-info">&bull; Planned (Cut for 5-Day)</span></td>
    </tr>
  </tbody>
</table>

<!-- PART 2 -->
<h1 class="section-break">PART 2 &mdash; TECHNOLOGY STACK</h1>

<h2>Frontend Technologies</h2>
<table>
  <thead>
    <tr>
      <th>Technology</th>
      <th>Version</th>
      <th>Why Used</th>
      <th>Where Used & Key Files</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>React</strong></td>
      <td>19.2.8</td>
      <td>Declarative UI component model with efficient state updates</td>
      <td>Core framework across <code>frontend/src/</code> (<code>main.tsx</code>, <code>App.tsx</code>)</td>
    </tr>
    <tr>
      <td><strong>TypeScript</strong></td>
      <td>6.0.2</td>
      <td>Strict static typing matching backend Pydantic API response shapes</td>
      <td>All components and definitions (<code>types/index.ts</code>, <code>client.ts</code>)</td>
    </tr>
    <tr>
      <td><strong>Vite</strong></td>
      <td>8.2.2</td>
      <td>Fast native ES module development server and bundler</td>
      <td>Build setup (<code>vite.config.ts</code>, <code>package.json</code>)</td>
    </tr>
    <tr>
      <td><strong>Tailwind CSS</strong></td>
      <td>4.3.3</td>
      <td>Utility-first CSS engine configured via <code>@theme</code> tokens</td>
      <td>Dark mission-control styling (<code>index.css</code>, all UI components)</td>
    </tr>
    <tr>
      <td><strong>TanStack React Query</strong></td>
      <td>5.102.8</td>
      <td>Server state management, automated polling, and async mutation lifecycle</td>
      <td>Telemetry caching and auto-polling (<code>hooks/useStationData.ts</code>)</td>
    </tr>
    <tr>
      <td><strong>Recharts</strong></td>
      <td>3.10.1</td>
      <td>Composable SVG charting library for responsive time-series curves</td>
      <td>Sensor telemetry visualization (<code>components/SensorChart.tsx</code>)</td>
    </tr>
    <tr>
      <td><strong>Axios</strong></td>
      <td>1.20.0</td>
      <td>Promise-based HTTP client for structured REST API communication</td>
      <td>Backend API client layer (<code>api/client.ts</code>)</td>
    </tr>
    <tr>
      <td><strong>Lucide React</strong></td>
      <td>1.41.0</td>
      <td>Clean icon set for micro-interactions</td>
      <td>Accordions, loading spinners, icons (<code>components/AnomalyCard.tsx</code>)</td>
    </tr>
  </tbody>
</table>

<h2>Backend Technologies</h2>
<table>
  <thead>
    <tr>
      <th>Technology</th>
      <th>Version</th>
      <th>Why Used</th>
      <th>Where Used & Key Files</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Python</strong></td>
      <td>3.13+</td>
      <td>Modern execution environment with rich scientific computing libraries</td>
      <td>Entire backend codebase (<code>backend/app/</code>)</td>
    </tr>
    <tr>
      <td><strong>FastAPI</strong></td>
      <td>0.141.1</td>
      <td>High-speed async web framework with automatic OpenAPI Swagger generation</td>
      <td>Server entry point and routes (<code>app/main.py</code>, <code>app/routers/</code>)</td>
    </tr>
    <tr>
      <td><strong>Uvicorn</strong></td>
      <td>0.52.4</td>
      <td>Asynchronous Server Gateway Interface (ASGI) server with WatchFiles</td>
      <td>Development and production server runtime</td>
    </tr>
    <tr>
      <td><strong>SQLAlchemy</strong></td>
      <td>2.0.52</td>
      <td>Object Relational Mapper providing vendor-neutral database modeling</td>
      <td>Database engine and ORM tables (<code>app/database.py</code>, <code>app/models.py</code>)</td>
    </tr>
    <tr>
      <td><strong>Scikit-Learn</strong></td>
      <td>1.9.0</td>
      <td>Unsupervised Isolation Forest algorithm implementation</td>
      <td>Station anomaly detector (<code>app/ml/detector.py</code>)</td>
    </tr>
    <tr>
      <td><strong>Pandas & NumPy</strong></td>
      <td>3.0.5 / 2.5.2</td>
      <td>Vectorized math, seasonal generation, and missing data imputation</td>
      <td>Data processing (<code>app/ml/simulator.py</code>, <code>app/ml/detector.py</code>)</td>
    </tr>
    <tr>
      <td><strong>Joblib</strong></td>
      <td>1.6.0</td>
      <td>High-performance serialization for Python estimators</td>
      <td>Saving/loading model files in <code>models_store/</code></td>
    </tr>
    <tr>
      <td><strong>OpenAI SDK</strong></td>
      <td>3.8.0</td>
      <td>Client for standard OpenAI-compatible Chat Completion endpoints</td>
      <td>NVIDIA NIM API communication (<code>app/ai/nvidia_client.py</code>)</td>
    </tr>
    <tr>
      <td><strong>NVIDIA NIM</strong></td>
      <td>Llama-3.2-11b</td>
      <td>State-of-the-art LLM hosted on NVIDIA API catalog for diagnostics</td>
      <td>Root-cause analysis (<code>meta/llama-3.2-11b-vision-instruct</code>)</td>
    </tr>
    <tr>
      <td><strong>Python-Dotenv</strong></td>
      <td>1.2.3</td>
      <td>Loads environment variables securely from <code>.env</code> file</td>
      <td>Secret and URL configuration (<code>main.py</code>, <code>database.py</code>, <code>nvidia_client.py</code>)</td>
    </tr>
  </tbody>
</table>

<h2>Database Architecture & Schema</h2>
<p>The project defaults to a zero-configuration SQLite database (<code>aws_anomaly.db</code>) managed by SQLAlchemy ORM. It can be redirected to a cloud PostgreSQL database simply by updating <code>DATABASE_URL</code> in <code>.env</code> with zero code changes.</p>
<ul>
  <li><strong>stations:</strong> <code>id</code> (PK), <code>code</code> (e.g. 'AWS-001'), <code>name</code> ('Coimbatore AWS'), <code>location</code> ('Tamil Nadu').</li>
  <li><strong>sensor_readings:</strong> <code>id</code> (PK), <code>station_id</code> (FK), <code>timestamp</code> (DateTime), <code>temperature</code>, <code>humidity</code>, <code>pressure</code>, <code>wind_speed</code>, <code>is_anomaly</code> (Bool), <code>anomaly_score</code> (Float).</li>
  <li><strong>anomalies:</strong> <code>id</code> (PK), <code>reading_id</code> (FK), <code>station_id</code> (FK), <code>anomaly_type</code> ('spike' | 'drift' | 'missing'), <code>sensor</code> ('multi'), <code>anomaly_score</code>, <code>value</code>, <code>explanation</code> (Text), <code>detected_at</code>, <code>resolved</code> (Bool).</li>
</ul>

<!-- PART 3 -->
<h1 class="section-break">PART 3 &mdash; FOLDER STRUCTURE & KEY FILES</h1>

<pre><code>aws-anomaly-backend/
├── backend/
│   ├── .env                       # Local secrets (NVIDIA_API_KEY, DATABASE_URL)
│   ├── .env.example               # Configuration template
│   ├── aws_anomaly.db             # Active SQLite database file
│   ├── requirements.txt           # Python library dependencies
│   ├── README.md                  # Backend guide & API contract specifications
│   ├── app/
│   │   ├── database.py            # SQLAlchemy engine, session maker, get_db generator
│   │   ├── main.py                # FastAPI initialization, CORS, router mounting, /health
│   │   ├── models.py              # SQLAlchemy ORM models (Station, SensorReading, Anomaly)
│   │   ├── schemas.py             # Pydantic request body validation schemas
│   │   ├── ai/
│   │   │   └── nvidia_client.py   # NVIDIA NIM integration & dynamic client handling
│   │   ├── ml/
│   │   │   ├── detector.py        # Isolation Forest training, scoring, baseline stats
│   │   │   └── simulator.py       # Weather data stream generator with injected faults
│   │   └── routers/
│   │       ├── stations.py        # GET /api/stations
│   │       ├── sensors.py         # GET /api/sensors/{id}/readings & POST /ingest
│   │       └── anomalies.py       # GET /api/anomalies & GET /api/anomalies/{id}/explain
│   ├── models_store/              # Serialized ML artifacts (.pkl & baseline .json)
│   └── scripts/
│       └── seed_demo_data.py      # Populates 48h realistic demo data across all 3 stations
└── frontend/
    ├── package.json               # Node dependencies and scripts (dev, build)
    ├── vite.config.ts             # Vite build & Tailwind plugin config
    ├── index.html                 # HTML shell and Google Fonts links
    └── src/
        ├── main.tsx               # React root, QueryClientProvider mount
        ├── App.tsx                # Master 3-column layout & query coordination
        ├── index.css              # Tailwind v4 theme design tokens & styling
        ├── api/client.ts          # Axios client instance with typed endpoint functions
        ├── types/index.ts         # TypeScript interfaces matching backend models
        ├── hooks/useStationData.ts# React Query hooks with 15s auto-polling
        └── components/
            ├── StationSidebar.tsx # Fleet navigation with green/amber alert indicators
            ├── DashboardStats.tsx # KPI summary scorecard (Uptime, readings, latest temp)
            ├── SensorChart.tsx    # Recharts graph with custom AnomalyDot markers
            ├── AnomalyFeed.tsx    # Scrollable sidebar panel listing anomalies
            └── AnomalyCard.tsx    # Expandable alert card with AI explanation & retry</code></pre>

<!-- PART 4 & 5 -->
<h1 class="section-break">PARTS 4 & 5 &mdash; FRONTEND ARCHITECTURE & COMPONENTS</h1>

<h2>4.1 Frontend Architecture</h2>
<p>The frontend is structured as a reactive single-page dashboard (SPA). There are no multi-page routing delays; state changes (such as choosing a new weather station) immediately trigger cached React Query fetches, refreshing all statistics, charts, and anomaly queues simultaneously.</p>

<h2>5.1 Core Component Details</h2>

<h3>1. App (Master Layout Coordinator)</h3>
<p><strong>Location:</strong> <code>frontend/src/App.tsx</code><br>
<strong>Purpose:</strong> Controls top-level dashboard layout. Manages <code>selectedStationId</code> state and queries data for stations, readings, and anomalies.<br>
<strong>Layout:</strong> Three distinct columns: Left (StationSidebar), Center (Header + DashboardStats + 2x2 SensorChart grid), Right (AnomalyFeed).</p>

<h3>2. StationSidebar</h3>
<p><strong>Location:</strong> <code>frontend/src/components/StationSidebar.tsx</code><br>
<strong>Simple Meaning:</strong> The station selection list on the left.<br>
<strong>Technical Details:</strong> Iterates through the <code>stations</code> array. Matches station codes against a precomputed <code>Set</code> of unresolved anomalies (<code>unresolvedByStation</code>). Renders an amber status dot if unresolved anomalies exist, or a teal dot if nominal. Emits <code>onSelect(station.id)</code> on click.</p>

<h3>3. DashboardStats</h3>
<p><strong>Location:</strong> <code>frontend/src/components/DashboardStats.tsx</code><br>
<strong>Simple Meaning:</strong> Top scorecard summarizing station health.<br>
<strong>Technical Details:</strong> In-memory calculation across <code>readings</code> and <code>anomalies</code> props. Calculates total 24h packets received, total anomalies, station uptime percentage (<code>((total - anomalies) / total) * 100</code>), and the latest temperature.</p>

<h3>4. SensorChart</h3>
<p><strong>Location:</strong> <code>frontend/src/components/SensorChart.tsx</code><br>
<strong>Simple Meaning:</strong> The interactive line graph that shows sensor trends and marks bad readings.<br>
<strong>Technical Details:</strong> Reusable Recharts wrapper. Accepts <code>title</code>, <code>unit</code>, and <code>dataKey</code> (e.g. <code>temperature</code>). Formats ISO timestamps into readable <code>HH:MM</code> clock values. Employs a custom SVG dot component (<code>AnomalyDot</code>) that conditionally renders an amber circle (<code>r=4</code>) exclusively on data points where <code>payload.is_anomaly === true</code>.</p>

<h3>5. AnomalyFeed & AnomalyCard</h3>
<p><strong>Location:</strong> <code>frontend/src/components/AnomalyFeed.tsx</code> & <code>AnomalyCard.tsx</code><br>
<strong>Simple Meaning:</strong> The alert queue on the right where clicking an item explains the problem in plain English.<br>
<strong>Technical Details:</strong> <code>AnomalyFeed</code> maps anomaly records. <code>AnomalyCard</code> features internal accordion toggle state (<code>expanded</code>). When clicked, it invokes <code>useExplanation</code> (React Query mutation). If an explanation is cached in SQLite, it renders instantly; otherwise, it triggers NVIDIA NIM, displays a spinning loader, and renders the AI diagnosis once returned. Includes <code>shrink-0</code> to prevent flexbox clipping and an inline retry handler.</p>

<!-- PART 6 & 7 -->
<h1 class="section-break">PARTS 6 & 7 &mdash; STATE MANAGEMENT & API CONNECTION</h1>

<h2>6.1 State Management System</h2>
<div class="callout callout-success">
  <strong>Dual-Tier State Model:</strong> Combines lightweight React <code>useState</code> for local UI toggles with TanStack React Query v5 for asynchronous server state, automatic background polling, and cache invalidation.
</div>
<ul>
  <li><strong>Server State (React Query):</strong>
    <ul>
      <li><code>useStations()</code>: Cached under key <code>["stations"]</code>; polls every 15 seconds.</li>
      <li><code>useReadings(stationId, 24)</code>: Cached under key <code>["readings", stationId, 24]</code>; polls every 15 seconds.</li>
      <li><code>useAnomalies(stationId, limit)</code>: Cached under key <code>["anomalies", stationId, limit]</code>; polls every 15 seconds.</li>
      <li><code>useExplanation()</code>: React Query mutation that invokes <code>GET /api/anomalies/{id}/explain</code>. On success, executes <code>queryClient.invalidateQueries({ queryKey: ["anomalies"] })</code>, propagating the cached explanation across the fleet.</li>
    </ul>
  </li>
  <li><strong>Local State (React <code>useState</code>):</strong>
    <ul>
      <li><code>selectedStationId</code> (in <code>App.tsx</code>): Stores active station code (defaults to first station).</li>
      <li><code>expanded</code> (in <code>AnomalyCard.tsx</code>): Controls accordion open/close display.</li>
    </ul>
  </li>
</ul>

<h2>7.1 Complete API Communication Matrix</h2>
<table>
  <thead>
    <tr>
      <th>Frontend Caller</th>
      <th>Method</th>
      <th>Endpoint</th>
      <th>Backend Handler</th>
      <th>Database Action</th>
      <th>UI Consumer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>fetchStations()</code></td>
      <td>GET</td>
      <td><code>/api/stations</code></td>
      <td><code>stations.list_stations</code></td>
      <td><code>db.query(Station).all()</code></td>
      <td><code>StationSidebar</code> (fleet list)</td>
    </tr>
    <tr>
      <td><code>fetchReadings()</code></td>
      <td>GET</td>
      <td><code>/api/sensors/{id}/readings?hours=24</code></td>
      <td><code>sensors.get_readings</code></td>
      <td><code>SensorReading.timestamp >= since</code></td>
      <td><code>SensorChart</code> & <code>DashboardStats</code></td>
    </tr>
    <tr>
      <td><code>fetchAnomalies()</code></td>
      <td>GET</td>
      <td><code>/api/anomalies?station_id=&limit=</code></td>
      <td><code>anomalies.list_anomalies</code></td>
      <td><code>db.query(Anomaly).filter(...)</code></td>
      <td><code>AnomalyFeed</code> & <code>StationSidebar</code></td>
    </tr>
    <tr>
      <td><code>fetchExplanation()</code></td>
      <td>GET</td>
      <td><code>/api/anomalies/{id}/explain</code></td>
      <td><code>anomalies.get_explanation</code></td>
      <td>Retrieves or commits cached text</td>
      <td><code>AnomalyCard</code> (expanded view)</td>
    </tr>
    <tr>
      <td><em>External Sensor</em></td>
      <td>POST</td>
      <td><code>/api/sensors/ingest</code></td>
      <td><code>sensors.ingest_reading</code></td>
      <td>Evaluates ML and commits reading</td>
      <td>Ingestion stream</td>
    </tr>
    <tr>
      <td><em>Health Probe</em></td>
      <td>GET</td>
      <td><code>/health</code></td>
      <td><code>main.health</code></td>
      <td>None</td>
      <td>DevOps uptime check</td>
    </tr>
  </tbody>
</table>

<!-- PART 8 & 9 & 10 -->
<h1 class="section-break">PARTS 8, 9 & 10 &mdash; BACKEND, DATA FLOW & DASHBOARD GUIDE</h1>

<h2>8.1 Backend Router Structure</h2>
<ul>
  <li><code>routers/stations.py</code>: Formats database station rows into frontend-compatible objects (<code>id</code> = station code, <code>name</code>, <code>location</code>).</li>
  <li><code>routers/sensors.py</code>: Handles time-series retrieval filtered by timestamp window, plus <code>/ingest</code> which loads the station's pre-trained Isolation Forest model, runs live inference via <code>detect_single()</code>, and persists both the reading and any triggered anomaly.</li>
  <li><code>routers/anomalies.py</code>: Returns flagged anomalies ordered by timestamp descending, and provides the <code>/explain</code> endpoint with smart caching logic.</li>
</ul>

<h2>9.1 End-to-End Telemetry Data Flow</h2>
<div class="flow-box">
1. Generation / Ingestion: Sensor stream generated via simulator.py or received via POST /api/sensors/ingest
2. Feature Preparation: Vector [temperature, humidity, pressure, wind_speed] formatted and forward-filled
3. ML Inference: Scikit-learn Isolation Forest evaluates decision_function() score and predict() (-1 = anomaly)
4. Persistence: Telemetry record committed to SQLite database with is_anomaly flag
5. Anomaly Creation: If anomalous, Z-Score deviation heuristic assigns fault category (spike/drift/missing)
6. Frontend Retrieval: React Query queries /api/sensors/.../readings and /api/anomalies every 15 seconds
7. Rendering: Recharts plots curves and superimposes AnomalyDot; AnomalyFeed populates cards
8. AI Explanation: Clicking card calls /api/anomalies/{id}/explain &rarr; NVIDIA NIM returns diagnosis
</div>

<h2>10.1 Complete Dashboard Walkthrough</h2>
<div class="grid-2">
  <div class="callout">
    <strong>1. Fleet Sidebar (Left)</strong><br>
    Displays AWS-001 (Coimbatore), AWS-002 (Chennai), and AWS-003 (Bengaluru). Shows instant green or orange indicators representing fleet health status.
  </div>
  <div class="callout">
    <strong>2. KPI Summary Bar (Top)</strong><br>
    Shows total packets (557+), anomaly count (50+), uptime percentage (91.0%), and real-time temperature readout (24.8&deg;C).
  </div>
</div>
<div class="grid-2">
  <div class="callout">
    <strong>3. Sensor Visualizer (Center)</strong><br>
    Four synchronized charts plotting diurnal oscillations. Orange dots pinpoint exact moments where spikes or drifts occurred.
  </div>
  <div class="callout">
    <strong>4. Anomaly Feed (Right)</strong><br>
    Clickable alert cards displaying anomaly types. Expanding a card fetches plain-English NVIDIA NIM diagnostics for field technicians.
  </div>
</div>

<!-- PART 11 & 12 -->
<h1 class="section-break">PARTS 11 & 12 &mdash; CALCULATIONS & AI / ML PIPELINE</h1>

<h2>11.1 Key Mathematical Calculations</h2>
<ol>
  <li><strong>Diurnal Weather Simulation:</strong>
    $$\text{temperature}(t) = 25 + 5\sin\left(\frac{t}{24}\cdot 2\pi\right) + \mathcal{N}(0, 0.5)$$
    $$\text{humidity}(t) = 60 + 10\cos\left(\frac{t}{24}\cdot 2\pi\right) + \mathcal{N}(0, 2)$$
    <em>Why:</em> Mathematically enforces real-world physical correlation (temperature rises as humidity falls) so the ML model learns natural environmental cycles.
  </li>
  <li><strong>Isolation Forest Decision Score:</strong>
    Calculated across 200 isolation decision trees. Returns negative float values representing anomaly severity (more negative = more anomalous).
  </li>
  <li><strong>Heuristic Z-Score Classification:</strong>
    $$Z = \frac{|x_{\text{feature}} - \mu_{\text{baseline}}|}{\sigma_{\text{baseline}}}$$
    If worst feature $Z > 4.0 \rightarrow \text{"spike"}$; otherwise $\rightarrow \text{"drift"}$. If wind speed is null $\rightarrow \text{"missing"}$.
  </li>
</ol>

<h2>12.1 NVIDIA NIM Integration Architecture</h2>
<div class="flow-box">
Trigger: User clicks AnomalyCard in UI
   &darr;
Endpoint: GET /api/anomalies/{id}/explain
   &darr;
Cache Verification: If valid explanation already exists in SQLite, return immediately
   &darr;
Prompt Construction: Formats sensor values, detected anomaly type, and anomaly score
   &darr;
NVIDIA NIM API Call:
   - Base URL: https://integrate.api.nvidia.com/v1
   - Model: meta/llama-3.2-11b-vision-instruct
   - Temperature: 0.3 | Max Tokens: 200
   &darr;
Response Processing: Parses diagnostic text (physical cause + technician action)
   &darr;
Persistence: Writes explanation to SQLite Anomaly record (skips caching if error occurred)
   &darr;
Display: Frontend displays explanation text under glowing Sparkles icon
</div>

<!-- PART 13 to 19 -->
<h1 class="section-break">PARTS 13 TO 19 &mdash; SECURITY, RUNTIME & ARCHITECTURE</h1>

<h2>13.1 Security & Authentication</h2>
<ul>
  <li><strong>Authentication:</strong> ❌ Not implemented. Prototype endpoints are open for demo evaluation.</li>
  <li><strong>CORS:</strong> Enabled via FastAPI <code>CORSMiddleware</code> allowing local frontend communication.</li>
  <li><strong>Input Validation:</strong> Enforced by Pydantic schemas (<code>ReadingIn</code>) validating data types on ingest.</li>
  <li><strong>Secrets Management:</strong> API keys (<code>NVIDIA_API_KEY</code>) are managed exclusively through <code>.env</code>.</li>
</ul>

<h2>15.1 Developer Quick-Start Execution Guide</h2>
<div class="grid-2">
  <div class="flow-box">
    <strong>Start Backend:</strong><br>
    <code>cd backend</code><br>
    <code>python -m venv venv</code><br>
    <code>.\venv\Scripts\activate</code><br>
    <code>pip install -r requirements.txt</code><br>
    <code>python scripts/seed_demo_data.py</code><br>
    <code>uvicorn app.main:app --reload --port 8000</code>
  </div>
  <div class="flow-box">
    <strong>Start Frontend:</strong><br>
    <code>cd frontend</code><br>
    <code>npm install</code><br>
    <code>npm run dev</code><br><br>
    <strong>Open in Browser:</strong><br>
    <code>http://localhost:5173</code>
  </div>
</div>

<h2>17.1 Resilience & Error Handling</h2>
<ul>
  <li><strong>NVIDIA Fallback:</strong> If no API key is provided or remote inference fails, a clear fallback message is returned without crashing the server.</li>
  <li><strong>Error Cache Isolation:</strong> Failed API status errors are blocked from persisting in SQLite, ensuring subsequent clicks retry cleanly.</li>
  <li><strong>Frontend Retry:</strong> If an explanation call encounters a network issue, [AnomalyCard.tsx] displays an inline retry button.</li>
  <li><strong>Flexbox Layout Stability:</strong> <code>shrink-0</code> prevents cards from collapsing in flexbox containers.</li>
</ul>

<!-- PART 20 to 25 -->
<h1 class="section-break">PARTS 20 TO 25 &mdash; IMPLEMENTATION AUDIT & DEVELOPER GUIDE</h1>

<h2>20.1 Implementation Audit Matrix</h2>
<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Plan Origin</th>
      <th>Status in Codebase</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>FastAPI 6 Endpoints</td>
      <td>PDF Page 4-5</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
      <td>All endpoints active and verified</td>
    </tr>
    <tr>
      <td>Isolation Forest ML</td>
      <td>PDF Page 6</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
      <td>Trains and saves models to <code>models_store/</code></td>
    </tr>
    <tr>
      <td>Sensor Simulator</td>
      <td>PDF Page 6</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
      <td>Simulates 48h realistic multi-fault telemetry</td>
    </tr>
    <tr>
      <td>NVIDIA NIM Diagnostics</td>
      <td>PDF Page 6</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
      <td>Active with <code>meta/llama-3.2-11b-vision-instruct</code></td>
    </tr>
    <tr>
      <td>Recharts Graphs + Dots</td>
      <td>PDF Page 7</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
      <td>4 charts with orange anomaly markers</td>
    </tr>
    <tr>
      <td>15s Auto-Polling</td>
      <td>PDF Page 9</td>
      <td><span class="badge badge-success">&check; Implemented</span></td>
      <td>React Query polling active in <code>useStationData.ts</code></td>
    </tr>
    <tr>
      <td>Autoencoder Deep Learning</td>
      <td>PDF Page 1</td>
      <td><span class="badge badge-info">&bull; Planned (Cut)</span></td>
      <td>Cut without hesitation for 5-day demo</td>
    </tr>
    <tr>
      <td>Azure Cloud Hosting</td>
      <td>PDF Page 10</td>
      <td><span class="badge badge-info">&bull; Planned (Cut)</span></td>
      <td>Running locally; cloud cut for 5-day plan</td>
    </tr>
  </tbody>
</table>

<h2>24.1 Developer Modification Recipes</h2>
<ul>
  <li><strong>Add a New Station:</strong> Add a dictionary entry to <code>STATIONS</code> in [seed_demo_data.py] and re-run the seed script.</li>
  <li><strong>Change the NVIDIA LLM Model:</strong> Set <code>NVIDIA_MODEL=&lt;model_name&gt;</code> in <code>backend/.env</code>.</li>
  <li><strong>Adjust Anomaly Sensitivity:</strong> Modify <code>contamination=0.05</code> in [detector.py].</li>
</ul>

<!-- PART 26 to 34 -->
<h1 class="section-break">PARTS 26 TO 34 &mdash; HACKATHON PRESENTATION & JUDGES' Q&A</h1>

<h2>26.1 30-Second Elevator Pitch</h2>
<p><em>"India relies on thousands of remote Automatic Weather Stations for critical monsoon and disaster forecasting, but sensor degradation often goes undetected for weeks. Mavericks is an intelligent monitoring platform that uses unsupervised Machine Learning to catch multi-sensor faults in real time and NVIDIA AI to generate instant, plain-English diagnostics and corrective field actions for ground technicians."</em></p>

<h2>26.2 1-Minute Demonstration Pitch</h2>
<p><em>"Weather forecasts are only as reliable as ground sensor telemetry. In remote terrains, weather sensors silently suffer calibration drift, flatlines, or electrical spikes&mdash;corrupting climate models. Mavericks solves this with an end-to-end mission control dashboard. Our backend trains an Isolation Forest model per station to catch coupled multi-sensor anomalies across temperature, humidity, pressure, and wind speed. When an anomaly is detected, clicking any alert invokes our NVIDIA NIM AI diagnostic copilot, which translates complex multi-sensor deviations into plain English, explaining the physical root cause and telling the field technician exactly what tools and actions are needed."</em></p>

<h2>28.1 Anticipated Judges' Questions & Answers</h2>
<div class="callout">
  <strong>Q: Why use Isolation Forest instead of simple threshold rules (e.g. Temp > 45&deg;C)?</strong><br>
  <strong>A:</strong> Simple threshold rules fail to detect coupled environmental anomalies. For instance, 28&deg;C is normal at noon, but 28&deg;C at 3:00 AM combined with 15% humidity is physically impossible. Isolation Forest evaluates multi-sensor correlation in multi-dimensional space, isolating anomalies that threshold rules completely miss.
</div>

<div class="callout">
  <strong>Q: Why use NVIDIA NIM instead of standard cloud LLMs?</strong><br>
  <strong>A:</strong> NVIDIA NIM provides high-throughput, enterprise-optimized inference microservices with standard OpenAI-compatible endpoints. It delivers low latency and high reliability without requiring local GPU memory management or vendor lock-in.
</div>

<div class="callout">
  <strong>Q: How does this scale to real AWS hardware in the field?</strong><br>
  <strong>A:</strong> The trained Isolation Forest model is extremely compact (~2.5 MB). It can run directly on edge microcontrollers (e.g. Raspberry Pi or NVIDIA Jetson) deployed at the weather tower, transmitting only flagged incident packets over low-bandwidth cellular/satellite telemetry via our <code>/api/sensors/ingest</code> REST API.
</div>

<h2>30.1 Technical Terms Glossary</h2>
<table>
  <thead>
    <tr>
      <th>Term</th>
      <th>Simple Meaning</th>
      <th>How It Is Used Here</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Automatic Weather Station (AWS)</strong></td>
      <td>Automated ground tower capturing climate data</td>
      <td>Source entity generating telemetry (<code>AWS-001</code>, <code>AWS-002</code>, <code>AWS-003</code>)</td>
    </tr>
    <tr>
      <td><strong>Isolation Forest</strong></td>
      <td>Unsupervised ML algorithm that isolates anomalies</td>
      <td>Evaluates sensor vectors and assigns anomaly scores in <code>detector.py</code></td>
    </tr>
    <tr>
      <td><strong>Diurnal Cycle</strong></td>
      <td>24-hour day/night solar oscillation</td>
      <td>Modeled via sine/cosine waves in <code>simulator.py</code> for realistic baselines</td>
    </tr>
    <tr>
      <td><strong>Z-Score</strong></td>
      <td>Number of standard deviations away from mean</td>
      <td>Used in <code>classify_anomaly_type()</code> to identify spikes versus drifts</td>
    </tr>
    <tr>
      <td><strong>NVIDIA NIM</strong></td>
      <td>NVIDIA Inference Microservice</td>
      <td>Remote LLM engine generating diagnostic technician advice</td>
    </tr>
    <tr>
      <td><strong>Polling</strong></td>
      <td>Automatic background data refresh</td>
      <td>Configured via React Query (15s interval) in <code>useStationData.ts</code></td>
    </tr>
  </tbody>
</table>

<!-- FINAL SECTION -->
<h1 class="section-break">&#9201; IF I HAD TO UNDERSTAND THIS PROJECT IN 10 MINUTES</h1>

<div class="callout callout-success">
  <strong>The 10-Minute Executive Cheat Sheet:</strong>
</div>
<ol>
  <li><strong>The Goal:</strong> Automatically detect weather station sensor failures and give repair crews instant plain-English explanations using AI.</li>
  <li><strong>Where Data Originates:</strong> [simulator.py] generates 48 hours of seasonal telemetry with injected faults; [seed_demo_data.py] trains models and stores data in SQLite (<code>aws_anomaly.db</code>).</li>
  <li><strong>The Machine Learning:</strong> [detector.py] runs Scikit-Learn's <strong>Isolation Forest</strong> across Temperature, Humidity, Pressure, and Wind Speed. Outliers receive negative anomaly decision scores.</li>
  <li><strong>The AI Diagnostic Copilot:</strong> When a user clicks an anomaly card, [nvidia_client.py] sends sensor readouts to <strong>NVIDIA NIM</strong> (<code>meta/llama-3.2-11b-vision-instruct</code>), returning physical causes and corrective actions.</li>
  <li><strong>The Dashboard:</strong> Built with <strong>React 19</strong>, <strong>Tailwind CSS v4</strong>, and <strong>Recharts</strong>. Left sidebar switches stations, center displays 4 sensor graphs with orange anomaly markers, and right displays the expandable AI anomaly feed.</li>
  <li><strong>Demo Readiness:</strong> 100% functional locally on <code>http://localhost:5173</code> (frontend) and <code>http://localhost:8000</code> (backend).</li>
</ol>

</body>
</html>
"""

def generate_pdf():
    # Save HTML to temporary file
    temp_dir = tempfile.mkdtemp()
    html_path = os.path.join(temp_dir, "document.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    target_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "MAVERICKS_PROJECT_DOCUMENTATION.pdf"))
    
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    user_data = tempfile.mkdtemp()
    
    print(f"Launching Edge to render PDF...")
    cmd = [
        edge_path,
        "--headless",
        f"--user-data-dir={user_data}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={target_pdf}",
        html_path
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if os.path.exists(target_pdf):
        print(f"SUCCESS: PDF generated at: {target_pdf}")
        print(f"File size: {os.path.getsize(target_pdf):,} bytes")
    else:
        print("Failed to generate PDF.")
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)

if __name__ == "__main__":
    generate_pdf()
