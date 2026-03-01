"""
ThaleOS × GPT4All Integration
Local LLM connector — no API key required, runs fully offline.
Activation spell handshake for local models.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator

from ..base_integration import BaseIntegration

logger = logging.getLogger("ThaleOS.Integrations.GPT4All")

try:
    from gpt4all import GPT4All
    GPT4ALL_AVAILABLE = True
except ImportError:
    GPT4ALL_AVAILABLE = False
    logger.warning("gpt4all package not installed — run: pip install gpt4all")


# Default model to download/use if none specified
DEFAULT_GPT4ALL_MODEL = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"


class GPT4AllConnector(BaseIntegration):
    """
    GPT4All local LLM connector.
    Runs entirely offline — all computation is local.
    No sandbox, no API limits, full system access.
    """

    integration_name = "gpt4all"
    supported_models = [
        "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
        "Phi-3-mini-4k-instruct.Q4_0.gguf",
        "mistral-7b-instruct-v0.1.Q4_0.gguf",
        "orca-mini-3b-gguf2-q4_0.gguf",
    ]

    def __init__(self, model: Optional[str] = None, model_path: Optional[str] = None):
        # GPT4All doesn't need an API key
        self.api_key = "local"
        self.model = model or DEFAULT_GPT4ALL_MODEL
        self.model_path = model_path
        self._gpt4all_instance = None
        self._active_spell = None
        self._handshake_complete = False
        logger.info(f"[gpt4all] Local LLM initialized: {self.model}")

    def _api_key_env(self) -> str:
        return "GPT4ALL_MODEL_PATH"

    def _default_model(self) -> str:
        return DEFAULT_GPT4ALL_MODEL

    def is_available(self) -> bool:
        return GPT4ALL_AVAILABLE

    def _get_instance(self):
        if not GPT4ALL_AVAILABLE:
            raise RuntimeError("gpt4all package not installed — run: pip install gpt4all")
        if self._gpt4all_instance is None:
            kwargs = {"model_name": self.model}
            if self.model_path:
                kwargs["model_path"] = self.model_path
            logger.info(f"[gpt4all] Loading model: {self.model} (first use — may download)")
            self._gpt4all_instance = GPT4All(**kwargs)
        return self._gpt4all_instance

    def _format_prompt(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """Format messages into a single prompt string for GPT4All"""
        lines = [f"### System\n{system_prompt}\n"]
        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            lines.append(f"### {role}\n{content}\n")
        lines.append("### Assistant\n")
        return "\n".join(lines)

    async def _raw_complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str:
        instance = self._get_instance()
        prompt = self._format_prompt(system_prompt, messages)

        # GPT4All is synchronous — run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: instance.generate(
                prompt,
                max_tokens=max_tokens,
                temp=temperature,
            ),
        )
        return response

    async def _raw_stream(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        instance = self._get_instance()
        prompt = self._format_prompt(system_prompt, messages)

        # GPT4All streaming via generator — wrap in async
        loop = asyncio.get_event_loop()
        queue: asyncio.Queue = asyncio.Queue()

        def generate_to_queue():
            try:
                with instance.chat_session():
                    for token in instance.generate(
                        prompt,
                        max_tokens=max_tokens,
                        temp=temperature,
                        streaming=True,
                    ):
                        loop.call_soon_threadsafe(queue.put_nowait, token)
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)  # sentinel

        import threading
        t = threading.Thread(target=generate_to_queue, daemon=True)
        t.start()

        while True:
            token = await queue.get()
            if token is None:
                break
            yield token
