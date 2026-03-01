"""
ThaleOS × Siri Integration
Bridges Apple Siri (via Shortcuts) to the ThaleOS listener.

How it works:
  1. A Siri Shortcut on iPhone/Mac sends a POST to /api/siri/message
  2. ThaleOS processes it through the best available agent
  3. The response is returned as text — Siri reads it aloud via Shortcuts "Speak Text"

Setting up the Siri Shortcut:
  1. Open Shortcuts app on iPhone or Mac
  2. Create new shortcut → Add Action → "Get Contents of URL"
  3. URL: http://<your-ip>:8099/api/siri/message
  4. Method: POST
  5. Request Body: JSON → {"content": [Shortcut Input], "agent": "thaelia"}
  6. Add "Speak Text" action with the result
  7. Add to Siri with a phrase like "Ask ThaleOS"

For local network access, replace <your-ip> with your Mac's local IP.
For remote access, expose port 8099 via ngrok or Cloudflare Tunnel.
"""

import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger("ThaleOS.Integrations.Siri")

# Siri-specific response formatting
SIRI_MAX_CHARS = 500  # Siri TTS works best with shorter responses


class SiriConnector:
    """
    Siri bridge — not an LLM connector itself, but a protocol adapter.
    Receives voice input from Siri Shortcuts, routes to ThaleOS agents,
    and returns Siri-optimised (concise, spoken-word-friendly) responses.
    """

    integration_name = "siri"

    def __init__(self):
        self._request_count = 0
        logger.info("[siri] Siri bridge connector initialized")

    def is_available(self) -> bool:
        return True  # Always available — no API key needed

    def format_for_speech(self, text: str) -> str:
        """
        Trim and clean a response for Siri TTS.
        Removes markdown, shortens to 500 chars, adds natural pauses.
        """
        import re
        # Remove markdown
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'`[^`]*`', lambda m: m.group(0).strip('`'), text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'\n{2,}', '. ', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) > SIRI_MAX_CHARS:
            # Cut at sentence boundary
            cut = text[:SIRI_MAX_CHARS]
            last_dot = cut.rfind('.')
            if last_dot > 200:
                text = cut[:last_dot + 1]
            else:
                text = cut.rstrip() + "..."

        return text

    def parse_voice_command(self, text: str) -> Dict[str, Any]:
        """
        Parse a Siri voice command to extract agent routing hints.
        "Ask THAELIA what should I focus on today" → agent=thaelia
        "Tell ORACLE to predict this week's revenue" → agent=oracle
        """
        text_lower = text.lower()

        agent_keywords = {
            "thaelia": ["thaelia", "guide", "harmony"],
            "chronagate": ["chronagate", "schedule", "calendar", "time", "deadline"],
            "utilix": ["utilix", "file", "computer", "system", "run"],
            "scribe": ["scribe", "write", "email", "draft", "document"],
            "oracle": ["oracle", "predict", "forecast", "analyse", "analyze"],
            "phantom": ["phantom", "research", "background", "investigate"],
            "sage": ["sage", "explain", "what is", "research", "learn"],
            "nexus": ["nexus", "money", "business", "invest", "revenue"],
            "scales": ["scales", "legal", "contract", "law", "rights"],
        }

        detected_agent = "thaelia"
        for agent, keywords in agent_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected_agent = agent
                break

        # Strip "ask [agent]" / "tell [agent]" prefix from the actual content
        import re
        clean = re.sub(
            r'^(ask|tell|have|get)\s+(thaelia|chronagate|utilix|scribe|oracle|phantom|sage|nexus|scales)\s+(to\s+)?',
            '', text, flags=re.IGNORECASE
        ).strip()
        if not clean:
            clean = text

        return {"content": clean, "agent": detected_agent, "raw": text}

    def get_shortcut_config(self, host: str = "localhost", port: int = 8099) -> Dict[str, Any]:
        """
        Returns the configuration needed to set up a Siri Shortcut.
        """
        return {
            "name": "Ask ThaleOS",
            "trigger_phrase": "Ask ThaleOS",
            "steps": [
                {
                    "action": "Ask for Input",
                    "prompt": "What would you like to ask ThaleOS?",
                    "variable": "UserInput"
                },
                {
                    "action": "Get Contents of URL",
                    "url": f"http://{host}:{port}/api/siri/message",
                    "method": "POST",
                    "body": {
                        "content": "{{UserInput}}",
                        "agent": "thaelia",
                        "source": "siri"
                    }
                },
                {
                    "action": "Speak Text",
                    "text": "{{result.response}}"
                }
            ],
            "notes": (
                f"Replace {host} with your Mac's local IP (System Preferences → Network) "
                f"for iPhone access. Or expose port {port} via ngrok/Cloudflare Tunnel for remote use."
            )
        }

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.integration_name,
            "available": True,
            "type": "voice_bridge",
            "endpoint": "/api/siri/message",
            "description": "Apple Siri Shortcuts bridge — no API key required",
        }
