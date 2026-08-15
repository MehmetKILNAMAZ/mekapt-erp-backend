from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from ..database import get_db
from ..models.user import User
from ..auth.jwt import verify_password, hash_password, create_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_admin: bool
    full_name: str
    daire_no: int | None = None

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    is_admin: bool = False
    daire_no: int | None = None

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Kullanıcı adı veya şifre hatalı")
    token = create_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer", "is_admin": user.is_admin, "full_name": user.full_name or user.username, "daire_no": user.daire_no}

@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == req.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten alınmış")
    user = User(username=req.username, email=req.email, hashed_password=hash_password(req.password),
                full_name=req.full_name, is_admin=req.is_admin, daire_no=req.daire_no)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = create_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer", "is_admin": user.is_admin, "full_name": user.full_name, "daire_no": user.daire_no}

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email,
            "full_name": current_user.full_name, "is_admin": current_user.is_admin, "daire_no": current_user.daire_no}
