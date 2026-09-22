from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Identity(BaseModel):
    provider: str  # e.g., 'local', 'google', 'facebook', 'apple'
    provider_id: str  # ID from the external provider or hash of password
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: str
    email: str
    email_verified: bool = False
    roles: List[str] = ["user"]
    identities: List[Identity] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
