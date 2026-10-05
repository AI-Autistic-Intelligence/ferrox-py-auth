import pytest
from ferrox_py.core.errors import FerroxError
from ferrox_py_auth.services.auth_service import AuthService
from ferrox_py_auth.models.user import User

class MockJwtService:
    def sign(self, payload: dict) -> str:
        return f"mock_token_{payload['sub']}"

@pytest.fixture
def auth_service():
    jwt = MockJwtService()
    return AuthService(jwt)

@pytest.mark.asyncio
async def test_register_local_success(auth_service):
    user = await auth_service.register_local("test@example.com", "hash")
    assert user.email == "test@example.com"
    assert "test@example.com" in auth_service._users_db
    
@pytest.mark.asyncio
async def test_register_local_disabled(auth_service):
    auth_service.enforce_sso_only = True
    with pytest.raises(FerroxError) as exc:
        await auth_service.register_local("test@example.com", "hash")
    assert exc.value.status_code == 403

@pytest.mark.asyncio
async def test_login_sso(auth_service):
    token = await auth_service.login_sso("google", "123", "sso@example.com")
    assert token == "mock_token_sso@example.com"
    
    user = auth_service._users_db["sso@example.com"]
    assert user.email_verified is True
    assert any(i.provider == "google" for i in user.identities)
