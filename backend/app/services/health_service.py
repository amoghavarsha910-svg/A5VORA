from sqlalchemy.orm import Session
from ..models import HealthReading, EnvironmentReading
from .risk_service import assess
def save_health(db:Session, patient_id:int, values:dict):
    row=HealthReading(patient_id=patient_id,**values); db.add(row); db.flush(); assess(db,patient_id,row,None); db.commit(); db.refresh(row); return row
def save_environment(db:Session, patient_id:int, values:dict):
    row=EnvironmentReading(patient_id=patient_id,**values); db.add(row); db.flush(); assess(db,patient_id,None,row); db.commit(); db.refresh(row); return row
