from datetime import datetime
from pydantic import BaseModel, Field
from ..models.risk_assessment import RiskLevel
class RiskResponse(BaseModel):
    id:int; patient_id:int; risk_score:float=Field(ge=0,le=100); risk_level:RiskLevel; heat_stress_score:float; respiratory_risk_score:float; cardiovascular_risk_score:float; anomaly_detected:bool; confidence:float; pattern:str|None; timestamp:datetime
    model_config={"from_attributes":True}
