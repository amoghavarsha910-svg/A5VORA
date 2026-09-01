from fastapi import APIRouter,Depends,Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile,HealthReading,EnvironmentReading,RiskAssessment
from ..schemas.risk import RiskResponse
from ..services.risk_service import assess
router=APIRouter(prefix="/api/risk",tags=["Risk"])
@router.get("/latest",response_model=RiskResponse|None)
def latest(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    health=db.scalar(select(HealthReading).where(HealthReading.patient_id==patient.id).order_by(HealthReading.timestamp.desc()))
    environment=db.scalar(select(EnvironmentReading).where(EnvironmentReading.patient_id==patient.id).order_by(EnvironmentReading.timestamp.desc()))
    assessment=db.scalar(select(RiskAssessment).where(RiskAssessment.patient_id==patient.id).order_by(RiskAssessment.timestamp.desc()))
    if not health and not environment: return None
    source_timestamp=max(row.timestamp for row in (health,environment) if row is not None)
    needs_combined_assessment=(assessment is None or assessment.timestamp < source_timestamp or (health is not None and environment is not None and assessment.confidence < 0.8))
    if needs_combined_assessment:
        assessment=assess(db,patient.id,health,environment)
        db.commit()
        db.refresh(assessment)
    return assessment
@router.get("/history",response_model=list[RiskResponse])
def history(limit:int=Query(100,ge=1,le=1000),patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return db.scalars(select(RiskAssessment).where(RiskAssessment.patient_id==patient.id).order_by(RiskAssessment.timestamp.desc()).limit(limit)).all()
