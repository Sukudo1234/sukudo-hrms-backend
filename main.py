from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import users, auth
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables (or use Alembic migrations instead)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Add cleanup code here if needed


app = FastAPI(
    title="HRMS AttendX Backend",
    description="HRMS Backend API with JWT Authentication",
    version="0.1.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "HRMS AttendX Backend API", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
