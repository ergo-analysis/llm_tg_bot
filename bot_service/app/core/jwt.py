from jose import JWTError, jwt
from ..core import settings

def decode_and_validate(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])

        if "sub" not in payload:
            raise ValueError("no sub in token")
        return payload
    except JWTError as e:
        raise ValueError("invalid token") from e