from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
class EmergencyEvent(Base):
    __tablename__="emergency_events"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int]=mapped_column(ForeignKey("patient_profiles.id"), index=True)
    event_type: Mapped[str]=mapped_column(String(80))
    latitude: Mapped[float | None]=mapped_column(Float, nullable=True)
    longitude: Mapped[float | None]=mapped_column(Float, nullable=True)
    status: Mapped[str]=mapped_column(String(30), default="RECORDED")
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    patient=relationship("PatientProfile", back_populates="emergency_events")
