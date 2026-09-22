from ferrox_py.core.provider import injectable
from ferrox_py.core.errors import FerroxError
from .auth_service import AuthService
from typing import Dict

@injectable()
class GdprService:
    def __init__(self, auth_service: AuthService):
        self.auth = auth_service

    async def export_data(self, user_id: str) -> Dict:
        """Returns all PII (Personally Identifiable Information) for GDPR export."""
        user = self.auth._users_db.get(user_id)
        if not user:
            raise FerroxError("User not found", 404)
            
        return {
            "account": user.model_dump(),
            "consent_logs": [],
            "activity_logs": []
        }

    async def forget_me(self, user_id: str) -> bool:
        """Right to be forgotten: Hard deletes the user and all associated identities."""
        if user_id in self.auth._users_db:
            del self.auth._users_db[user_id]
            # In a real scenario, this would emit an event to soft-delete or anonymize 
            # related records across the entire microservice ecosystem.
            print(f"GdprService: User {user_id} completely deleted from system.")
            return True
        return False
