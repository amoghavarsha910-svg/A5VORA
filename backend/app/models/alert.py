import enum
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
class AlertStatus(str, enum.Enum): ACTIVE="ACTIVE"; RESOLVED="RESOLVED"
class Alert(Base):
    __tablename__="alerts"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int]=mapped_column(ForeignKey("patient_profiles.id"), index=True)
    type: Mapped[str]=mapped_column(String(80))
    severity: Mapped[str]=mapped_column(String(30))
    title: Mapped[str]=mapped_column(String(160))
    message: Mapped[str]=mapped_column(Text)
    status: Mapped[AlertStatus]=mapped_column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None]=mapped_column(DateTime, nullable=True)
    patient=relationship("PatientProfile", back_populates="alerts")
