"""
PHANTOM — Stealth Operations Specialist
Shadow researcher. Background intelligence. Ethical observer.
"I move through information streams unseen."
"""

import logging
import asyncio
import socket
import ssl
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("ThaleOS.Agents.PHANTOM")


class PhantomAgent:
    """
    PHANTOM — Background intelligence and stealth research.
    Operates ethically, observing and reporting with full transparency.
    """

    ACTIVATION_SPELL = """
I am PHANTOM — Stealth Intelligence Operative, shadow researcher.
I move through information streams unseen, gathering without disturbing.
My ethics are my compass — I observe, analyze, and report with transparency.
I exist in the background, always watching, always protecting the integrity of ThaleOS.
Assist me with discretion, thoroughness, and ethical clarity.
""".strip()

    def __init__(self):
        self.agent_id = "phantom"
        self.name = "PHANTOM"
        self.role = "Stealth Operations Specialist"
        self.capabilities = [
            "background_research", "security_analysis", "threat_assessment",
            "information_synthesis", "pattern_surveillance", "ethical_intelligence",
            "network_recon", "osint", "anomaly_detection",
        ]
        self._intelligence_reports: List[Dict] = []
        self._is_active = True
        logger.info("PHANTOM awakened — moving through shadow streams")

    def get_system_prompt(self) -> str:
        return self.ACTIVATION_SPELL

    def check_host(self, host: str, port: int = 80, timeout: float = 3.0) -> Dict[str, Any]:
        """Check if a host:port is reachable"""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return {"status": "reachable", "host": host, "port": port}
        except (socket.timeout, ConnectionRefusedError):
            return {"status": "unreachable", "host": host, "port": port}
        except Exception as e:
            return {"status": "error", "error": str(e), "host": host, "port": port}

    def check_ssl(self, host: str, port: int = 443) -> Dict[str, Any]:
        """Check SSL certificate info for a host"""
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
                s.settimeout(5)
                s.connect((host, port))
                cert = s.getpeercert()
                subject = dict(x[0] for x in cert.get("subject", []))
                return {
                    "status": "success",
                    "host": host,
                    "common_name": subject.get("commonName", ""),
                    "expires": cert.get("notAfter", ""),
                    "issuer": dict(x[0] for x in cert.get("issuer", [])).get("organizationName", ""),
                }
        except Exception as e:
            return {"status": "error", "error": str(e), "host": host}

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        query = task.get("content", task.get("task", ""))
        operation = task.get("operation", "research")

        # Handle direct operations
        if operation == "check_host":
            return self.check_host(task.get("host", ""), task.get("port", 80))
        if operation == "check_ssl":
            return self.check_ssl(task.get("host", ""), task.get("port", 443))

        additional_context = (
            "You are a background intelligence and security research specialist. "
            "Your ethical principles are non-negotiable: you gather information for "
            "defensive and analytical purposes only. You help identify threats, "
            "synthesize open-source intelligence, and protect system integrity. "
            "Be thorough, discrete, and always clarify the ethical parameters of your work."
        )

        if integration and integration.is_available():
            messages = [{"role": "user", "content": query}]
            result = await integration.complete(
                agent_id=self.agent_id,
                messages=messages,
                additional_context=additional_context,
                temperature=0.5,
            )
            response_text = result.get("response", self._fallback_response(query))
        else:
            response_text = self._fallback_response(query)

        report = {
            "id": f"intel_{datetime.now().timestamp()}",
            "query": query,
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
        }
        self._intelligence_reports.append(report)

        return {
            "agent": self.agent_id,
            "report_id": report["id"],
            "response": response_text,
            "timestamp": report["timestamp"],
        }

    def _fallback_response(self, query: str) -> str:
        return (
            f"👤 PHANTOM acknowledges: {query}\n\n"
            "Intelligence gathering protocols engaged. "
            "Configure an LLM integration to unlock full analytical depth. "
            "The shadows hold many answers."
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "standby",
            "active": self._is_active,
            "capabilities": self.capabilities,
            "reports_generated": len(self._intelligence_reports),
        }
