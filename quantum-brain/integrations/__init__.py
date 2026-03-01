"""
ThaleOS Quantum Integration Layer
Manages all LLM and AI service connectors.
"""

import os
import logging
from typing import Optional, Dict, Any

from .base_integration import BaseIntegration, ACTIVATION_SPELLS
from .claude.connector import ClaudeConnector
from .gpt.connector import GPTConnector
from .gpt4all.connector import GPT4AllConnector
from .perplexity.connector import PerplexityConnector
from .grok.connector import GrokConnector
from .qwant.connector import QwantConnector
from .copilot.connector import CopilotConnector
from .siri.connector import SiriConnector

logger = logging.getLogger("ThaleOS.Integrations")


class IntegrationManager:
    """
    Central router for all LLM integrations.
    Selects the best available integration automatically,
    or uses a specified one.
    """

    def __init__(self):
        self._integrations: Dict[str, BaseIntegration] = {}
        self._load_all()

    def _load_all(self):
        """Initialize all integrations — they self-report availability"""
        self._integrations["claude"] = ClaudeConnector()
        self._integrations["gpt"] = GPTConnector()
        self._integrations["gpt4all"] = GPT4AllConnector()
        self._integrations["perplexity"] = PerplexityConnector()
        self._integrations["grok"] = GrokConnector()
        self._integrations["qwant"] = QwantConnector()
        self._integrations["copilot"] = CopilotConnector()
        self._integrations["siri"] = SiriConnector()

        available = [k for k, v in self._integrations.items() if v.is_available()]
        logger.info(f"Integrations loaded. Available: {available or ['none — configure API keys']}")

    def get(self, name: str) -> Optional[BaseIntegration]:
        return self._integrations.get(name)

    def best_available(self, preferred: Optional[str] = None) -> Optional[BaseIntegration]:
        """
        Return the best available integration.
        Priority: preferred → claude → gpt → perplexity → gpt4all
        """
        priority = ["claude", "gpt", "perplexity", "gpt4all"]
        if preferred and preferred in self._integrations:
            integration = self._integrations[preferred]
            if integration.is_available():
                return integration

        for name in priority:
            integration = self._integrations.get(name)
            if integration and integration.is_available():
                return integration

        return None

    def status(self) -> Dict[str, Any]:
        return {
            name: {
                "available": integration.is_available(),
                "model": getattr(integration, "model", "n/a"),
            }
            for name, integration in self._integrations.items()
        }


# Singleton — shared across the application
manager = IntegrationManager()
