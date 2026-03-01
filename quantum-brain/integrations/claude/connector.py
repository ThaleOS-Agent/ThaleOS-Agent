"""
ThaleOS × Anthropic Claude Integration
Activation spell handshake for Claude models.
"""

import os
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator

from ..base_integration import BaseIntegration

logger = logging.getLogger("ThaleOS.Integrations.Claude")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("anthropic package not installed — run: pip install anthropic")


class ClaudeConnector(BaseIntegration):
    """Claude API connector with activation spell handshake"""

    integration_name = "claude"
    supported_models = [
        "claude-sonnet-4-6",
        "claude-opus-4-6",
        "claude-haiku-4-5-20251001",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
    ]

    def _api_key_env(self) -> str:
        return "ANTHROPIC_API_KEY"

    def _default_model(self) -> str:
        return "claude-sonnet-4-6"

    def _get_client(self):
        if not ANTHROPIC_AVAILABLE:
            raise RuntimeError("anthropic package not installed")
        return anthropic.AsyncAnthropic(api_key=self.api_key)

    async def _raw_complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str:
        client = self._get_client()
        response = await client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text

    async def _raw_stream(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        client = self._get_client()
        async with client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=messages,
        ) as stream_obj:
            async for text in stream_obj.text_stream:
                yield text
