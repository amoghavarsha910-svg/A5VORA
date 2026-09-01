import enum
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
class RiskLevel(str, enum.Enum): NORMAL="NORMAL"; CAUTION="CAUTION"; HIGH_RISK="HIGH_RISK"
class RiskAssessment(Base):
    __tablename__="risk_assessments"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int]=mapped_column(ForeignKey("patient_profiles.id"), index=True)
    risk_score: Mapped[float]=mapped_column(Float)
    risk_level: Mapped[RiskLevel]=mapped_column(Enum(RiskLevel))
    heat_stress_score: Mapped[float]=mapped_column(Float, default=0)
    respiratory_risk_score: Mapped[float]=mapped_column(Float, default=0)
    cardiovascular_risk_score: Mapped[float]=mapped_column(Float, default=0)
    anomaly_detected: Mapped[bool]=mapped_column(Boolean, default=False)
    confidence: Mapped[float]=mapped_column(Float, default=0)
    pattern: Mapped[str | None]=mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, index=True)
    patient=relationship("PatientProfile", back_populates="risk_assessments")
