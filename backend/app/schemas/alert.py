from datetime import datetime
from pydantic import BaseModel
from ..models.alert import AlertStatus
class AlertResponse(BaseModel):
    id:int; patient_id:int; type:str; severity:str; title:str; message:str; status:AlertStatus; created_at:datetime; resolved_at:datetime|None
    model_config={"from_attributes":True}
