from datetime import datetime
from pydantic import BaseModel, Field, model_validator
class HealthReadingCreate(BaseModel):
    heart_rate:float|None=Field(None, ge=20, le=300); spo2:float|None=Field(None, ge=0, le=100); body_temperature:float|None=Field(None, ge=25, le=45)
    activity:str|None=Field(None,max_length=80); fall_detected:bool=False
    @model_validator(mode="after")
    def measurement_present(self):
        if all(v is None for v in (self.heart_rate,self.spo2,self.body_temperature,self.activity)) and not self.fall_detected: raise ValueError("Provide at least one health measurement or fall event")
        return self
class HealthReadingResponse(HealthReadingCreate):
    id:int; patient_id:int; timestamp:datetime
    model_config={"from_attributes":True}
