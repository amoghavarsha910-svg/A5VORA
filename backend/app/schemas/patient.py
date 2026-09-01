from datetime import datetime
from pydantic import BaseModel, Field
class PatientUpdate(BaseModel):
    age:int|None=Field(None, ge=0, le=130); gender:str|None=Field(None,max_length=50)
    height:float|None=Field(None, gt=0, le=300); weight:float|None=Field(None, gt=0, le=700)
    baseline_heart_rate:float|None=Field(None, ge=20, le=300); baseline_spo2:float|None=Field(None, ge=0, le=100); baseline_temperature:float|None=Field(None, ge=25, le=45)
class PatientResponse(PatientUpdate):
    id:int; user_id:int; created_at:datetime; updated_at:datetime
    model_config={"from_attributes":True}
