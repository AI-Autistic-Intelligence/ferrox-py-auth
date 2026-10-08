from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class KYCStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    NEEDS_REVIEW = "needs_review"
    ERROR = "error"

@dataclass
class KYCApplicant:
    """Represents a user applying for KYC."""
    id: str
    user_id: str
    first_name: str
    last_name: str
    email: str
    country_iso3: str # e.g. ITA, USA

@dataclass
class KYCVerificationResult:
    """Standardized KYC verification result."""
    applicant_id: str
    status: KYCStatus
    provider: str
    rejection_reasons: list[str]
    raw_data: Dict[str, Any]

class KYCProvider(ABC):
    
    @abstractmethod
    async def create_applicant(self, applicant: KYCApplicant) -> str:
        """Registers the applicant with the provider. Returns the provider's applicant ID."""
        pass

    @abstractmethod
    async def generate_verification_link(self, provider_applicant_id: str, redirect_url: str) -> str:
        """Generates a secure link for the user to upload their documents/selfie."""
        pass

    @abstractmethod
    async def check_status(self, provider_applicant_id: str) -> KYCVerificationResult:
        """Manually checks the verification status."""
        pass
        
    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """Verifies the authenticity of incoming webhooks."""
        pass
