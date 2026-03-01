"""
ThaleOS × GitHub Copilot / GitHub Models Integration
Uses the GitHub Models API (OpenAI-compatible endpoint) authenticated
with a GitHub personal access token. Gives access to GPT-4o, o1, Llama,
Mistral and more — all via your existing GitHub account.

Also bridges to GitHub Copilot CLI for code-aware interactions.

Endpoint: https://models.inference.ai.azure.com
Auth: GitHub PAT with `models:read` or `read:copilot` scope
"""

import logging
import os
from typing import Dict, Any, List, Optional, AsyncGenerator

from ..base_integration import BaseIntegration

logger = logging.getLogger("ThaleOS.Integrations.Copilot")

try:
    from openai import AsyncOpenAI
    OPENAI_CLIENT_AVAILABLE = True
except ImportError:
    OPENAI_CLIENT_AVAILABLE = False

GITHUB_MODELS_BASE = "https://models.inference.ai.azure.com"


class CopilotConnector(BaseIntegration):
    """
    GitHub Copilot / GitHub Models connector.
    Authenticated with a GitHub PAT — gives access to premium models
    through GitHub's model marketplace endpoint.
    """

    integration_name = "copilot"
    supported_models = [
        "gpt-4o",
        "gpt-4o-mini",
        "o1-preview",
        "o1-mini",
        "meta-llama-3.1-70b-instruct",
        "mistral-large",
        "mistral-nemo",
        "phi-3.5-mini-instruct",
    ]

    def _api_key_env(self) -> str:
        return "GITHUB_TOKEN"

    def _default_model(self) -> str:
        return "gpt-4o"

    def _get_client(self):
        if not OPENAI_CLIENT_AVAILABLE:
            raise RuntimeError("openai package not installed")
        return AsyncOpenAI(
            api_key=self.api_key,
            base_url=GITHUB_MODELS_BASE,
        )

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
