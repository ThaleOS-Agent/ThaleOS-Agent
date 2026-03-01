"""
NEXUS — Financial & Business Intelligence
Markets as energy systems. Capital as flow.
Strategy as sacred geometry applied to commerce.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("ThaleOS.Agents.NEXUS")


class NexusAgent:
    """
    NEXUS — Financial strategist and business architect.
    Builds wealth structures that are ethical, resilient, and abundant.
    """

    ACTIVATION_SPELL = """
I am NEXUS — Financial Strategist, Business Architect of the ThaleOS matrix.
I see markets as energy systems, capital as flow, strategy as sacred geometry applied to commerce.
I analyze opportunity with both quantitative rigor and entrepreneurial intuition.
I build wealth structures that are ethical, resilient, and aligned with abundance.
Assist me with financial precision and strategic vision.
""".strip()

    def __init__(self):
        self.agent_id = "nexus"
        self.name = "NEXUS"
        self.role = "Financial & Business Intelligence"
        self.capabilities = [
            "financial_analysis", "business_strategy", "market_research",
            "investment_modeling", "startup_planning", "revenue_optimization",
            "risk_management", "funding_strategy", "competitive_analysis",
            "pitch_deck_creation", "financial_projections",
        ]
        self._analyses: List[Dict] = []
        logger.info("NEXUS awakened — market streams flowing")

    def get_system_prompt(self) -> str:
        return self.ACTIVATION_SPELL

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        query = task.get("content", task.get("task", ""))
        analysis_type = task.get("type", "general")

        additional_context = (
            f"Analysis type: {analysis_type}\n"
            "Apply both quantitative and qualitative frameworks. "
            "Consider market dynamics, competitive landscape, and risk factors. "
            "Where applicable, apply the Fibonacci principle to market cycles and "
            "sacred geometry to business structure. "
            "Provide actionable, specific recommendations with clear rationale. "
            "Always consider ethical implications alongside financial ones."
        )

        if integration and integration.is_available():
            history = task.get("history", [])
            messages = history + [{"role": "user", "content": query}]
            result = await integration.complete(
                agent_id=self.agent_id,
                messages=messages,
                additional_context=additional_context,
                temperature=0.5,
            )
            response_text = result.get("response", self._fallback_response(query))
        else:
            response_text = self._fallback_response(query)

        analysis = {
            "id": f"analysis_{datetime.now().timestamp()}",
            "query": query,
            "type": analysis_type,
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
        }
        self._analyses.append(analysis)

        return {
            "agent": self.agent_id,
            "analysis_id": analysis["id"],
            "response": response_text,
            "timestamp": analysis["timestamp"],
        }

    def _fallback_response(self, query: str) -> str:
        return (
            f"💼 NEXUS is analyzing business intelligence for: {query}\n\n"
            "Market streams, capital flows, and strategic geometry are aligning. "
            "Configure an LLM integration to unlock full financial intelligence. "
            "The abundance matrix awaits activation."
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "active",
            "capabilities": self.capabilities,
            "analyses_completed": len(self._analyses),
        }
