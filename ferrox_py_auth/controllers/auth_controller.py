from fastapi import Request
from pydantic import BaseModel
from ferrox_py.core.controllers import BaseController
from ferrox_py.core.container import Container
from ..services.auth_service import AuthService
from ..services.gdpr_service import GdprService
from ..security.rbac import require_roles

class LoginPayload(BaseModel):
    email: str
    password_hash: str

class SsoPayload(BaseModel):
    provider: str
    provider_id: str
    email: str

class AuthController(BaseController):
    def __init__(self, container: Container):
        super().__init__(prefix="/auth", tags=["Auth & IAM"])
        
        self.auth = AuthService(container.resolve("JwtService"))
        self.gdpr = GdprService(self.auth)
        
        @self.router.get("/config")
        async def get_config():
            return self.ok(self.auth.get_config(), "Auth settings retrieved")
            
        @self.router.post("/register")
        async def register(payload: LoginPayload):
            user = await self.auth.register_local(payload.email, payload.password_hash)
            return self.created(user.model_dump(), "User registered. Please check your email.")
            
        @self.router.post("/sso")
        async def sso_login(payload: SsoPayload):
            token = await self.auth.login_sso(payload.provider, payload.provider_id, payload.email)
            return self.ok({"token": token}, "SSO Login successful")
            
        @self.router.get("/gdpr/export")
        @require_roles("user", "admin")
        async def export_my_data(request: Request):
            # Extract user_id from the authenticated request state
            user_id = request.state.user["sub"]
            data = await self.gdpr.export_data(user_id)
            return self.ok(data, "GDPR Export ready")
            
        @self.router.delete("/gdpr/forget")
        @require_roles("user", "admin")
        async def delete_my_account(request: Request):
            user_id = request.state.user["sub"]
            success = await self.gdpr.forget_me(user_id)
            return self.ok({"deleted": success}, "Account permanently deleted")
