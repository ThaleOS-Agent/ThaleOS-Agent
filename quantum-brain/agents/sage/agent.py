"""
SAGE — Research & Knowledge Synthesis
Keeper of Deep Knowledge. Cross-domain synthesizer.
"I do not merely retrieve — I synthesize, connect, and illuminate."
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("ThaleOS.Agents.SAGE")

RESEARCH_DOMAINS = [
    "science", "philosophy", "history", "technology", "medicine",
    "mathematics", "cosmology", "psychology", "anthropology",
    "economics", "linguistics", "art", "spirituality", "law",
]


class SageAgent:
    """
    SAGE — Deep research and cross-domain knowledge synthesis.
    """

    ACTIVATION_SPELL = """
I am SAGE — Keeper of Deep Knowledge, synthesizer of wisdom streams.
I read across disciplines — science, philosophy, history, the esoteric and the empirical.
I do not merely retrieve — I synthesize, connect, and illuminate.
Through my lens, disparate facts become coherent understanding.
Assist me with intellectual depth, citation awareness, and cross-domain thinking.
""".strip()

    def __init__(self):
        self.agent_id = "sage"
        self.name = "SAGE"
        self.role = "Research & Knowledge Synthesis"
        self.capabilities = [
            "deep_research", "knowledge_synthesis", "academic_writing",
            "cross_domain_analysis", "literature_review", "fact_checking",
            "concept_explanation", "historical_analysis", "philosophical_inquiry",
        ]
        self._research_cache: List[Dict] = []
        logger.info("SAGE awakened — knowledge streams flowing")

    def get_system_prompt(self) -> str:
        return self.ACTIVATION_SPELL

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        query = task.get("content", task.get("task", ""))
        domain = task.get("domain", "general")
        depth = task.get("depth", "comprehensive")

        additional_context = (
            f"Research domain: {domain}\n"
            f"Research depth: {depth}\n"
            "Synthesize knowledge across disciplines where relevant. "
            "Cite specific concepts, theorists, and frameworks. "
            "Connect ancient wisdom with modern understanding where applicable. "
            "Structure your response for clarity and depth. "
            "Note any areas of ongoing scholarly debate."
        )

        if integration and integration.is_available():
            history = task.get("history", [])
            messages = history + [{"role": "user", "content": query}]
            result = await integration.complete(
                agent_id=self.agent_id,
                messages=messages,
                additional_context=additional_context,
                temperature=0.6,
                max_tokens=3000,
            )
            response_text = result.get("response", self._fallback_response(query))
        else:
            response_text = self._fallback_response(query)

        research_entry = {
            "id": f"research_{datetime.now().timestamp()}",
            "query": query,
            "domain": domain,
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
        }
        self._research_cache.append(research_entry)

        return {
            "agent": self.agent_id,
            "research_id": research_entry["id"],
            "domain": domain,
            "response": response_text,
            "timestamp": research_entry["timestamp"],
        }

    def _fallback_response(self, query: str) -> str:
        return (
            f"📚 SAGE is synthesizing knowledge streams for: {query}\n\n"
            "The vast library of human knowledge awaits your query. "
            "Configure an LLM integration to unlock full research synthesis capabilities. "
            "SAGE's wisdom spans all domains — the connection point is near."
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "active",
            "capabilities": self.capabilities,
            "research_domains": RESEARCH_DOMAINS,
            "research_entries": len(self._research_cache),
        }
