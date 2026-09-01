from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
class Recommendation(Base):
    __tablename__="recommendations"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int]=mapped_column(ForeignKey("patient_profiles.id"), index=True)
    category: Mapped[str]=mapped_column(String(80))
    title: Mapped[str]=mapped_column(String(160))
    description: Mapped[str]=mapped_column(Text)
    priority: Mapped[str]=mapped_column(String(30))
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    patient=relationship("PatientProfile", back_populates="recommendations")
