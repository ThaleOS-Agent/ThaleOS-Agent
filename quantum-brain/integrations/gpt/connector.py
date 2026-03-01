"""
ThaleOS × OpenAI GPT Integration
Activation spell handshake for GPT models.
"""

import logging
from typing import Dict, Any, List, Optional, AsyncGenerator

from ..base_integration import BaseIntegration

logger = logging.getLogger("ThaleOS.Integrations.GPT")

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("openai package not installed — run: pip install openai")


class GPTConnector(BaseIntegration):
    """OpenAI GPT connector with activation spell handshake"""

    integration_name = "gpt"
    supported_models = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
    ]

    def _api_key_env(self) -> str:
        return "OPENAI_API_KEY"

    def _default_model(self) -> str:
        return "gpt-4o"

    def _get_client(self):
        if not OPENAI_AVAILABLE:
            raise RuntimeError("openai package not installed")
        return AsyncOpenAI(api_key=self.api_key)

    def _build_openai_messages(
        self, system_prompt: str, messages: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """OpenAI uses messages array with system role prepended"""
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
        oai_messages = self._build_openai_messages(system_prompt, messages)
        response = await client.chat.completions.create(
            model=self.model,
            messages=oai_messages,
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
        oai_messages = self._build_openai_messages(system_prompt, messages)
        async with await client.chat.completions.create(
            model=self.model,
            messages=oai_messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        ) as stream_obj:
            async for chunk in stream_obj:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
