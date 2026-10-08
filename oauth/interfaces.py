from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class OAuthProviderType(Enum):
    GOOGLE = "google"
    GITHUB = "github"
    APPLE = "apple"
    MICROSOFT = "microsoft"

@dataclass
class FerroxIdentity:
    """Standardized identity profile returned by any OAuth provider."""
    provider: OAuthProviderType
    provider_user_id: str
    email: str
    is_email_verified: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    raw_data: Dict[str, Any] = None

class OAuthProvider(ABC):
    
    @abstractmethod
    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """Returns the URL where the user should be redirected to authenticate."""
        pass

    @abstractmethod
    async def exchange_code(self, code: str, redirect_uri: str) -> str:
        """Exchanges the authorization code for an access token."""
        pass

    @abstractmethod
    async def fetch_user_profile(self, access_token: str) -> FerroxIdentity:
        """Fetches and normalizes the user profile from the provider."""
        pass

class OAuthManager:
    """Centralized manager for handling OAuth flows."""
    
    def __init__(self):
        self._providers: Dict[OAuthProviderType, OAuthProvider] = {}
        
    def register_provider(self, provider_type: OAuthProviderType, provider: OAuthProvider):
        self._providers[provider_type] = provider
        
    def get_provider(self, provider_type: OAuthProviderType) -> OAuthProvider:
        if provider_type not in self._providers:
            raise ValueError(f"OAuth provider {provider_type} is not registered.")
        return self._providers[provider_type]
