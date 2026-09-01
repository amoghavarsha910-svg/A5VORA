from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile, EnvironmentReading
from ..schemas.environment import EnvironmentReadingCreate, EnvironmentReadingResponse
from ..services.health_service import save_environment
router=APIRouter(prefix="/api/environment",tags=["Environment"])
@router.post("/readings",response_model=EnvironmentReadingResponse,status_code=201)
def create(body:EnvironmentReadingCreate,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return save_environment(db,patient.id,body.model_dump())
@router.get("/latest",response_model=EnvironmentReadingResponse|None)
def latest(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return db.scalar(select(EnvironmentReading).where(EnvironmentReading.patient_id==patient.id).order_by(EnvironmentReading.timestamp.desc()))
@router.get("/history",response_model=list[EnvironmentReadingResponse])
def history(limit:int=Query(100,ge=1,le=1000),start_date:datetime|None=None,end_date:datetime|None=None,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    stmt=select(EnvironmentReading).where(EnvironmentReading.patient_id==patient.id)
    if start_date: stmt=stmt.where(EnvironmentReading.timestamp>=start_date)
    if end_date: stmt=stmt.where(EnvironmentReading.timestamp<=end_date)
    return db.scalars(stmt.order_by(EnvironmentReading.timestamp.desc()).limit(limit)).all()
