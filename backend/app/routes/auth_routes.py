from fastapi import APIRouter

from app.schemas.user_schema import UserRegister, UserLogin
from app.schemas.auth_schema import Token
from app.services.auth_service import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", status_code=201)
async def register(user: UserRegister):
    return await register_user(user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    return await login_user(user)