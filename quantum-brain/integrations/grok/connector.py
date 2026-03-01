"""
ThaleOS × Grok (xAI) Integration
xAI's Grok LLM via OpenAI-compatible API at api.x.ai
"""

import logging
from typing import Dict, Any, List, Optional, AsyncGenerator

from ..base_integration import BaseIntegration

logger = logging.getLogger("ThaleOS.Integrations.Grok")

try:
    from openai import AsyncOpenAI
    OPENAI_CLIENT_AVAILABLE = True
except ImportError:
    OPENAI_CLIENT_AVAILABLE = False

GROK_BASE_URL = "https://api.x.ai/v1"


class GrokConnector(BaseIntegration):
    """
    Grok (xAI) connector — uses OpenAI-compatible client pointed at api.x.ai.
    Grok has real-time web access and excels at reasoning and current events.
    """

    integration_name = "grok"
    supported_models = [
        "grok-3",
        "grok-3-fast",
        "grok-3-mini",
        "grok-3-mini-fast",
        "grok-2-1212",
        "grok-2-vision-1212",
    ]

    def _api_key_env(self) -> str:
        return "GROK_API_KEY"

    def _default_model(self) -> str:
        return "grok-3"

    def _get_client(self):
        if not OPENAI_CLIENT_AVAILABLE:
            raise RuntimeError("openai package not installed — run: pip install openai")
        return AsyncOpenAI(api_key=self.api_key, base_url=GROK_BASE_URL)

    def _build_messages(
        self, system_prompt: str, messages: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        return [{"role": "system", "content": system_prompt}] + messages

    async def _raw_complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str:
        client = self._get_client()
        response = await client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(system_prompt, messages),
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content

    async def _raw_stream(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        client = self._get_client()
        stream = await client.chat.completions.create(
            model=self.model,
            messages=self._build_messages(system_prompt, messages),
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
