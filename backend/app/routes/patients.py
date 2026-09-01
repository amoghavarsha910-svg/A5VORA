from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile
from ..schemas.patient import PatientUpdate, PatientResponse
router=APIRouter(prefix="/api/patients",tags=["Patients"])
@router.get("/me",response_model=PatientResponse)
def me(patient:PatientProfile=Depends(get_current_patient)): return patient
@router.put("/me",response_model=PatientResponse)
def update(body:PatientUpdate,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    for key,value in body.model_dump(exclude_unset=True).items(): setattr(patient,key,value)
    db.commit(); db.refresh(patient); return patient
