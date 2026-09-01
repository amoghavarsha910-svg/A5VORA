from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_patient
from ..models import PatientProfile
from ..services.health_service import save_health,save_environment
router=APIRouter(prefix="/api/device",tags=["Device"])
class DeviceReading(BaseModel):
    device_id:str=Field(min_length=1,max_length=120)
    heart_rate:float|None=Field(None,ge=20,le=300); spo2:float|None=Field(None,ge=0,le=100); body_temperature:float|None=Field(None,ge=25,le=45)
    activity:str|None=Field(None,max_length=80); fall_detected:bool=False
    ambient_temperature:float|None=Field(None,ge=-50,le=100); humidity:float|None=Field(None,ge=0,le=100); air_quality:float|None=Field(None,ge=0,le=1000)
@router.post("/readings",status_code=status.HTTP_201_CREATED)
def ingest(body:DeviceReading,patient:PatientProfile=Depends(get_current_patient),db:Session=Depends(get_db)):
    data=body.model_dump(); data.pop("device_id")
    health_keys={"heart_rate","spo2","body_temperature","activity","fall_detected"}; env_keys={"ambient_temperature","humidity","air_quality"}
    health=save_health(db,patient.id,{k:data[k] for k in health_keys}) if any(data[k] is not None for k in health_keys-{"fall_detected"}) or data["fall_detected"] else None
    environment=save_environment(db,patient.id,{k:data[k] for k in env_keys}) if any(data[k] is not None for k in env_keys) else None
    if not health and not environment: raise HTTPException(422,"Provide health or environmental measurements")
    return {"message":"Device readings stored","health_reading_id":health.id if health else None,"environment_reading_id":environment.id if environment else None}
