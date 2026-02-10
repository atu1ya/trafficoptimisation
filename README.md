# perth-greenwave

## 1) Elevator pitch
**perth-greenwave** is a portfolio-grade intelligent traffic control demo for Perth, WA. It turns OpenStreetMap data into a SUMO-ready network and provides a web app where users choose a start/end trip, pick demand scenarios, and compare fixed-time control versus adaptive control (Max Pressure + Green Wave). The key design principle is network-wide optimisation: we improve outcomes for all traffic, not only the highlighted route.

This demonstrates:
- Transport simulation engineering (OSM -> SUMO pipeline)
- Real-time systems (REST + WebSocket streaming)
- Control algorithms with explainability
- Fair A/B benchmarking with deterministic seeds
- Deployable full-stack architecture

---
## 2) Demo walkthrough
1. Open the SPA (`http://localhost:5173` in Docker mode).
2. Select start and end points (lat/lon inputs represent map click flow; backend also provides route matching endpoint).
3. Choose a scenario:
   - Night (baseline)
   - Off peak morning
   - Afternoon medium
   - Peak rush hour
   - Incident mode
4. Choose controller:
   - Night Fixed Plan
   - Scenario Fixed Plan
   - Max Pressure
   - Green Wave
5. Toggle **Compare baseline vs optimised**.
6. Run simulation and watch live metrics streamed over WebSocket.
7. Inspect before/after metrics and explainability narrative showing top intersections that reduced queue pressure.

---
## 3) System architecture
```
+-------------------+      REST/WS      +---------------------+
| React SPA         | <---------------> | FastAPI Backend     |
| - scenario UI     |                   | - API + websocket   |
| - controls + live |                   | - controller engine |
| - charts/summary  |                   | - explainability    |
+-------------------+                   +----------+----------+
                                                   |
                                                   | subprocess / data I/O
                                                   v
                                         +---------+----------+
                                         | SUMO toolchain     |
                                         | - netconvert       |
                                         | - TraCI-ready net  |
                                         +---------+----------+
                                                   |
                                                   v
                                         +---------+----------+
                                         | Cached networks    |
                                         | backend/data/...   |
                                         +--------------------+
```

- Frontend is SPA (Vite + React).
- Backend exposes REST (`/api/...`) and WS (`/ws/simulate`).
- Network build script downloads OSM from Overpass and calls `netconvert`.

---
## 4) Methods
### OSM -> SUMO and caching
- Bounding box defaults to:
  - South `-32.120`
  - North `-31.920`
  - West `115.740`
  - East `116.050`
- This covers Canning Vale, Rossmoyne, Willetton, Bicton, Mosman Park, Nedlands, and Churchlands.
- Script: `backend/scripts/build_network.py`
- Cache key = hash of bbox/options. Outputs under `backend/data/networks/<key>/`.

### Demand generation + scenario params
Scenario model includes explicit knobs:
- Demand intensity
- Speed compliance mean/std
- Accel/decel
- Driver imperfection
- Fixed cycle and arterial split assumptions

### Baseline signal timing model
- Baseline: **Night Fixed Plan** with realistic cycle and split.
- Scenario fixed plan scales cycle/split by scenario demand.

### Controllers
#### Fixed Plan
Cycle-based deterministic split.

#### Max Pressure
Queue pressure control with minimum green hold:
```text
for each intersection:
  if current phase elapsed < min_green: keep phase
  else:
    pressure_ns = queue_ns
    pressure_ew = queue_ew
    choose larger pressure direction
```

#### Green Wave
- Corridor intersections assigned progressive offsets.
- Target speed represented through offset progression.
- Limited adaptivity: if cross-street imbalance high, temporarily break wave.

### Explainability method
- Every control action logs queue reduction estimate.
- Intersections ranked by cumulative queue reduction.
- Narrative generated from top contributors.

---
## 5) Metrics and evaluation
Primary network metrics:
- Delay (s)
- Travel time (s)
- Throughput (vehicles)
- Stops
- Queue length

Secondary route metrics:
- Selected-route travel time/delay
- Ideal physics baseline (free flow with accel constraints, no signal stops)

### A/B fairness
Compare mode uses the same:
- random seed
- demand profile
- simulation horizon

Only controller policy changes.

---
## 6) Benchmarks
- Google Directions supported **only** when `GOOGLE_MAPS_API_KEY` exists.
- No scraping.
- If absent/unavailable, backend reports unavailable and UI falls back to simulation + ideal physics baseline.

---
## 7) How to run
## A) Docker (single command path)
### Prerequisites
- Docker + Docker Compose

### Commands
```bash
cp .env.example .env  # optional
docker compose up --build
```

### URLs
- Frontend: `http://localhost:5173`
- Backend OpenAPI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## B) Local non-Docker
### macOS
1. Install SUMO (1.20+ recommended):
   ```bash
   brew install sumo
   ```
2. Install Python 3.11 and Node 20.
3. Backend:
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt pydantic-settings
   PYTHONPATH=backend uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
5. Build network:
   ```bash
   PYTHONPATH=backend python backend/scripts/build_network.py
   ```

### Windows (PowerShell)
1. Install SUMO from official installer (1.20+).
2. Install Python 3.11 and Node 20.
3. Backend:
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r backend\requirements.txt pydantic-settings
   $env:PYTHONPATH="backend"
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Frontend:
   ```powershell
   cd frontend
   npm install
   npm run dev
   ```
5. Build network:
   ```powershell
   $env:PYTHONPATH="backend"
   python backend\scripts\build_network.py
   ```

### Troubleshooting
- `netconvert not found`: ensure SUMO/bin on PATH.
- Overpass timeout: retry or reduce bbox for local debugging.
- CORS/WS issues: ensure frontend uses backend URL.

---
## 8) Deployment guide
## Option 1: Render + Cloudflare Pages (or Netlify/Vercel)
### Backend on Render
- Create Web Service from repo.
- Build command:
  ```bash
  pip install -r backend/requirements.txt pydantic-settings
  ```
- Start command:
  ```bash
  PYTHONPATH=backend uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- Health check: `/health`
- Persistent disk mount for `backend/data/networks`
- Set env vars listed below.

### Frontend on Pages/Netlify/Vercel
- Build command: `npm run build`
- Publish dir: `dist`
- Set `VITE_API_BASE=https://<backend-domain>`

### HTTPS + domain
- Attach custom domain in provider dashboard.
- Enforce HTTPS redirects.

## Option 2: Single Ubuntu VM + Docker Compose + reverse proxy
1. Provision VM (4 vCPU, 8GB RAM recommended).
2. Install Docker + Compose plugin.
3. Clone repo and run:
   ```bash
   docker compose up -d --build
   ```
4. Place `deployment/Caddyfile` and run Caddy container (or system package).
5. Configure DNS A record to VM.
6. Caddy obtains Let's Encrypt certificates automatically.
7. Persist cache volume:
   - bind mount `./backend/data/networks` to durable disk.

### Scaling notes
- SUMO-heavy workloads should be queued as jobs.
- Restrict max simulation length per request.
- Pre-build common bbox networks.

---
## 9) Reproducibility and configuration
| Env var | Default | Used by |
|---|---:|---|
| `OSM_BBOX_SOUTH` | `-32.120` | network build + backend settings |
| `OSM_BBOX_NORTH` | `-31.920` | network build + backend settings |
| `OSM_BBOX_WEST` | `115.740` | network build + backend settings |
| `OSM_BBOX_EAST` | `116.050` | network build + backend settings |
| `GOOGLE_MAPS_API_KEY` | unset | optional benchmark endpoint |
| `VITE_API_BASE` | `http://localhost:8000` | frontend API base |

---
## 10) Limitations and future work
- Integrate real WA signal timing and detector data.
- Calibrate against loop detector counts and travel-time probes.
- Extend to MPC or RL policy optimisation.
- Scale to metro-wide network using partitioning, batched sim workers, and async job orchestration.

---
## Repository layout
- `backend/app`: API, controllers, services, models
- `backend/scripts/build_network.py`: OSM -> SUMO build pipeline
- `backend/scripts/run_demo.py`: quick CLI sanity runner
- `frontend`: SPA
- `deployment`: Caddy/Nginx/systemd examples
- `Makefile`: setup/run/test/build targets
