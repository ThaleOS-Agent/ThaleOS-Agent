"""
ThaleOS Agent Registry
All nine quantum agents, wired to LLM integrations via activation spell handshake.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from memory import MemoryManager
from .manifest import AGENT_MANIFESTS
from .thaelia.agent import ThaeliaAgent
from .chronagate.agent import ChronogateAgent
from .utilix.agent import UtilixAgent
from .scribe.agent import ScribeAgent
from .oracle.agent import OracleAgent
from .phantom.agent import PhantomAgent
from .sage.agent import SageAgent
from .nexus.agent import NexusAgent
from .scales.agent import ScalesAgent

logger = logging.getLogger("ThaleOS.Agents")


class AgentRegistry:
    """
    Central registry for all ThaleOS quantum agents.
    Routes requests to the correct agent with LLM integration injected.
    """

    def __init__(self, integration_manager=None):
        self._integration_manager = integration_manager
        self._memory = MemoryManager()
        self._agents: Dict[str, Any] = {
            "thaelia":    ThaeliaAgent(),
            "chronagate": ChronogateAgent(),
            "utilix":     UtilixAgent(),
            "scribe":     ScribeAgent(),
            "oracle":     OracleAgent(),
            "phantom":    PhantomAgent(),
            "sage":       SageAgent(),
            "nexus":      NexusAgent(),
            "scales":     ScalesAgent(),
        }
        logger.info(f"AgentRegistry initialized — {len(self._agents)} agents online")

    def get(self, agent_id: str) -> Optional[Any]:
        return self._agents.get(agent_id.lower())

    def list_agents(self) -> Dict[str, Dict]:
        """Return full manifest data for all agents, merged with live status."""
        result = {}
        for agent_id, agent in self._agents.items():
            manifest = AGENT_MANIFESTS.get(agent_id)
            if manifest:
                data = manifest.to_dict()
            else:
                data = {"id": agent_id}
            # Merge in live status if available
            if hasattr(agent, "get_status"):
                data["live_status"] = agent.get_status()
            result[agent_id] = data
        return result

    def get_manifest(self, agent_id: str):
        """Return the AgentManifest for a given agent_id, or None."""
        return AGENT_MANIFESTS.get(agent_id.lower())

    def _get_integration(self, preferred: Optional[str] = None):
        """Get best available LLM integration"""
        if self._integration_manager is None:
            return None
        return self._integration_manager.best_available(preferred)

    async def invoke(
        self,
        agent_id: str,
        task: Dict[str, Any],
        preferred_integration: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Invoke an agent with a task.
        Injects conversation history from MemoryManager before the call,
        then persists the exchange after.
        The activation spell handshake is managed by the integration layer.
        """
        agent = self.get(agent_id)
        if agent is None:
            return {
                "status": "error",
                "error": f"Unknown agent: {agent_id}",
                "available": list(self._agents.keys()),
            }

        integration = self._get_integration(preferred_integration)

        # Inject recent memory into the task so agents can pass it to the LLM
        user_content = task.get("content", task.get("task", ""))
        if user_content and "history" not in task:
            task = {**task, "history": self._memory.get_recent_messages(agent_id)}

        if hasattr(agent, "process_task"):
            import inspect
            sig = inspect.signature(agent.process_task)
            if "integration" in sig.parameters:
                result = await agent.process_task(task, integration=integration)
            else:
                result = await agent.process_task(task)
        else:
            return {"status": "error", "error": f"Agent {agent_id} has no process_task method"}

        # Persist the exchange
        response_text = result.get("response", "")
        if user_content and response_text:
            self._memory.append(agent_id, user_content, response_text)

        # Auto-persist artifact if agent returned one
        artifact_data = result.get("artifact")
        if artifact_data and isinstance(artifact_data, dict):
            try:
                import db
                user_id = task.get("user_id", "anonymous")
                artifact_id = str(uuid.uuid4())
                db.execute(
                    "INSERT OR IGNORE INTO artifacts (id, user_id, agent_id, artifact_type, title, content, language, version, parent_id, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (
                        artifact_id,
                        user_id,
                        agent_id,
                        artifact_data.get("type", "markdown"),
                        artifact_data.get("title", "Artifact"),
                        artifact_data.get("content", ""),
                        artifact_data.get("language"),
                        1,
                        None,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                result = {**result, "artifact_id": artifact_id}
                logger.info(f"[registry] artifact auto-saved: {artifact_id} type={artifact_data.get('type')}")
            except Exception as e:
                logger.warning(f"[registry] artifact save failed: {e}")

        return {"status": "success", **result}

    @property
    def memory(self) -> MemoryManager:
        return self._memory


# Singleton — created after integration manager is available
_registry: Optional[AgentRegistry] = None


def get_registry(integration_manager=None) -> AgentRegistry:
    global _registry
    if _registry is None:
        _registry = AgentRegistry(integration_manager)
    return _registry
