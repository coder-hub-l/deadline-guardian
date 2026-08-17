# Deadline Guardian — AI Task & Completion Risk Estimator

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb)
![Gemini](https://img.shields.io/badge/Gemini%20API-AI%20Risk%20Analysis-orange)
![React](https://img.shields.io/badge/React-18-cyan?logo=react)
![License](https://img.shields.io/badge/License-MIT-yellow)

An **AI-driven task management backend** that uses Google Gemini to analyze every task on creation — returning structured priority scores, completion probability estimates, and plain-language risk assessments. Built with per-user MongoDB isolation, Argon2 password hashing, and strict 3-tier architecture.

## Architecture

```
React Frontend
      │ REST (JWT Bearer)
      ▼
┌────────────────────────────────────────────┐
│             FastAPI Backend                 │
│                                             │
│  Routes (HTTP only, no business logic)     │
│       │                                     │
│  Services (business logic, Gemini calls)   │
│       │                                     │
│  Database Layer (MongoDB, per-user scope)  │
└────────────────────────────────────────────┘
         │                    │
    MongoDB Atlas         Gemini API
  (per-user isolation)  (risk analysis)
```

## Features

| Feature | Details |
|---|---|
| **AI Risk Analysis** | Gemini analyzes each task: priority score, completion %, risk narrative |
| **Security** | Argon2id password hashing (OWASP recommended), JWT auth |
| **Isolation** | Per-user MongoDB collections — no data leakage between users |
| **3-Tier Arch** | Routes → Services → Database — strict layer enforcement |
| **OWASP Compliance** | Argon2 hashing, token expiry, input validation via Pydantic |

## Quick Start

```bash
git clone https://github.com/coder-hub-l/deadline-guardian.git
cd deadline-guardian/backend

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your MongoDB URI and Gemini API key

uvicorn app.main:app --reload --port 8000
```

- Swagger Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## Environment Variables

```env
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
DATABASE_NAME=deadline_guardian
SECRET_KEY=your-jwt-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
GEMINI_API_KEY=your-gemini-api-key
```

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/auth/signup` | POST | Register a new user |
| `/auth/login` | POST | Login and receive JWT |
| `/tasks/` | GET | List all tasks for authenticated user |
| `/tasks/` | POST | Create task (triggers Gemini risk analysis) |
| `/tasks/{id}` | PATCH | Update task |
| `/tasks/{id}` | DELETE | Delete task |
| `/health` | GET | Health check |

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Motor (async MongoDB)
- **Database**: MongoDB Atlas (free tier)
- **Auth**: JWT (PyJWT), Argon2id password hashing
- **AI**: Google Gemini API
- **Frontend**: React 18, Vite
