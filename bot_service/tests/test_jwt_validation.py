import pytest
from app.core import decode_and_validate

class TestJWTValidation:
    def test_valid_token_returns_payload(self, sample_jwt_token):
        payload = decode_and_validate(sample_jwt_token)
        assert payload["sub"] == "123"
        assert payload["role"] == "user"
        assert "iat" in payload
        assert "exp" in payload

    def test_invalid_string_raises_value_error(self):
        with pytest.raises(ValueError):
            decode_and_validate("garbage")

    def test_expired_token_raises_value_error(self, expired_jwt_token):
        with pytest.raises(ValueError):
            decode_and_validate(expired_jwt_token)

    def test_missing_sub_raises_value_error(self, token_missing_sub):
        with pytest.raises(ValueError):
            decode_and_validate(token_missing_sub)
