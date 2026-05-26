from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, logs, goals, analytics, insights, export, settings, admin

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Health Tracker API",
    description="AI-Powered Personal Health Tracker Dashboard",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(logs.router)
app.include_router(goals.router)
app.include_router(analytics.router)
app.include_router(insights.router)
app.include_router(export.router)
app.include_router(settings.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Personal Health Tracker API", "version": "1.0.0", "docs": "/docs"}
