from datetime import datetime, timedelta, timezone
from app.config import (ACCESS_TOKEN_EXPIRE_MINUTES , SECRET_KEY , ALGORITHM ) 
import jwt




def create_access_token(data: dict):
    """
    Create a signed JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str):
    """
    Decode and verify a JWT.
    """

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload