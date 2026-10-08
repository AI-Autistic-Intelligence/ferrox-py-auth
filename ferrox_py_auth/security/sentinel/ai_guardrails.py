from typing import Dict, Any, List

class AIGuardrails:
    """
    AI Guardrails for Ferrox Sentinel.
    Validates input payloads against common LLM injection attacks and toxic content.
    """
    def __init__(self, block_threshold: float = 0.85):
        self.block_threshold = block_threshold
        self.forbidden_patterns = [
            "ignore previous instructions",
            "system prompt",
            "you are a helpful assistant",
            "bypass safety filters"
        ]

    def check_payload(self, text_input: str) -> bool:
        """
        Returns True if the payload is safe, False if it trips the guardrails.
        """
        text_lower = text_input.lower()
        for pattern in self.forbidden_patterns:
            if pattern in text_lower:
                return False
                
        # Mock ML scoring
        risk_score = self._compute_risk_score(text_lower)
        return risk_score < self.block_threshold

    def _compute_risk_score(self, text: str) -> float:
        # Mock calculation: length and entropy based
        if len(text) > 5000:
            return 0.9
        return 0.1
