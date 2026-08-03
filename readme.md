Deadline Guardian

A task manager that uses AI to score deadline urgency, estimate completion risk, and tell you what you're actually likely to miss — not just a to-do list with due dates.

 Live demo: [add link once deployed] 
 
 Screenshot/GIF: [add once frontend is live]

Tech Stack

Backend: FastAPI, MongoDB (Motor — async driver), JWT (PyJWT), pwdlib (Argon2 password hashing), Gemini API Frontend: React Deploy: [fill in once deployed — e.g. Render/Railway (backend), Vercel/Netlify (frontend)]

Key Features
Per-user task isolation, enforced at the database layer. Every task read, update, and delete query is scoped by user_id derived from the authenticated JWT — not just hidden in the UI. One user can never read or modify another user's tasks, even by guessing an ID.
AI-driven urgency scoring. Each task is sent to Gemini on creation, which returns a structured priority score, urgency label, difficulty estimate, completion probability, recommended start time, and a plain-language risk assessment — merged directly into the stored task.
Stateless JWT authentication with Argon2 password hashing (via pwdlib), following OWASP's current recommendation over older algorithms like bcrypt-only or SHA-based hashing.
Clean separation between client-writable and server-owned fields. Task ownership, timestamps, and AI-derived fields can never be set or overwritten by the client — the API schemas simply don't expose them as input, so there's nothing to override.
Fail-fast configuration. Missing required environment variables crash the app at startup with a clear error, instead of surfacing as a cryptic failure on the first request that needs them.
Architecture
Client → Routes (auth + request validation only)
       → Services (business logic + MongoDB access)
       → MongoDB

Routes never touch the database directly, and services never import anything from FastAPI (no Depends, no HTTPException). This keeps business logic testable independent of the web framework, and keeps each layer responsible for exactly one thing: routes authenticate and validate, services decide what happens, MongoDB stores it.

app/
├── auth/          # password hashing, JWT creation/verification, get_current_user dependency
├── database/      # Motor client + database handle
├── models/        # MongoDB collection references
├── routes/        # FastAPI route handlers — auth, tasks, ai
├── schemas/       # Pydantic request/response models
├── services/      # business logic, ownership checks, MongoDB queries
└── ai/            # Gemini integration
Setup
bash
git clone <repo-url>
cd <repo-name>

pip install -r requirements.txt --break-system-packages   # or use a virtualenv

cp .env.example .env
# fill in: MONGO_URI, DATABASE_NAME, SECRET_KEY, ALGORITHM,
#          ACCESS_TOKEN_EXPIRE_MINUTES, GEMINI_API_KEY

uvicorn app.main:app --reload

The API will be running at http://127.0.0.1:8000. Interactive docs (Swagger UI) are auto-generated at http://127.0.0.1:8000/docs.

API Overview
Method	Path	Auth required	Description
POST	/auth/register	No	Create a new user account
POST	/auth/login	No	Authenticate and receive a JWT
POST	/tasks	Yes	Create a task (runs Gemini analysis)
GET	/tasks	Yes	List all tasks belonging to the user
GET	/tasks/{id}	Yes	Get a single task (owner-only)
PUT	/tasks/{id}	Yes	Partially update a task (owner-only)
DELETE	/tasks/{id}	Yes	Delete a task (owner-only)
POST	/ai/test	Yes	Run Gemini analysis on a task payload without saving it

Full request/response schemas are available in /docs once the server is running — this table is intentionally just an index, not a duplicate of the OpenAPI spec.

Auth uses a bearer token: Authorization: Bearer <access_token> on every protected route.

Known Limitations
No refresh tokens — access tokens simply expire and require re-login. Fine for a demo, would need a refresh-token flow before production use.
No rate limiting on /auth/login or /auth/register yet — brute-force protection is a known gap.
No account deactivation flow (the is_active check exists in the auth dependency, but nothing currently sets it to false).
Frontend does not yet persist JWTs securely or protect its own API calls — in progress.