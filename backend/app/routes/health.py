from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile, HealthReading
from ..schemas.health import HealthReadingCreate, HealthReadingResponse
from ..services.health_service import save_health
router=APIRouter(prefix="/api/health",tags=["Health"])
@router.post("/readings",response_model=HealthReadingResponse,status_code=201)
def create(body:HealthReadingCreate,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return save_health(db,patient.id,body.model_dump())
@router.get("/latest",response_model=HealthReadingResponse|None)
def latest(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return db.scalar(select(HealthReading).where(HealthReading.patient_id==patient.id).order_by(HealthReading.timestamp.desc()))
@router.get("/history",response_model=list[HealthReadingResponse])
def history(limit:int=Query(100,ge=1,le=1000),start_date:datetime|None=None,end_date:datetime|None=None,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    stmt=select(HealthReading).where(HealthReading.patient_id==patient.id)
    if start_date: stmt=stmt.where(HealthReading.timestamp>=start_date)
    if end_date: stmt=stmt.where(HealthReading.timestamp<=end_date)
    return db.scalars(stmt.order_by(HealthReading.timestamp.desc()).limit(limit)).all()
