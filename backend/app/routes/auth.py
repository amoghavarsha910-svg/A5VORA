from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, PatientProfile, UserRole
from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from ..services.auth_service import hash_password, verify_password, create_access_token
router=APIRouter(prefix="/api/auth",tags=["Authentication"])
@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(body:RegisterRequest,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==body.email.lower()).first(): raise HTTPException(400,"Email is already registered")
    user=User(name=body.name,email=body.email.lower(),password_hash=hash_password(body.password),role=body.role); db.add(user); db.flush()
    if body.role==UserRole.PATIENT: db.add(PatientProfile(user_id=user.id))
    db.commit(); db.refresh(user); return user
@router.post("/login",response_model=TokenResponse)
def login(body:LoginRequest,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==body.email.lower()).first()
    if not user or not verify_password(body.password,user.password_hash): raise HTTPException(status_code=401,detail="Incorrect email or password",headers={"WWW-Authenticate":"Bearer"})
    return TokenResponse(access_token=create_access_token(str(user.id)))
