import urllib.parse
import httpx
from .interfaces import OAuthProvider, FerroxIdentity, OAuthProviderType

class GitHubOAuthProvider(OAuthProvider):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.user_api_url = "https://api.github.com/user"
        
    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": "read:user user:email"
        }
        return f"{self.auth_url}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str, redirect_uri: str) -> str:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        headers = {"Accept": "application/json"}
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()["access_token"]

    async def fetch_user_profile(self, access_token: str) -> FerroxIdentity:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with httpx.AsyncClient() as client:
            # Fetch user profile
            response = await client.get(self.user_api_url, headers=headers)
            response.raise_for_status()
            user_data = response.json()
            
            # Fetch user emails (GitHub doesn't always include email in the profile endpoint)
            email_response = await client.get(f"{self.user_api_url}/emails", headers=headers)
            email_response.raise_for_status()
            emails = email_response.json()
            
            primary_email = next((email for email in emails if email.get("primary")), None)
            
            name_parts = (user_data.get("name") or "").split(" ", 1)
            first_name = name_parts[0] if len(name_parts) > 0 else None
            last_name = name_parts[1] if len(name_parts) > 1 else None

            return FerroxIdentity(
                provider=OAuthProviderType.GITHUB,
                provider_user_id=str(user_data.get("id")),
                email=primary_email.get("email") if primary_email else None,
                is_email_verified=primary_email.get("verified", False) if primary_email else False,
                first_name=first_name,
                last_name=last_name,
                avatar_url=user_data.get("avatar_url"),
                raw_data=user_data
            )
