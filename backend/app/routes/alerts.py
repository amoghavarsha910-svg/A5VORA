from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile,Alert,AlertStatus
from ..schemas.alert import AlertResponse
router=APIRouter(prefix="/api/alerts",tags=["Alerts"])
@router.get("",response_model=list[AlertResponse])
def list_alerts(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return db.scalars(select(Alert).where(Alert.patient_id==patient.id).order_by(Alert.created_at.desc())).all()
@router.post("/{alert_id}/resolve",response_model=AlertResponse)
def resolve(alert_id:int,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    alert=db.get(Alert,alert_id)
    if not alert or alert.patient_id!=patient.id: raise HTTPException(404,"Alert not found")
    alert.status=AlertStatus.RESOLVED; alert.resolved_at=datetime.utcnow(); db.commit(); db.refresh(alert); return alert
