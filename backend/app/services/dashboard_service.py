from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import HealthReading,EnvironmentReading,RiskAssessment,Alert,Recommendation,PatientProfile
def dashboard(db:Session,patient:PatientProfile):
    h=db.scalar(select(HealthReading).where(HealthReading.patient_id==patient.id).order_by(HealthReading.timestamp.desc()))
    e=db.scalar(select(EnvironmentReading).where(EnvironmentReading.patient_id==patient.id).order_by(EnvironmentReading.timestamp.desc()))
    r=db.scalar(select(RiskAssessment).where(RiskAssessment.patient_id==patient.id).order_by(RiskAssessment.timestamp.desc()))
    alerts=db.scalars(select(Alert).where(Alert.patient_id==patient.id).order_by(Alert.created_at.desc()).limit(20)).all()
    recs=db.scalars(select(Recommendation).where(Recommendation.patient_id==patient.id).order_by(Recommendation.created_at.desc()).limit(20)).all()
    return {"patient":{"name":patient.user.name,"plan":"Personal"},"vitals":{"heart_rate":h.heart_rate if h else None,"spo2":h.spo2 if h else None,"temperature":h.body_temperature if h else None,"activity":h.activity if h else None},"risk":{"score":r.risk_score if r else None,"level":r.risk_level.value if r else None,"confidence":r.confidence if r else None,"pattern":r.pattern if r else None,"anomaly_detected":r.anomaly_detected if r else False},"environment":{"temperature":e.ambient_temperature if e else None,"humidity":e.humidity if e else None,"air_quality":e.air_quality if e else None},"baseline":{"heart_rate":patient.baseline_heart_rate,"spo2":patient.baseline_spo2,"temperature":patient.baseline_temperature},"alerts":[{"id":a.id,"type":a.type,"severity":a.severity,"title":a.title,"message":a.message,"status":a.status.value,"created_at":a.created_at} for a in alerts],"recommendations":[{"id":x.id,"category":x.category,"title":x.title,"description":x.description,"priority":x.priority,"created_at":x.created_at} for x in recs]}
