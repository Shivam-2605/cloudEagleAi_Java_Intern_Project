# GitHub Organization Access Report Service

A high-performance auditing tool built with Python (FastAPI + Flask) designed to generate structured access reports for large GitHub organizations. This service efficiently maps "Who has access to which repositories" and is architected to scale to 100+ repositories and 1000+ users using asynchronous I/O.

## Table of Contents

- [Tech Stack](#-tech-stack)
- [How to Run](#-how-to-run)
- [Authentication Configuration](#-authentication-configuration)
- [How to Call the API](#-how-to-call-the-api)
- [Project Architecture](#-project-architecture)
- [Design Decisions & Assumptions](#-design-decisions--assumptions)

---

## Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Backend API | FastAPI | High-concurrency async REST API |
| Frontend UI | Flask | Lightweight server for the dashboard |
| Async Runtime | asyncio | Concurrent processing using Semaphores |
| HTTP Client | httpx | Asynchronous GitHub API communication |
| Data Validation | Pydantic v2 | Strict request/response schema validation |

---

## How to Run

### 1. Prerequisites

- Python 3.11 or higher
- A GitHub Personal Access Token (PAT)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/github-access-report.git
cd github-access-report

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
GITHUB_TOKEN=ghp_your_token_here
FASTAPI_PORT=8000
FLASK_PORT=5000
CONCURRENCY_LIMIT=10
```

### 4. Start the Application

You will need two terminal windows:

**Terminal 1 (Backend API):**

```bash
python3 -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend Dashboard):**

```bash
python3 frontend/flask_app.py
```

Open your browser to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Authentication Configuration

This application uses a GitHub Personal Access Token (Classic) for secure communication with the GitHub REST API.

1. Navigate to **GitHub Settings > Developer Settings > Personal Access Tokens > Tokens (classic)**.
2. Click **"Generate new token"**.
3. Select the following scopes:
   - `repo` — Required to access private repositories and list collaborators.
   - `read:org` — Required to read organization membership.
4. Copy the token and paste it into the `GITHUB_TOKEN` variable in your `.env` file.

---

## How to Call the API

While the dashboard provides a visual interface, you can call the API directly:

### Generate Full Report

```
GET /api/v1/report/{org}
```

**Example via cURL:**

```bash
curl http://127.0.0.1:8000/api/v1/report/google
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `include_private` | bool | `false` | If `true`, fetches private repos (requires a token with `repo` scope). |

### Health Check

```
GET /health
```

---

## Project Architecture

The project follows a modular, clean-code organization:

```
github-access-report/
├── app/                      # Backend (FastAPI)
│   ├── api/                  # API Routes (Endpoints)
│   ├── services/             # Core Business Logic (Report Generation)
│   ├── github/               # Async GitHub HTTP Client
│   ├── schemas/              # Pydantic Data Models (Report Shapes)
│   ├── middleware/           # Request Logger & Error Handlers
│   └── utils/                # Concurrency Helpers (Semaphores)
├── frontend/                 # Frontend (Flask)
│   ├── templates/            # HTML Dashboard
│   └── static/               # JS Logic (Fetch/Render) & CSS
├── .env                      # Secrets & Config
└── requirements.txt          # Dependencies
```

---

## Design Decisions & Assumptions

### 1. Handling Scale with Asynchronous Concurrency

To meet the requirement of 100+ repositories, sequential API calls would result in a very poor user experience.

**Decision:** Implemented Bounded Async Concurrency.

**Implementation:** Using `asyncio.gather` combined with an `asyncio.Semaphore`, the service fetches collaborators for 10 repositories simultaneously. This drastically reduces the time to generate a large report while protecting against GitHub's secondary rate limits.

### 2. Dual-Server Architecture

**Decision:** Separate FastAPI (Port 8000) and Flask (Port 5000).

**Reason:** FastAPI is optimized for high-performance, non-blocking I/O tasks. Flask is used simply as a static file host for the UI. This separation allows the backend to be scaled or deployed as a microservice independently of the dashboard.

### 3. Aggregation Strategy

GitHub's API provides data per-repository. To provide a "User-Centric" view, I implemented a re-indexing service that traverses repository data and aggregates it into a `by_user` map. This allows the frontend to toggle views instantly without secondary API calls.

### 4. Robust Error Handling

**Decision:** Global Exception Middleware.

**Reason:** Even if the GitHub API fails for a single repository (e.g., due to missing permissions), the middleware and service-level safety checks ensure the entire report doesn't crash, returning partial data with a warning instead.

### 5. Assumptions

- **Permissions:** It is assumed the provided `GITHUB_TOKEN` belongs to a user with Admin access to the organization's repositories. GitHub requires admin permissions to list repository collaborators.
- **Environment:** The app assumes it is running in a trusted internal environment; thus, it utilizes a server-side `.env` token rather than per-user OAuth.

---

## Final Checklist for Your Public Repo

- [ ] **Full Source Code:** Ensure all files (`app/`, `frontend/`, `requirements.txt`, etc.) are uploaded.
- [ ] **Clean Code:** Remove any hardcoded tokens or secrets.
- [ ] **`.gitignore`:** Ensure `.env` and `venv/` are listed so you don't leak your token.
- [ ] **README:** This file is ready to go!
