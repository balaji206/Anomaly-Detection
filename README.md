# Anomaly Detection Platform

A full-stack anomaly detection dashboard for monitoring station/sensor data, identifying abnormal behavior, and presenting anomaly information through a web interface.

The project is organized into a **FastAPI backend** and a **React + TypeScript frontend**. The backend handles data access, anomaly detection/ML processing, station and sensor APIs, and AI-assisted functionality. The frontend consumes the backend APIs and presents the results through a dashboard.

## Project Overview

### Problem

Operational sensor systems can produce large amounts of data, making it difficult for technicians to quickly identify abnormal behavior and understand which stations require attention.

### Solution

This application provides a centralized dashboard where users can:

- View monitored stations.
- View sensor-related information.
- See detected anomalies.
- Inspect anomaly details.
- Visualize sensor information.
- View dashboard-level statistics.
- Use backend anomaly-detection and AI-assisted processing.
- Work with station-specific ML/baseline artifacts.

The architecture is designed so that the frontend is responsible for the user interface while the backend handles APIs, data processing, anomaly detection, and persistence.

---

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- npm
- HTML/CSS
- REST API integration
- Component-based UI architecture

Important frontend areas:

```text
frontend/src/
├── api/
│   └── client.ts
├── components/
│   ├── AnomalyCard.tsx
│   ├── AnomalyFeed.tsx
│   ├── DashboardStats.tsx
│   ├── SensorChart.tsx
│   └── StationSidebar.tsx
├── hooks/
│   └── useStationData.ts
├── types/
│   └── index.ts
├── App.tsx
├── main.tsx
└── index.css
```

### Backend

- Python
- FastAPI
- Uvicorn
- SQLite/local database
- Pydantic schemas
- Machine-learning/anomaly-detection modules
- NVIDIA/AI client integration
- REST APIs

Important backend areas:

```text
backend/
├── app/
│   ├── ai/
│   │   └── nvidia_client.py
│   ├── ml/
│   │   ├── detector.py
│   │   └── simulator.py
│   ├── routers/
│   │   ├── anomalies.py
│   │   ├── sensors.py
│   │   └── stations.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── models_store/
├── scripts/
├── requirements.txt
└── aws_anomaly.db
```

---

# Architecture

The high-level application flow is:

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ React + TypeScript  │
                    │     Frontend        │
                    └──────────┬──────────┘
                               │
                         REST API calls
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌─────────────┐  ┌─────────────┐
       │  Database  │   │ ML/Anomaly  │  │ AI/NVIDIA   │
       │   / Data   │   │ Detection   │  │ Integration │
       └────────────┘   └─────────────┘  └─────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ JSON API Response   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Dashboard / UI      │
                    └─────────────────────┘
```

---

# Repository Structure

```text
Anomaly-Detection/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   └── nvidia_client.py
│   │   ├── ml/
│   │   │   ├── detector.py
│   │   │   └── simulator.py
│   │   ├── routers/
│   │   │   ├── anomalies.py
│   │   │   ├── sensors.py
│   │   │   └── stations.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── models_store/
│   │   ├── station_1.pkl
│   │   ├── station_1_baseline.json
│   │   ├── station_2.pkl
│   │   ├── station_2_baseline.json
│   │   ├── station_3.pkl
│   │   └── station_3_baseline.json
│   │
│   ├── scripts/
│   │   ├── generate_docs_pdf.py
│   │   └── seed_demo_data.py
│   │
│   ├── .env.example
│   ├── requirements.txt
│   ├── README.md
│   └── aws_anomaly.db
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   │   ├── AnomalyCard.tsx
│   │   │   ├── AnomalyFeed.tsx
│   │   │   ├── DashboardStats.tsx
│   │   │   ├── SensorChart.tsx
│   │   │   └── StationSidebar.tsx
│   │   ├── hooks/
│   │   │   └── useStationData.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   │
│   ├── .env.example
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.ts
│
├── MAVERICKS_PROJECT_DOCUMENTATION.pdf
└── .gitignore
```

---

# Prerequisites

Install the following before running the project:

- Git
- Python 3.x
- Node.js and npm

Verify installations:

```bash
git --version
python --version
node --version
npm --version
```

If your system uses `python3` instead of `python`, use `python3` in the commands below.

---

# Getting the Project

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd Anomaly-Detection
```

Repository:

`https://github.com/balaji206/Anomaly-Detection`

---

# Backend Setup

Open a terminal window and navigate to the `backend` folder:

```bash
cd backend
```

### Step 1: Create & Activate Virtual Environment

- **Windows (PowerShell)**:
  ```powershell
  py -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(If execution policy prevents script activation, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*

- **Linux / macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment File

Copy `.env.example` to create your local `.env`:

- **Windows (PowerShell)**:
  ```powershell
  Copy-Item .env.example .env
  ```
- **Linux / macOS**:
  ```bash
  cp .env.example .env
  ```

*(Optionally open `.env` and add your `NVIDIA_API_KEY` for live AI explanations from NVIDIA NIM).*

### Step 4: Seed Demo Data & Train Models

Seed the database with 48 hours of simulated station telemetry and train per-station Isolation Forest models:

```bash
python scripts/seed_demo_data.py
```

### Step 5: Start Backend API Server

```bash
uvicorn app.main:app --reload --port 8000
```

The backend server runs on `http://localhost:8000`.  
Interactive API docs are available at **`http://localhost:8000/docs`**.

---

# Frontend Setup

Open a **second terminal window** and navigate to the `frontend` folder:

```bash
cd frontend
```

### Step 1: Configure Environment File

Copy `.env.example` to create your local `.env`:

- **Windows (PowerShell)**:
  ```powershell
  Copy-Item .env.example .env
  ```
- **Linux / macOS**:
  ```bash
  cp .env.example .env
  ```

*(By default, `VITE_API_BASE_URL` points to `http://localhost:8000`).*

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Start Frontend Development Server

```bash
npm run dev
```

The frontend dashboard will run on **`http://localhost:5173`**. Open this URL in your web browser.

---

# Quick-Start Summary (Running Both Together)

To run the complete application, keep two terminals open:

### Terminal 1 — Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python scripts/seed_demo_data.py
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend
```powershell
cd frontend
npm install
npm run dev
```

The overall flow is:

```text
Browser
   ↓
React/Vite Frontend
   ↓
API Client
   ↓
FastAPI Backend
   ↓
Database / ML / AI
   ↓
Backend Response
   ↓
Frontend State
   ↓
Dashboard UI
```

---

# Main Frontend Components

## AnomalyCard

`frontend/src/components/AnomalyCard.tsx`

Responsible for displaying information about an individual anomaly.

This is also the primary component for anomaly-specific user actions and visual status.

## AnomalyFeed

`frontend/src/components/AnomalyFeed.tsx`

Responsible for displaying the anomaly feed/list and coordinating the anomaly cards.

## DashboardStats

`frontend/src/components/DashboardStats.tsx`

Displays dashboard-level anomaly/statistical information.

## SensorChart

`frontend/src/components/SensorChart.tsx`

Displays sensor-related information visually using charts.

## StationSidebar

`frontend/src/components/StationSidebar.tsx`

Provides station-level navigation/selection.

## useStationData

`frontend/src/hooks/useStationData.ts`

Provides reusable frontend logic for loading/handling station-related data.

## API Client

`frontend/src/api/client.ts`

Central location for frontend-to-backend API communication.

---

# Main Backend Components

## `app/main.py`

Backend application entry point.

Responsible for creating/configuring the FastAPI application and registering the API routers.

## `app/database.py`

Database-related configuration and access.

## `app/models.py`

Database/application models.

## `app/schemas.py`

API data validation/serialization schemas.

## `app/routers/anomalies.py`

Anomaly-related API routes.

## `app/routers/sensors.py`

Sensor-related API routes.

## `app/routers/stations.py`

Station-related API routes.

## `app/ml/detector.py`

Anomaly-detection/ML logic.

## `app/ml/simulator.py`

Simulation/data-generation logic used by the project.

## `app/ai/nvidia_client.py`

AI/NVIDIA integration used by the backend.

---

# Data Flow

The application follows a general data flow similar to:

```text
Data Source
    ↓
Backend
    ↓
Database / ML / AI Processing
    ↓
FastAPI Router
    ↓
REST API Response
    ↓
frontend/src/api/client.ts
    ↓
React State / Hook
    ↓
UI Components
    ↓
Dashboard
```

For example, anomaly information can flow through:

```text
Anomaly data
    ↓
Backend anomaly logic
    ↓
/api anomaly route
    ↓
Frontend API client
    ↓
AnomalyFeed
    ↓
AnomalyCard
    ↓
User
```

---

# Anomaly Resolution Workflow

The planned/implemented demo enhancement is to close the operational loop after an anomaly is detected.

Target workflow:

```text
Anomaly detected
      ↓
AI/ML explanation
      ↓
Anomaly displayed in dashboard
      ↓
Technician reviews anomaly
      ↓
Technician selects "Mark resolved"
      ↓
PATCH /api/anomalies/{id}/resolve
      ↓
Backend updates resolved = true
      ↓
Frontend receives updated state
      ↓
AnomalyCard shows resolved state
```

The existing anomaly model's `resolved` field is intended to represent whether the anomaly has been closed.

If the resolution endpoint has not yet been implemented in the current branch, it should be treated as a pending feature rather than an existing API.

---

# API Structure

Backend API routers are organized by responsibility:

```text
/api/...
├── anomalies
├── sensors
└── stations
```

The exact endpoints and request/response schemas should be checked in:

```text
backend/app/routers/
backend/app/schemas.py
```

The FastAPI Swagger interface can be used during development to inspect the currently registered endpoints:

```text
http://localhost:8000/docs
```

---

# Machine Learning / Anomaly Detection

The backend contains a dedicated ML area:

```text
backend/app/ml/
├── detector.py
└── simulator.py
```

The repository also contains station-specific model/baseline artifacts:

```text
backend/models_store/
├── station_1.pkl
├── station_1_baseline.json
├── station_2.pkl
├── station_2_baseline.json
├── station_3.pkl
└── station_3_baseline.json
```

These files support station-specific anomaly-detection/baseline behavior.

The exact model algorithm and feature-processing pipeline should be treated as implementation details defined by `detector.py` and the associated backend code.

---

# AI Integration

The backend contains:

```text
backend/app/ai/nvidia_client.py
```

This indicates that the application has a dedicated integration layer for NVIDIA/AI functionality.

Any required API credentials should be configured through environment variables and should never be committed to Git.

---

# Security and Environment Variables

Never commit:

```text
.env
.env.local
.env.production
```

The repository includes:

```text
backend/.env.example
frontend/.env.example
```

These files should contain only safe configuration templates.

If an API key or secret is accidentally exposed:

1. Revoke/rotate the credential.
2. Remove it from the working files.
3. Check Git history.
4. Update the local `.env`.
5. Do not reuse the exposed credential.

---

# Development Workflow

Before making a feature change:

```text
1. Pull/fetch the latest code
2. Create a feature branch
3. Understand the existing implementation
4. Make the smallest required change
5. Run backend tests/checks
6. Run frontend checks/build
7. Test the complete frontend → backend flow
8. Review git diff
9. Commit
10. Push the branch
```

Example:

```bash
git checkout -b feature/mark-anomaly-resolved
```

After making changes:

```bash
git status
git diff
```

Then commit:

```bash
git add .
git commit -m "Add anomaly resolution workflow"
git push -u origin feature/mark-anomaly-resolved
```

---

# Important Files for New Contributors

Start with these files:

### Frontend

```text
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/components/AnomalyFeed.tsx
frontend/src/components/AnomalyCard.tsx
frontend/src/hooks/useStationData.ts
frontend/src/types/index.ts
```

### Backend

```text
backend/app/main.py
backend/app/database.py
backend/app/models.py
backend/app/schemas.py
backend/app/routers/anomalies.py
backend/app/routers/sensors.py
backend/app/routers/stations.py
backend/app/ml/detector.py
backend/app/ml/simulator.py
backend/app/ai/nvidia_client.py
```

---

# Troubleshooting

## Backend does not start

Check:

```bash
pip install -r requirements.txt
```

Make sure the virtual environment is active.

Check that the required environment variables exist.

Try:

```bash
uvicorn app.main:app --reload --port 8000
```

from the `backend` directory.

## Frontend does not start

Run:

```bash
npm install
npm run dev
```

Check that Node.js is installed.

## Frontend cannot reach backend

Check:

1. Backend is running.
2. Backend is listening on the expected port.
3. Frontend `.env` has the correct API URL.
4. `frontend/src/api/client.ts` uses the expected API configuration.
5. Browser developer tools for network/API errors.
6. Backend terminal for request/error logs.

## Dashboard has no data

Check:

1. Backend is running.
2. Database exists/configuration is correct.
3. Required demo data has been seeded if necessary.
4. API endpoints return data.
5. Frontend API requests succeed.
6. Browser console/network tab for errors.

---

# Project Documentation

The repository also contains:

```text
MAVERICKS_PROJECT_DOCUMENTATION.pdf
```

This document provides additional project information, architecture/context, implementation details, and onboarding information.

---

# Current Demo Goal

The main demonstration story is:

```text
Monitor
   ↓
Detect anomaly
   ↓
Explain anomaly
   ↓
Display anomaly on dashboard
   ↓
Technician reviews it
   ↓
Technician takes action
   ↓
Mark anomaly as resolved
```

The important product idea is not only detecting an anomaly, but helping the technician move from **detection to action**.

---

# Future Enhancements

Potential next steps include:

- Resolution notes.
- Resolved-by technician information.
- Resolution timestamps.
- Resolution history/audit trail.
- Resolved/unresolved filters.
- "Resolved today" dashboard statistics.
- More detailed anomaly explanations.
- Improved model monitoring.
- Authentication and role-based access.
- Production database deployment.
- Cloud deployment.
- Automated testing and CI/CD.

---

# Team Development Notes

When modifying the project:

- Reuse existing components and utilities.
- Reuse the existing API client.
- Follow the existing backend router structure.
- Do not duplicate API logic unnecessarily.
- Do not hardcode credentials.
- Do not commit `.env` files.
- Keep frontend and backend responsibilities separate.
- Test API changes from both the backend and frontend.
- Verify that dashboard data still works after backend changes.

---

# License

This project is currently intended as a hackathon/demo project. Add an appropriate open-source license here if the team decides to distribute the project under one.
