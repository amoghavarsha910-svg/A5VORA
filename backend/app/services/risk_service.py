"""Temporary rule-based risk engine for integration testing; not a medical diagnostic system."""
from sqlalchemy.orm import Session
from ..models import HealthReading, EnvironmentReading, RiskAssessment, RiskLevel, Alert, Recommendation
def assess(db:Session, patient_id:int, health:HealthReading|None, environment:EnvironmentReading|None)->RiskAssessment|None:
    if not health and not environment: return None
    heat=resp=cardio=0.0; notes=[]
    if environment and environment.ambient_temperature is not None and environment.ambient_temperature>=32: heat=max(heat,60); notes.append("elevated ambient temperature")
    if environment and environment.humidity is not None and environment.humidity>=70: heat=max(heat,70); notes.append("high humidity")
    if environment and environment.air_quality is not None and environment.air_quality>=150: resp=70; notes.append("poor air quality")
    if health and health.heart_rate is not None and (health.heart_rate>=110 or health.heart_rate<=45): cardio=75; notes.append("unusual heart-rate reading")
    if health and health.spo2 is not None and health.spo2<92: resp=max(resp,80); notes.append("low SpO₂ reading")
    if health and health.body_temperature is not None and health.body_temperature>=38: heat=max(heat,75); notes.append("elevated body-temperature reading")
    if health and health.fall_detected: cardio=max(cardio,90); notes.append("fall detected")
    score=max(heat,resp,cardio)
    level=RiskLevel.HIGH_RISK if score>=70 else RiskLevel.CAUTION if score>=35 else RiskLevel.NORMAL
    item=RiskAssessment(patient_id=patient_id,risk_score=score,risk_level=level,heat_stress_score=heat,respiratory_risk_score=resp,cardiovascular_risk_score=cardio,anomaly_detected=score>=70,confidence=0.8 if health and environment else 0.55,pattern=", ".join(notes) if notes else "no rule-based concern identified")
    db.add(item)
    if level != RiskLevel.NORMAL:
        alert=Alert(patient_id=patient_id,type="RULE_BASED_RISK",severity="HIGH" if level==RiskLevel.HIGH_RISK else "CAUTION",title="Health signal needs attention",message="Temporary rule-based assessment: "+item.pattern)
        rec=Recommendation(patient_id=patient_id,category="monitoring",title="Review recent readings",description="Consider resting, checking sensor placement, and seeking professional advice if concerning readings persist.",priority="high" if level==RiskLevel.HIGH_RISK else "medium")
        db.add_all([alert,rec])
    return item
