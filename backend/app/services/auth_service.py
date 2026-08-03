from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.user_model import user_collection
from app.schemas.user_schema import UserRegister, UserLogin
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token


async def get_user_by_email(email: str):
    return await user_collection.find_one({"email": email})


async def register_user(user: UserRegister):
    # Check if email already exists
    existing_user = await get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create user document
    user_document = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "created_at": datetime.now(timezone.utc),
        "last_login": None,
        "is_active": True,
    }

    result =await user_collection.insert_one(user_document)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
    }


async def authenticate_user(login_data: UserLogin):
    user = await get_user_by_email(login_data.email)

    if not user:
        return None

    if not verify_password(
        login_data.password,
        user["hashed_password"]
    ):
        return None

    return user


async def login_user(login_data: UserLogin):
    user = await authenticate_user(login_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Update last login
    await user_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "last_login": datetime.now(timezone.utc)
            }
        },
    )

    access_token = create_access_token(
        {
            "sub": str(user["_id"])
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
