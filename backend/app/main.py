from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import client
from app.routes.task_routes import router as task_router
from app.routes.ai_routes import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.admin.command("ping")
        print("✅ Connected to MongoDB")
    except Exception as e:
        print("❌ MongoDB Connection Failed")
        print(e)

    yield

    client.close()


app = FastAPI(
    title="Deadline Guardian API",
    lifespan=lifespan
)

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(ai_router)


@app.get("/")
def home():
    return {
        "message": "Deadline Guardian API is running!"
    }