"""
ThaleOS × Perplexity AI Integration
Online search-augmented LLM with activation spell handshake.
"""

import logging
from typing import Dict, Any, List, Optional, AsyncGenerator

from ..base_integration import BaseIntegration

logger = logging.getLogger("ThaleOS.Integrations.Perplexity")

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logger.warning("httpx package not installed — run: pip install httpx")

PERPLEXITY_API_BASE = "https://api.perplexity.ai"


class PerplexityConnector(BaseIntegration):
    """
    Perplexity AI connector — search-augmented LLM responses.
    Ideal for ORACLE (web-grounded predictions) and SAGE (deep research).
    """

    integration_name = "perplexity"
    supported_models = [
        "llama-3.1-sonar-large-128k-online",
        "llama-3.1-sonar-small-128k-online",
        "llama-3.1-sonar-huge-128k-online",
    ]

    def _api_key_env(self) -> str:
        return "PERPLEXITY_API_KEY"

    def _default_model(self) -> str:
        return "llama-3.1-sonar-large-128k-online"

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
        if not HTTPX_AVAILABLE:
            raise RuntimeError("httpx not installed")

        payload = {
            "model": self.model,
            "messages": self._build_messages(system_prompt, messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{PERPLEXITY_API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _raw_stream(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        if not HTTPX_AVAILABLE:
            raise RuntimeError("httpx not installed")

        import json as _json

        payload = {
            "model": self.model,
            "messages": self._build_messages(system_prompt, messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                f"{PERPLEXITY_API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunk = line[6:]
                        if chunk == "[DONE]":
                            break
                        try:
                            data = _json.loads(chunk)
                            delta = data["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            pass
