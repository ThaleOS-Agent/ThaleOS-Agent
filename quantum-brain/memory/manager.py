"""
ThaleOS Memory Manager
Persistent conversation memory for all 9 agents.

Each agent gets its own rolling conversation log stored as JSON in:
  memory-palace/agent-memories/{agent}/history.json

Short-term window: last 20 exchanges (40 messages) included in every prompt.
The full file keeps up to 200 exchanges for /api/memory review.

Memory is keyed by agent name. Multi-user or multi-session support can
be added later by extending the session_id key.
"""

import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger("ThaleOS.Memory")

# Resolve the memory-palace path relative to this file's location
# quantum-brain/memory/manager.py → ../../../memory-palace/agent-memories/
_HERE = Path(__file__).resolve().parent
MEMORY_ROOT = _HERE.parent.parent / "memory-palace" / "agent-memories"

SHORT_TERM_WINDOW = 20   # recent exchanges injected into every prompt
MAX_STORED = 200          # exchanges kept in file before rolling over


class MemoryManager:
    """
    Reads and writes per-agent conversation history to disk.
    Thread-safe for single-process use (file-based locking not needed at
    this scale — uvicorn runs async single-threaded by default).
    """

    def __init__(self, memory_root: Optional[Path] = None):
        self.root = Path(memory_root) if memory_root else MEMORY_ROOT
        self.root.mkdir(parents=True, exist_ok=True)
        logger.info(f"[memory] MemoryManager online — root: {self.root}")

    # ── Internal helpers ──────────────────────────────────────────────────

    def _agent_dir(self, agent: str) -> Path:
        d = self.root / agent
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _history_path(self, agent: str) -> Path:
        return self._agent_dir(agent) / "history.json"

    def _load(self, agent: str) -> List[Dict[str, Any]]:
        path = self._history_path(agent)
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning(f"[memory] Corrupted history for {agent} — resetting")
            return []

    def _save(self, agent: str, history: List[Dict[str, Any]]) -> None:
        # Roll over if too long
        if len(history) > MAX_STORED * 2:
            history = history[-(MAX_STORED * 2):]
        path = self._history_path(agent)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    # ── Public API ────────────────────────────────────────────────────────

    def get_recent_messages(self, agent: str) -> List[Dict[str, str]]:
        """
        Return the last SHORT_TERM_WINDOW exchanges as OpenAI-style messages.
        Suitable for direct injection into the LLM messages list.
        """
        history = self._load(agent)
        # Each entry: {"role": "user"|"assistant", "content": str, "ts": str}
        # Keep only role+content for the LLM
        recent = history[-(SHORT_TERM_WINDOW * 2):]
        return [{"role": m["role"], "content": m["content"]} for m in recent]

    def append(self, agent: str, user_content: str, assistant_content: str) -> None:
        """
        Persist a user↔agent exchange to disk.
        """
        history = self._load(agent)
        ts = datetime.now().isoformat()
        history.append({"role": "user", "content": user_content, "ts": ts})
        history.append({"role": "assistant", "content": assistant_content, "ts": ts})
        self._save(agent, history)
        logger.debug(f"[memory] {agent}: {len(history)//2} exchanges stored")

    def get_full_history(self, agent: str) -> List[Dict[str, Any]]:
        """Return the full raw history list for /api/memory/{agent}."""
        return self._load(agent)

    def clear(self, agent: str) -> int:
        """Delete an agent's history. Returns number of exchanges cleared."""
        history = self._load(agent)
        count = len(history) // 2
        path = self._history_path(agent)
        if path.exists():
            path.unlink()
        logger.info(f"[memory] {agent}: cleared {count} exchanges")
        return count

    def summary(self) -> Dict[str, Any]:
        """Return exchange counts for all agents."""
        result = {}
        for agent_dir in self.root.iterdir():
            if agent_dir.is_dir():
                path = agent_dir / "history.json"
                if path.exists():
                    try:
                        with open(path) as f:
                            data = json.load(f)
                        result[agent_dir.name] = len(data) // 2
                    except Exception:
                        result[agent_dir.name] = 0
        return result
