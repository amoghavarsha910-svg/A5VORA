from datetime import datetime
from pydantic import BaseModel, Field
class SOSCreate(BaseModel):
    event_type:str=Field(default="SOS", min_length=1,max_length=80); latitude:float|None=Field(None,ge=-90,le=90); longitude:float|None=Field(None,ge=-180,le=180)
class EmergencyResponse(BaseModel):
    id:int; patient_id:int; event_type:str; latitude:float|None; longitude:float|None; status:str; created_at:datetime
    model_config={"from_attributes":True}
