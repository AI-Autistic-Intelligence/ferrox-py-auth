import urllib.parse
import httpx
from .interfaces import OAuthProvider, FerroxIdentity, OAuthProviderType

class GoogleOAuthProvider(OAuthProvider):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        
    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }
        return f"{self.auth_url}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str, redirect_uri: str) -> str:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=data)
            response.raise_for_status()
            return response.json()["access_token"]

    async def fetch_user_profile(self, access_token: str) -> FerroxIdentity:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.userinfo_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            return FerroxIdentity(
                provider=OAuthProviderType.GOOGLE,
                provider_user_id=data.get("sub"),
                email=data.get("email"),
                is_email_verified=data.get("email_verified", False),
                first_name=data.get("given_name"),
                last_name=data.get("family_name"),
                avatar_url=data.get("picture"),
                raw_data=data
            )
