from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile,Recommendation
from ..schemas.recommendation import RecommendationResponse
router=APIRouter(prefix="/api/recommendations",tags=["Recommendations"])
@router.get("",response_model=list[RecommendationResponse])
def list_recommendations(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)): return db.scalars(select(Recommendation).where(Recommendation.patient_id==patient.id).order_by(Recommendation.created_at.desc())).all()
