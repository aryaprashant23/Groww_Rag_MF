import re

class GuardrailManager:
    def __init__(self):
        # Regex patterns for PII detection
        self.pii_patterns = {
            "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
            "Aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
            "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "Phone": r"\b(?:\+91[-\s]?)?[6789]\d{9}\b",
            "Account Number": r"\b\d{9,18}\b"  # Typical Indian bank account numbers
        }
        
        # Heuristics for advisory or subjective intent
        self.advisory_keywords = [
            "should i invest",
            "is it a good",
            "is this a good",
            "which fund is better",
            "recommend",
            "should i buy",
            "should i sell",
            "best fund",
            "compare",
            "my portfolio",
            "give me advice"
        ]

    def _check_pii(self, query: str) -> tuple[bool, str]:
        """Check for PII in the query."""
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return True, f"Blocked: Query contains sensitive information ({pii_type})."
        return False, ""

    def _check_intent(self, query: str) -> tuple[bool, str]:
        """Check for advisory or subjective intent in the query."""
        query_lower = query.lower()
        for keyword in self.advisory_keywords:
            if keyword in query_lower:
                return True, "Blocked: Query asks for investment advice or subjective opinions."
        return False, ""

    def get_refusal_message(self, reason: str = "") -> str:
        """Return the standard refusal message."""
        base_message = (
            "I am a facts-only assistant and cannot process subjective queries, "
            "provide investment advice, or handle Personal Identifiable Information (PII) like PAN or Aadhaar.\n\n"
        )
        if reason:
            base_message = f"{reason}\n\n{base_message}"
            
        base_message += (
            "For educational resources on mutual funds, please visit the "
            "[AMFI Investor Corner](https://www.amfiindia.com/investor-corner) or "
            "[SEBI's Investor Website](https://investor.sebi.gov.in/)."
        )
        return base_message

    def validate_query(self, query: str) -> tuple[bool, str]:
        """
        Validates the user query against PII and intent guardrails.
        Returns (is_valid, refusal_message_or_empty)
        """
        # 1. PII Filter
        has_pii, pii_msg = self._check_pii(query)
        if has_pii:
            return False, self.get_refusal_message(pii_msg)

        # 2. Intent Classifier
        is_advisory, advisory_msg = self._check_intent(query)
        if is_advisory:
            return False, self.get_refusal_message(advisory_msg)

        # Query passed all guardrails
        return True, ""

# For testing
if __name__ == "__main__":
    guardrails = GuardrailManager()
    
    test_queries = [
        "What is the exit load for the Nippon India Small Cap fund?",
        "Is this a good fund?",
        "My PAN is ABCDE1234F, what are my returns?",
        "What is the NAV today?"
    ]
    
    for q in test_queries:
        is_valid, msg = guardrails.validate_query(q)
        print(f"Query: {q}")
        print(f"Valid: {is_valid}")
        if not is_valid:
            print(f"Message: {msg}")
        print("-" * 40)
