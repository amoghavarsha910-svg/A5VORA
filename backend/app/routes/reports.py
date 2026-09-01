from fastapi import APIRouter,Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile
from ..services.report_service import csv_report,pdf_report
router=APIRouter(prefix="/api/reports",tags=["Reports"])
@router.get("/csv")
def csv(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    return Response(csv_report(db,patient.id),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=health-history.csv"})
@router.get("/pdf")
def pdf(patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    return Response(pdf_report(db,patient),media_type="application/pdf",headers={"Content-Disposition":"attachment; filename=health-report.pdf"})
