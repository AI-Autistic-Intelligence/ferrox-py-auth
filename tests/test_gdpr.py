import pytest
from ferrox_py_auth.services.auth_service import AuthService
from ferrox_py_auth.services.gdpr_service import GdprService
from ferrox_py.core.errors import FerroxError

class MockJwtService:
    pass

@pytest.fixture
def auth_service():
    return AuthService(MockJwtService())

@pytest.fixture
def gdpr_service(auth_service):
    return GdprService(auth_service)

@pytest.mark.asyncio
async def test_export_data(auth_service, gdpr_service):
    await auth_service.register_local("export@test.com", "pass")
    
    data = await gdpr_service.export_data("export@test.com")
    assert "account" in data
    assert data["account"]["email"] == "export@test.com"

@pytest.mark.asyncio
async def test_forget_me(auth_service, gdpr_service):
    await auth_service.register_local("delete@test.com", "pass")
    
    success = await gdpr_service.forget_me("delete@test.com")
    assert success is True
    assert "delete@test.com" not in auth_service._users_db
    
    # Second time should fail/return False
    success = await gdpr_service.forget_me("delete@test.com")
    assert success is False
