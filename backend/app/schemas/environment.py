from datetime import datetime
from pydantic import BaseModel, Field, model_validator
class EnvironmentReadingCreate(BaseModel):
    ambient_temperature:float|None=Field(None, ge=-50, le=100); humidity:float|None=Field(None, ge=0, le=100); air_quality:float|None=Field(None, ge=0, le=1000)
    @model_validator(mode="after")
    def measurement_present(self):
        if all(v is None for v in (self.ambient_temperature,self.humidity,self.air_quality)): raise ValueError("Provide at least one environmental measurement")
        return self
class EnvironmentReadingResponse(EnvironmentReadingCreate):
    id:int; patient_id:int; timestamp:datetime
    model_config={"from_attributes":True}
