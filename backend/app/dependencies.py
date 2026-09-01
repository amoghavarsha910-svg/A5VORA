from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from .models import User, UserRole, PatientProfile
from .services.auth_service import ALGORITHM
bearer_scheme = HTTPBearer(scheme_name="Bearer Authentication", bearerFormat="JWT", auto_error=False)
def get_current_user(auth_credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme), db:Session=Depends(get_db))->User:
    credentials_error=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    if auth_credentials is None or auth_credentials.scheme.lower() != "bearer": raise credentials_error
    try: subject=jwt.decode(auth_credentials.credentials,settings.secret_key,algorithms=[ALGORITHM]).get("sub")
    except JWTError: raise credentials_error
    if not subject or not (user:=db.get(User,int(subject))): raise credentials_error
    return user
def require_patient(user:User=Depends(get_current_user))->User:
    if user.role != UserRole.PATIENT: raise HTTPException(status_code=403,detail="Patient access required")
    return user
def require_doctor(user:User=Depends(get_current_user))->User:
    if user.role != UserRole.DOCTOR: raise HTTPException(status_code=403,detail="Doctor access required")
    return user
def get_current_patient(user:User=Depends(require_patient),db:Session=Depends(get_db))->PatientProfile:
    if not user.patient_profile: raise HTTPException(status_code=404,detail="Patient profile not found")
    return user.patient_profile
