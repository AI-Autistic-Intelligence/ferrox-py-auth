from ferrox_py.core.provider import injectable
from ferrox_py.core.errors import FerroxError
from ferrox_py.security.jwt import JwtService
from ..models.user import User, Identity
from typing import Dict, Any

@injectable()
class AuthService:
    def __init__(self, jwt_service: JwtService):
        self.jwt = jwt_service
        self.enforce_sso_only = False  # Feature flag configurable by the application
        
        # Mock DB
        self._users_db: Dict[str, User] = {}

    def get_config(self) -> dict:
        """Returns auth settings for the frontend (e.g. to hide password fields)."""
        return {"enforce_sso_only": self.enforce_sso_only}

    async def register_local(self, email: str, password_hash: str) -> User:
        if self.enforce_sso_only:
            raise FerroxError("Local registration is disabled by SSO policy", 403)
            
        if email in self._users_db:
            raise FerroxError("Email already in use", 400)
            
        user = User(
            id=email, 
            email=email, 
            identities=[Identity(provider="local", provider_id=password_hash)]
        )
        self._users_db[email] = user
        
        # Here we would trigger the MailerService for email_verified=True
        print(f"AuthService: Emitting Email Confirmation for {email}")
        return user

    async def login_sso(self, provider: str, provider_id: str, email: str) -> str:
        """Handles SSO login or account linkage if user already exists."""
        user = self._users_db.get(email)
        
        if not user:
            # Create new user, auto-verify email since it comes from trusted SSO
            user = User(id=email, email=email, email_verified=True, identities=[])
            self._users_db[email] = user
            
        # Link identity if not present
        if not any(i.provider == provider for i in user.identities):
            user.identities.append(Identity(provider=provider, provider_id=provider_id))
            
        # Issue JWT
        return self.jwt.sign({"sub": user.id, "roles": user.roles})
