import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.exceptions import InvalidTokenError

PASSWORD = "secret123"

class TestPasswordHashing:
    def test_hash_is_not_plain_password(self):
        password = PASSWORD
        hashed = hash_password(password)
        assert hashed != password

    def test_correct_password_verified(self):
        password = PASSWORD
        hashed = hash_password(password)
        assert verify_password(password, hashed)

    def test_wrong_password_not_verified(self):
        password = PASSWORD
        hashed = hash_password(password)
        assert not verify_password("wrong", hashed)

class TestJWT:
    def test_create_and_decode_token(self):
        token = create_access_token(user_id=1, role="user")
        payload = decode_token(token)
        assert "sub" in payload
        assert payload["sub"] == "1"
        assert payload["role"] == "user"
        assert "iat" in payload
        assert "exp" in payload

    def test_decode_invalid_token_raises(self):
        with pytest.raises(InvalidTokenError):
            decode_token("invalid.token.here")
            