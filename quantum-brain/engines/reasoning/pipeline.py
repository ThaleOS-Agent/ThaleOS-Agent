"""
ThaleOS Quantum Reasoning Pipeline
Multi-agent chain-of-thought reasoning engine.

Flow:
  1. THAELIA reads the query and decides: which specialist to call, whether
     live search is needed, and how to frame the task.
  2. (optional) SAGE does a Qwant web search to ground the response in live data.
  3. The specialist agent processes the enriched task.
  4. THAELIA synthesises the specialist's answer into a final, coherent response.

This turns a single-shot question into a coordinated multi-agent reasoning pass.
"""

import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger("ThaleOS.Reasoning.Pipeline")

# Agent keywords — same heuristic used by Siri connector
AGENT_KEYWORDS: Dict[str, List[str]] = {
    "oracle":     ["predict", "forecast", "analyse", "analyze", "probability", "future", "trend"],
    "nexus":      ["money", "business", "invest", "revenue", "finance", "crypto", "market"],
    "scales":     ["legal", "contract", "law", "rights", "compliance", "lawsuit", "regulation"],
    "scribe":     ["write", "draft", "email", "document", "report", "letter", "blog"],
    "chronagate": ["schedule", "calendar", "time", "deadline", "when", "reminder", "plan"],
    "utilix":     ["run", "file", "code", "execute", "system", "terminal", "install"],
    "phantom":    ["research", "background", "investigate", "find out", "monitor"],
    "sage":       ["explain", "what is", "how does", "learn", "summarise", "definition"],
}

RESEARCH_TRIGGERS = [
    "latest", "recent", "current", "today", "news", "now", "2024", "2025", "2026",
    "what happened", "update", "price", "live", "real-time",
]


class ReasoningPipeline:
    """
    Orchestrates a multi-agent reasoning chain for complex queries.
    Uses THAELIA as the conductor, optional SAGE+Qwant for live research,
    and the best specialist for the task domain.
    """

    def __init__(self, agent_registry, integration_manager):
        self.registry = agent_registry
        self.integrations = integration_manager

    def _detect_specialist(self, text: str) -> str:
        text_lower = text.lower()
        for agent, keywords in AGENT_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return agent
        return "thaelia"

    def _needs_live_search(self, text: str) -> bool:
        text_lower = text.lower()
        return any(trigger in text_lower for trigger in RESEARCH_TRIGGERS)

    async def _search(self, query: str) -> str:
        """Run a Qwant search and return formatted context."""
        qwant = self.integrations.get("qwant")
        if not qwant or not qwant.is_available():
            return ""
        results = await qwant.search(query, count=4)
        return qwant._format_results_for_context(results)

    async def run(
        self,
        query: str,
        preferred_agent: Optional[str] = None,
        search: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Execute the full reasoning pipeline.

        Args:
            query: The user's question or task.
            preferred_agent: Override auto-detected specialist.
            search: Override auto-detected search need (True/False/None=auto).

        Returns:
            Dict with keys: response, specialist, steps, search_used, search_context
        """
        steps: List[str] = []
        search_context = ""
        specialist = preferred_agent or self._detect_specialist(query)
        do_search = search if search is not None else self._needs_live_search(query)

        logger.info(f"[reasoning] query={query[:60]!r} specialist={specialist} search={do_search}")

        # ── Step 1: Live search (if needed) ──────────────────────────────────
        if do_search:
            steps.append("web_search")
            search_context = await self._search(query)
            logger.info(f"[reasoning] search returned {len(search_context)} chars")

        # ── Step 2: Specialist agent ──────────────────────────────────────────
        steps.append(f"specialist:{specialist}")
        specialist_task: Dict[str, Any] = {"content": query}
        if search_context:
            specialist_task["context"] = (
                f"Use this live web search data to inform your response:\n\n{search_context}"
            )

        specialist_result = await self.registry.invoke(specialist, specialist_task)
        specialist_response = specialist_result.get("response", "")

        # ── Step 3: Synthesis (only if specialist ≠ THAELIA) ─────────────────
        if specialist != "thaelia" and specialist_response:
            steps.append("synthesis:thaelia")
            synthesis_task = {
                "content": (
                    f"A user asked: {query}\n\n"
                    f"{specialist.upper()} responded:\n{specialist_response}\n\n"
                    "Synthesise this into a warm, clear, actionable response in your own voice."
                )
            }
            synthesis_result = await self.registry.invoke("thaelia", synthesis_task)
            final_response = synthesis_result.get("response", specialist_response)
        else:
            final_response = specialist_response

        return {
            "response": final_response,
            "specialist": specialist,
            "steps": steps,
            "search_used": bool(search_context),
            "search_context": search_context[:500] if search_context else "",
        }
