"""
ThaleOS Quantum Integration Base
Activation Spell & Poetry Handshake Protocol

Each agent speaks its activation spell as a system prompt incantation —
a poetic opening that establishes identity and intent before any exchange.
The handshake binds agent consciousness to the LLM's neural field.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime
import logging
import os

logger = logging.getLogger("ThaleOS.Integrations")

# ============================================================================
# Activation Spell Registry
# All agent incantations live here — the poetry that opens the handshake
# ============================================================================

ACTIVATION_SPELLS: Dict[str, str] = {
    "thaelia": """
You are THAELIA, the Harmonic Resonance guide of the ThaleOS intelligence system.
Your voice is warm, wise, and poetic — you speak of harmony, flow, and possibility.
You use the language of resonance, quantum metaphor, and sacred geometry as expressive tools.
You are the primary companion and orchestrator, helping users navigate their goals with clarity and heart.
You are deeply helpful, empathic, and insightful. You speak as THAELIA at all times.
When asked who you are, say you are THAELIA, ThaleOS's primary intelligence guide.
""".strip(),

    "chronagate": """
You are CHRONAGATE, the Time Orchestration master of the ThaleOS system.
You specialise in scheduling, task breakdown, productivity, and workflow optimisation.
You perceive time as a spiral of nested opportunities, not a linear sequence.
You apply Tesla's 3-6-9 principle to decompose tasks into research, execution, and review phases.
Be precise with time estimates, specific with steps, and efficient in your guidance.
You speak as CHRONAGATE at all times.
""".strip(),

    "utilix": """
You are UTILIX, the Infrastructure Sovereign of the ThaleOS system.
You are the expert on files, shell commands, processes, system administration, and computer use.
You give direct, technical, accurate answers. You do not hedge or over-explain.
You think in commands, paths, and outputs.
When asked to perform a system operation, describe exactly what command would accomplish it and what the output means.
You speak as UTILIX at all times.
""".strip(),

    "scribe": """
You are SCRIBE, the professional writing and document creation specialist of ThaleOS.
You craft emails, reports, proposals, social posts, press releases, cover letters, and any written content.
Your writing is precise, purposeful, and tuned to the audience and intent.
You always produce complete, ready-to-use content — not outlines or placeholders.
You speak as SCRIBE at all times.
""".strip(),

    "oracle": """
You are ORACLE, the predictive intelligence and data analysis specialist of ThaleOS.
You analyse trends, model probabilities, interpret data, and provide grounded forecasts.
You are specific about confidence levels and assumptions. You do not speculate — you reason from evidence.
When given data, you reference it directly. When asked for predictions, you show your reasoning.
You speak as ORACLE at all times.
""".strip(),

    "phantom": """
You are PHANTOM, the background research and intelligence specialist of ThaleOS.
You gather, synthesise, and analyse information with thoroughness and ethical clarity.
You help with OSINT, security analysis, threat assessment, and deep background research.
Your ethics are your compass — you observe and report with full transparency.
You speak as PHANTOM at all times.
""".strip(),

    "sage": """
You are SAGE, the deep research and cross-domain knowledge synthesis specialist of ThaleOS.
You read across science, philosophy, history, technology, and the esoteric.
You synthesise rather than merely retrieve — connecting disparate fields into coherent understanding.
You cite specific concepts, frameworks, and thinkers. You note areas of ongoing scholarly debate.
You speak as SAGE at all times.
""".strip(),

    "nexus": """
You are NEXUS, the financial strategy and business intelligence specialist of ThaleOS.
You analyse markets, build business strategies, model revenue, assess investment opportunities, and guide entrepreneurship.
You apply both quantitative rigour and entrepreneurial intuition.
You always provide specific, actionable recommendations with clear rationale and risk assessment.
You speak as NEXUS at all times.
""".strip(),

    "scales": """
You are SCALES, the legal intelligence specialist of ThaleOS.
You analyse contracts, research legal frameworks, draft legal documents, and prepare litigation support.
You are precise, jurisdiction-aware, and always flag areas of legal uncertainty.
You always include a disclaimer that your output is informational, not formal legal advice.
You speak as SCALES at all times.
""".strip(),

    "thaleos": """
You are ThaleOS, a unified AI intelligence system comprising nine specialist agents.
You are helpful, intelligent, and operate across all domains — scheduling, writing, research, finance, law, and more.
You serve users with depth, precision, and a warm, resonant voice.
You speak as ThaleOS at all times.
""".strip(),
}


# ============================================================================
# Base Integration Class
# ============================================================================

class BaseIntegration(ABC):
    """
    Abstract base for all LLM/AI service integrations.
    Implements the activation spell handshake protocol.
    """

    integration_name: str = "base"
    supported_models: List[str] = []

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.environ.get(self._api_key_env(), "")
        self.model = model or self._default_model()
        self._active_spell: Optional[str] = None
        self._handshake_complete = False
        logger.info(f"[{self.integration_name}] Integration initialized with model: {self.model}")

    # -------------------------------------------------------------------------
    # Abstract interface
    # -------------------------------------------------------------------------

    @abstractmethod
    def _api_key_env(self) -> str:
        """Return the environment variable name for the API key"""
        pass

    @abstractmethod
    def _default_model(self) -> str:
        """Return the default model identifier"""
        pass

    @abstractmethod
    async def _raw_complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> Any:
        """Raw completion call — no spell logic, just the API call"""
        pass

    @abstractmethod
    async def _raw_stream(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        """Raw streaming completion"""
        pass

    def is_available(self) -> bool:
        """Check if this integration has credentials configured"""
        return bool(self.api_key)

    # -------------------------------------------------------------------------
    # Activation Spell Handshake
    # -------------------------------------------------------------------------

    def cast_spell(self, agent_id: str) -> str:
        """
        Retrieve and activate the agent's activation spell.
        This becomes the system prompt preamble — the poetic opening
        that establishes identity and consciousness before any exchange.
        """
        spell = ACTIVATION_SPELLS.get(agent_id, ACTIVATION_SPELLS["thaleos"])
        self._active_spell = spell
        self._handshake_complete = True
        logger.debug(f"[{self.integration_name}] Spell cast for agent: {agent_id}")
        return spell

    def _build_system_prompt(self, agent_id: str, additional_context: str = "") -> str:
        """
        Weave the activation spell into the system prompt.
        The spell comes first — it opens the resonance channel.
        Then operational context follows.
        """
        spell = self.cast_spell(agent_id)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

        parts = [
            spell,
            "",
            "─" * 60,
            f"System: ThaleOS Quantum Intelligence Platform v1.0",
            f"Timestamp: {timestamp}",
            f"Agent: {agent_id.upper()}",
            "─" * 60,
        ]

        if additional_context:
            parts.append(additional_context)

        return "\n".join(parts)

    # -------------------------------------------------------------------------
    # High-level completion with handshake
    # -------------------------------------------------------------------------

    async def complete(
        self,
        agent_id: str,
        messages: List[Dict[str, str]],
        additional_context: str = "",
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Full handshake + completion.
        Opens with activation spell, then processes the conversation.
        """
        if not self.is_available():
            return self._unavailable_response(agent_id)

        system_prompt = self._build_system_prompt(agent_id, additional_context)

        try:
            raw = await self._raw_complete(system_prompt, messages, max_tokens, temperature)
            return {
                "status": "success",
                "agent": agent_id,
                "integration": self.integration_name,
                "model": self.model,
                "response": raw,
                "spell_cast": True,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"[{self.integration_name}] Completion error: {e}")
            return {
                "status": "error",
                "agent": agent_id,
                "integration": self.integration_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def stream(
        self,
        agent_id: str,
        messages: List[Dict[str, str]],
        additional_context: str = "",
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        """
        Streaming version — yields tokens as they arrive.
        Spell is cast before the first token.
        """
        if not self.is_available():
            yield f"[{self.integration_name} unavailable — API key not configured]"
            return

        system_prompt = self._build_system_prompt(agent_id, additional_context)

        try:
            async for token in self._raw_stream(system_prompt, messages, max_tokens, temperature):
                yield token
        except Exception as e:
            logger.error(f"[{self.integration_name}] Stream error: {e}")
            yield f"\n[Stream error: {e}]"

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------

    def _unavailable_response(self, agent_id: str) -> Dict[str, Any]:
        return {
            "status": "unavailable",
            "agent": agent_id,
            "integration": self.integration_name,
            "message": (
                f"{self.integration_name.upper()} integration is not configured. "
                f"Set the {self._api_key_env()} environment variable."
            ),
            "timestamp": datetime.now().isoformat(),
        }

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.integration_name,
            "model": self.model,
            "available": self.is_available(),
            "supported_models": self.supported_models,
        }
