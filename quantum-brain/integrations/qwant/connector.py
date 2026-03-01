"""
ThaleOS × Qwant Search Integration
Privacy-first search engine — no user tracking, no filter bubble.
Used by ORACLE (research-backed predictions) and SAGE (live knowledge).
Qwant's API returns web results, news, and social results.
"""

import logging
import json as _json
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime

from ..base_integration import BaseIntegration

logger = logging.getLogger("ThaleOS.Integrations.Qwant")

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

QWANT_API_BASE = "https://api.qwant.com/v3"
QWANT_HEADERS = {
    "User-Agent": "ThaleOS-QuantumIntelligence/1.0 (compatible; ThaleOS)",
}


class QwantConnector(BaseIntegration):
    """
    Qwant search connector.
    Provides privacy-respecting web search results to augment agent responses.
    No API key required for basic use — Qwant is open for reasonable query volumes.
    """

    integration_name = "qwant"
    supported_models = ["web", "news", "social", "images"]

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # Qwant doesn't require an API key for basic queries
        self.api_key = api_key or ""
        self.model = model or "web"  # search type: web | news | images | social
        self._active_spell = None
        self._handshake_complete = False
        logger.info("[qwant] Privacy-first search connector initialized")

    def _api_key_env(self) -> str:
        return "QWANT_API_KEY"

    def _default_model(self) -> str:
        return "web"

    def is_available(self) -> bool:
        return HTTPX_AVAILABLE

    async def search(
        self,
        query: str,
        search_type: str = "web",
        count: int = 5,
        locale: str = "en_GB",
    ) -> Dict[str, Any]:
        """
        Perform a Qwant search and return structured results.
        """
        if not HTTPX_AVAILABLE:
            return {"status": "error", "error": "httpx not installed"}

        params = {
            "q": query,
            "count": count,
            "locale": locale,
            "offset": 0,
            "device": "desktop",
        }

        headers = dict(QWANT_HEADERS)
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = f"{QWANT_API_BASE}/search/{search_type}"

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

            results = []
            items = (
                data.get("data", {})
                    .get("result", {})
                    .get("items", {})
                    .get("mainline", [])
            )
            for group in items:
                for item in group.get("items", []):
                    if item.get("type") in ("web", "news"):
                        results.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "snippet": item.get("desc", item.get("content", "")),
                            "date": item.get("date", ""),
                        })

            return {
                "status": "success",
                "query": query,
                "type": search_type,
                "count": len(results),
                "results": results[:count],
                "timestamp": datetime.now().isoformat(),
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"[qwant] HTTP error: {e.response.status_code}")
            return {"status": "error", "error": f"HTTP {e.response.status_code}", "query": query}
        except Exception as e:
            logger.error(f"[qwant] Search error: {e}")
            return {"status": "error", "error": str(e), "query": query}

    def _format_results_for_context(self, results: Dict[str, Any]) -> str:
        """Format search results as context for LLM prompts"""
        if results.get("status") != "success" or not results.get("results"):
            return "No search results available."
        lines = [f"Web search results for: '{results['query']}'", ""]
        for i, r in enumerate(results["results"], 1):
            lines.append(f"{i}. {r['title']}")
            lines.append(f"   {r['url']}")
            if r.get("snippet"):
                lines.append(f"   {r['snippet'][:200]}")
            lines.append("")
        return "\n".join(lines)

    async def _raw_complete(self, system_prompt, messages, max_tokens=2048, temperature=0.7, stream=False):
        # Qwant is search-only — extract the query and return formatted results
        query = messages[-1].get("content", "") if messages else ""
        results = await self.search(query)
        return self._format_results_for_context(results)

    async def _raw_stream(self, system_prompt, messages, max_tokens=2048, temperature=0.7):
        result = await self._raw_complete(system_prompt, messages, max_tokens, temperature)
        yield result
