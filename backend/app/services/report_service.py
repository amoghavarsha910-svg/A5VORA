import csv
from io import BytesIO,StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import HealthReading,RiskAssessment
def csv_report(db:Session,patient_id:int)->str:
    out=StringIO(); writer=csv.writer(out); writer.writerow(["timestamp","heart_rate","spo2","body_temperature","activity","fall_detected"])
    rows=db.scalars(select(HealthReading).where(HealthReading.patient_id==patient_id).order_by(HealthReading.timestamp.desc())).all()
    for r in rows: writer.writerow([r.timestamp.isoformat(),r.heart_rate,r.spo2,r.body_temperature,r.activity,r.fall_detected])
    return out.getvalue()
def pdf_report(db:Session,patient)->bytes:
    buf=BytesIO(); pdf=canvas.Canvas(buf,pagesize=letter); _,height=letter; y=height-60
    pdf.setFont("Helvetica-Bold",16); pdf.drawString(50,y,"Personal Health Companion Report"); y-=30
    pdf.setFont("Helvetica",10); pdf.drawString(50,y,f"Patient: {patient.user.name}"); y-=20
    readings=db.scalars(select(HealthReading).where(HealthReading.patient_id==patient.id).order_by(HealthReading.timestamp.desc()).limit(20)).all()
    risks=db.scalars(select(RiskAssessment).where(RiskAssessment.patient_id==patient.id).order_by(RiskAssessment.timestamp.desc()).limit(10)).all()
    pdf.drawString(50,y,f"Recorded health readings: {len(readings)}"); y-=20
    for r in readings:
        pdf.drawString(50,y,f"{r.timestamp.isoformat()} | HR: {r.heart_rate} | SpO2: {r.spo2} | Temp: {r.body_temperature}"); y-=14
        if y<60: pdf.showPage(); y=height-60; pdf.setFont("Helvetica",10)
    y-=10; pdf.setFont("Helvetica-Bold",11); pdf.drawString(50,y,"Risk history (temporary rule-based engine)"); y-=18; pdf.setFont("Helvetica",10)
    for r in risks:
        pdf.drawString(50,y,f"{r.timestamp.isoformat()} | {r.risk_level.value} | score {r.risk_score} | {r.pattern or ''}"); y-=14
        if y<60: pdf.showPage(); y=height-60; pdf.setFont("Helvetica",10)
    pdf.save(); return buf.getvalue()
