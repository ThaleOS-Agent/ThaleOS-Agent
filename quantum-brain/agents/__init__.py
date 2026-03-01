"""
ThaleOS Agent Registry
All nine quantum agents, wired to LLM integrations via activation spell handshake.
"""

import logging
from typing import Dict, Any, Optional

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
        return {
            agent_id: agent.get_status()
            for agent_id, agent in self._agents.items()
        }

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

        if hasattr(agent, "process_task"):
            import inspect
            sig = inspect.signature(agent.process_task)
            if "integration" in sig.parameters:
                result = await agent.process_task(task, integration=integration)
            else:
                result = await agent.process_task(task)
        else:
            return {"status": "error", "error": f"Agent {agent_id} has no process_task method"}

        return {"status": "success", **result}


# Singleton — created after integration manager is available
_registry: Optional[AgentRegistry] = None


def get_registry(integration_manager=None) -> AgentRegistry:
    global _registry
    if _registry is None:
        _registry = AgentRegistry(integration_manager)
    return _registry
