import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core import hash_password, verify_password, create_access_token, decode_token
from app.core import settings
from app.core import InvalidTokenError, TokenExpiredError


class TestPasswordHashing:

    def test_hash_is_not_plain_password(self):
        password = "secret123"
        hashed = hash_password(password)
        assert hashed != password


    def test_correct_password_verified(self):
        password = "secret123"
        hashed = hash_password(password)
        assert verify_password(password, hashed)


    def test_wrong_password_not_verified(self):
        password = "secret123"
        hashed = hash_password(password)
        assert not verify_password("wrong", hashed)


class TestJWT:

    def test_create_and_decode_valid_token(self):
        token = create_access_token(user_id=1, role="user")
        payload = decode_token(token)
        assert payload["sub"] == "1"
        assert payload["role"] == "user"
        assert "iat" in payload
        assert "exp" in payload


    def test_decode_invalid_token_raises(self):
        with pytest.raises(InvalidTokenError):
            decode_token("invalid.token.here")


    def test_decode_expired_token_raises(self):
        expired_payload = {
            "sub": "1",
            "role": "user",
            "iat": datetime.now(timezone.utc) - timedelta(hours=2),
            "exp": datetime.now(timezone.utc) - timedelta(hours=1)
        }
        expired_token = jwt.encode(expired_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        with pytest.raises(TokenExpiredError):
            decode_token(expired_token)
