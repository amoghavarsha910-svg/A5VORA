from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile
from ..services.dashboard_service import dashboard
router=APIRouter(prefix="/api",tags=["Dashboard"])
@router.get("/dashboard")
def get_dashboard(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return dashboard(db,patient)
