from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base,engine
from . import models
from .routes import auth,patients,health,environment,risk,alerts,recommendations,emergency,dashboard,reports,device
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Personal Health Companion Backend",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_origin],allow_credentials=True,allow_methods=["GET","POST","PUT","OPTIONS"],allow_headers=["Authorization","Content-Type"])
for router in (auth.router,patients.router,health.router,environment.router,risk.router,alerts.router,recommendations.router,emergency.router,dashboard.router,reports.router,device.router): app.include_router(router)
@app.get("/",tags=["System"])
def root(): return {"message":"Personal Health Companion Backend is running"}
@app.get("/health",tags=["System"])
def health_check(): return {"status":"ok"}
