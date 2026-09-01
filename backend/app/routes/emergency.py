from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile,EmergencyEvent
from ..schemas.emergency import SOSCreate,EmergencyResponse
router=APIRouter(prefix="/api/emergency",tags=["Emergency"])
@router.post("/sos",response_model=EmergencyResponse,status_code=status.HTTP_201_CREATED)
def sos(body:SOSCreate,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    event=EmergencyEvent(patient_id=patient.id,**body.model_dump()); db.add(event); db.commit(); db.refresh(event); return event
