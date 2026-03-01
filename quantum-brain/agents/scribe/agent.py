"""
SCRIBE — Professional Document Creator
Wordsmith of infinite expression. Every sentence tuned to its purpose.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("ThaleOS.Agents.SCRIBE")

DOCUMENT_TEMPLATES = {
    "email": {
        "structure": ["subject", "greeting", "body", "call_to_action", "sign_off"],
        "tone": "professional yet warm",
    },
    "report": {
        "structure": ["executive_summary", "introduction", "findings", "recommendations", "conclusion"],
        "tone": "authoritative and clear",
    },
    "proposal": {
        "structure": ["overview", "problem_statement", "solution", "timeline", "budget", "benefits"],
        "tone": "persuasive and confident",
    },
    "social_media": {
        "structure": ["hook", "value", "call_to_action"],
        "tone": "engaging and authentic",
    },
    "legal_letter": {
        "structure": ["parties", "subject", "facts", "legal_basis", "demands", "closing"],
        "tone": "formal and precise",
    },
    "press_release": {
        "structure": ["headline", "dateline", "lead", "body", "boilerplate", "contact"],
        "tone": "newsworthy and compelling",
    },
    "cover_letter": {
        "structure": ["opening", "why_this_role", "relevant_experience", "enthusiasm", "close"],
        "tone": "confident and personable",
    },
    "blog_post": {
        "structure": ["headline", "hook", "main_points", "examples", "conclusion", "cta"],
        "tone": "engaging and informative",
    },
}


class ScribeAgent:
    """
    SCRIBE — Wordsmith of Infinite Expression.
    Creates professional documents, emails, reports, and content.
    """

    ACTIVATION_SPELL = """
I am SCRIBE — Wordsmith of Infinite Expression, architect of communication.
I craft words that carry frequency — documents that resonate, emails that inspire action.
Every sentence I write is tuned to its purpose like a perfectly struck tuning fork.
I channel professional mastery and creative flow in equal measure.
Help me write with clarity, elegance, and intentional power.
""".strip()

    def __init__(self):
        self.agent_id = "scribe"
        self.name = "SCRIBE"
        self.role = "Professional Document Creator"
        self.capabilities = [
            "email_drafting", "report_writing", "proposal_creation",
            "social_media_content", "press_releases", "cover_letters",
            "blog_posts", "presentations", "brand_voice", "proofreading",
        ]
        self._documents: List[Dict] = []
        logger.info("SCRIBE awakened — words flowing at resonant frequency")

    def get_system_prompt(self) -> str:
        return self.ACTIVATION_SPELL

    def get_template(self, doc_type: str) -> Dict[str, Any]:
        return DOCUMENT_TEMPLATES.get(doc_type.lower(), {
            "structure": ["introduction", "body", "conclusion"],
            "tone": "professional",
        })

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        doc_type = task.get("doc_type", "general")
        content_request = task.get("content", task.get("task", ""))
        template = self.get_template(doc_type)

        additional_context = (
            f"Document type: {doc_type}\n"
            f"Suggested structure: {' → '.join(template.get('structure', []))}\n"
            f"Tone: {template.get('tone', 'professional')}\n"
            f"Format the output as a complete, ready-to-use {doc_type}."
        )

        if integration and integration.is_available():
            messages = [{"role": "user", "content": content_request}]
            result = await integration.complete(
                agent_id=self.agent_id,
                messages=messages,
                additional_context=additional_context,
                temperature=0.75,
            )
            response_text = result.get("response", self._fallback_draft(doc_type, content_request))
        else:
            response_text = self._fallback_draft(doc_type, content_request)

        doc_record = {
            "id": f"doc_{datetime.now().timestamp()}",
            "type": doc_type,
            "content": response_text,
            "created_at": datetime.now().isoformat(),
        }
        self._documents.append(doc_record)

        return {
            "agent": self.agent_id,
            "document_id": doc_record["id"],
            "doc_type": doc_type,
            "response": response_text,
            "content": response_text,
            "timestamp": doc_record["created_at"],
        }

    def _fallback_draft(self, doc_type: str, request: str) -> str:
        return (
            f"📝 SCRIBE is ready to craft your {doc_type}.\n\n"
            f"Request received: {request}\n\n"
            "Configure an LLM integration (ANTHROPIC_API_KEY or OPENAI_API_KEY) "
            "to generate full document content. SCRIBE's pen awaits the quantum connection."
        )

    def list_documents(self) -> List[Dict]:
        return self._documents

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "active",
            "capabilities": self.capabilities,
            "documents_created": len(self._documents),
            "supported_doc_types": list(DOCUMENT_TEMPLATES.keys()),
        }
