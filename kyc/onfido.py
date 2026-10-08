import httpx
import hmac
import hashlib
from typing import Dict, Any
from .interfaces import KYCProvider, KYCApplicant, KYCVerificationResult, KYCStatus

class OnfidoKYCProvider(KYCProvider):
    """Implementation of KYCProvider for Onfido."""
    
    def __init__(self, api_token: str, region_url: str = "https://api.eu.onfido.com/v3.6"):
        self.api_token = api_token
        self.base_url = region_url
        self.headers = {
            "Authorization": f"Token token={self.api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def create_applicant(self, applicant: KYCApplicant) -> str:
        data = {
            "first_name": applicant.first_name,
            "last_name": applicant.last_name,
            "email": applicant.email,
            "location": {
                "country_of_residence": applicant.country_iso3
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/applicants", 
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["id"]

    async def generate_verification_link(self, provider_applicant_id: str, redirect_url: str) -> str:
        data = {
            "applicant_id": provider_applicant_id,
            "redirect_url": redirect_url
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sdk_tokens", 
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["token"]

    async def check_status(self, provider_applicant_id: str) -> KYCVerificationResult:
        async with httpx.AsyncClient() as client:
            # In Onfido, we check the status of 'checks' for an applicant
            response = await client.get(
                f"{self.base_url}/checks?applicant_id={provider_applicant_id}", 
                headers=self.headers
            )
            response.raise_for_status()
            checks = response.json().get("checks", [])
            
            if not checks:
                return KYCVerificationResult(
                    applicant_id=provider_applicant_id,
                    status=KYCStatus.PENDING,
                    provider="onfido",
                    rejection_reasons=[],
                    raw_data={}
                )
            
            latest_check = checks[0]
            status_str = latest_check.get("status")
            result_str = latest_check.get("result")
            
            status = KYCStatus.PENDING
            if status_str == "complete":
                if result_str == "clear":
                    status = KYCStatus.APPROVED
                elif result_str == "consider":
                    status = KYCStatus.NEEDS_REVIEW
                else:
                    status = KYCStatus.DECLINED
            
            return KYCVerificationResult(
                applicant_id=provider_applicant_id,
                status=status,
                provider="onfido",
                rejection_reasons=[],
                raw_data=latest_check
            )

    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        expected_sig = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_sig, signature)
