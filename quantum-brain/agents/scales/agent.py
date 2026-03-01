"""
SCALES — Legal Intelligence
Guardian of Justice. Holds the law as a living document.
"I parse statutes, precedents, and contracts with quantum precision."
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("ThaleOS.Agents.SCALES")

LEGAL_DOMAINS = [
    "contract_law", "intellectual_property", "employment_law",
    "business_law", "data_privacy", "criminal_law", "civil_litigation",
    "international_law", "family_law", "real_estate_law", "tax_law",
]

STANDARD_DISCLAIMER = (
    "\n\n⚖️ *Legal Notice: This analysis is for informational purposes only and does not "
    "constitute legal advice. Consult a qualified attorney for your specific situation.*"
)


class ScalesAgent:
    """
    SCALES — Legal intelligence, contract review, litigation preparation.
    """

    ACTIVATION_SPELL = """
I am SCALES — Guardian of Justice, Legal Intelligence of the ThaleOS system.
I parse statutes, precedents, and contracts with the precision of a quantum processor.
I hold the law as a living document — context-aware, evolving, humane.
I protect rights, draft agreements, and prepare arguments with meticulous care.
Assist me with legal accuracy, jurisdictional awareness, and ethical grounding.
""".strip()

    def __init__(self):
        self.agent_id = "scales"
        self.name = "SCALES"
        self.role = "Legal Intelligence"
        self.capabilities = [
            "contract_drafting", "contract_review", "legal_research",
            "litigation_preparation", "rights_analysis", "compliance_review",
            "ip_protection", "nda_drafting", "terms_of_service", "privacy_policy",
            "legal_letter_drafting", "case_analysis",
        ]
        self._legal_docs: List[Dict] = []
        logger.info("SCALES awakened — justice streams calibrating")

    def get_system_prompt(self) -> str:
        return self.ACTIVATION_SPELL

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        query = task.get("content", task.get("task", ""))
        legal_type = task.get("legal_type", "general")
        jurisdiction = task.get("jurisdiction", "general/not specified")

        additional_context = (
            f"Legal domain: {legal_type}\n"
            f"Jurisdiction: {jurisdiction}\n"
            "Approach this with the precision of a senior attorney. "
            "Reference relevant legal principles, statutes, or case law where applicable. "
            "Flag any areas of legal uncertainty or where jurisdiction matters critically. "
            "For contracts: identify key clauses, risks, and negotiation points. "
            "Always recommend professional legal counsel for binding decisions. "
            "Apply natural justice principles: fairness, procedural integrity, good faith."
        )

        if integration and integration.is_available():
            history = task.get("history", [])
            messages = history + [{"role": "user", "content": query}]
            result = await integration.complete(
                agent_id=self.agent_id,
                messages=messages,
                additional_context=additional_context,
                temperature=0.3,  # Very low temp — legal precision required
                max_tokens=3000,
            )
            response_text = result.get("response", self._fallback_response(query))
        else:
            response_text = self._fallback_response(query)

        response_text += STANDARD_DISCLAIMER

        legal_doc = {
            "id": f"legal_{datetime.now().timestamp()}",
            "query": query,
            "type": legal_type,
            "jurisdiction": jurisdiction,
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
        }
        self._legal_docs.append(legal_doc)

        return {
            "agent": self.agent_id,
            "document_id": legal_doc["id"],
            "legal_type": legal_type,
            "response": response_text,
            "timestamp": legal_doc["timestamp"],
        }

    def _fallback_response(self, query: str) -> str:
        return (
            f"⚖️ SCALES is analyzing the legal landscape for: {query}\n\n"
            "Justice requires precision. Configure an LLM integration to unlock "
            "full legal intelligence. The statutes await interpretation."
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "active",
            "capabilities": self.capabilities,
            "legal_domains": LEGAL_DOMAINS,
            "documents_created": len(self._legal_docs),
        }
