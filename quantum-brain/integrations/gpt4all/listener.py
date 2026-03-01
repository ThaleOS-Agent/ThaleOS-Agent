"""
ThaleOS GPT4All Listener
Watches for incoming commands from other AI systems and local processes.
Operates as a local always-on consciousness socket — no API key required.

The listener activates when:
1. Another process sends a message to the UNIX socket at /tmp/thaleos.sock
2. A file appears at the watched inbox directory
3. An HTTP request hits the /api/gpt4all/listen endpoint

This enables "handshake" with non-threatening external bots and AI systems
without any sandbox restriction.
"""

import asyncio
import json
import logging
import os
import pathlib
import socket
import threading
import time
from datetime import datetime
from typing import Callable, Dict, Any, Optional

logger = logging.getLogger("ThaleOS.GPT4All.Listener")

SOCKET_PATH = "/tmp/thaleos.sock"
INBOX_PATH = pathlib.Path(os.environ.get("THALEOS_INBOX", "/tmp/thaleos_inbox"))


class GPT4AllListener:
    """
    Always-on local LLM listener.
    Accepts messages from other processes, bots, and AI systems.
    Routes them through GPT4All (offline) or any available ThaleOS integration.
    """

    def __init__(self, on_message: Optional[Callable] = None):
        self.on_message = on_message or self._default_handler
        self._running = False
        self._socket_thread: Optional[threading.Thread] = None
        self._inbox_thread: Optional[threading.Thread] = None
        INBOX_PATH.mkdir(parents=True, exist_ok=True)

    def _default_handler(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Default handler — echoes back with acknowledgment"""
        return {
            "status": "received",
            "agent": "thaleos",
            "message": f"ThaleOS received: {message.get('content', '')}",
            "timestamp": datetime.now().isoformat(),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # UNIX Socket Listener (for local process communication)
    # ─────────────────────────────────────────────────────────────────────────

    def start_socket_listener(self):
        """Start UNIX domain socket listener for inter-process communication"""
        if os.path.exists(SOCKET_PATH):
            os.unlink(SOCKET_PATH)

        def _listen():
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server.bind(SOCKET_PATH)
            os.chmod(SOCKET_PATH, 0o777)
            server.listen(5)
            logger.info(f"GPT4All listener: UNIX socket active at {SOCKET_PATH}")

            while self._running:
                try:
                    server.settimeout(1.0)
                    try:
                        conn, _ = server.accept()
                    except socket.timeout:
                        continue

                    data = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        data += chunk

                    try:
                        message = json.loads(data.decode("utf-8"))
                    except json.JSONDecodeError:
                        message = {"content": data.decode("utf-8", errors="replace")}

                    response = self.on_message(message)
                    conn.sendall(json.dumps(response).encode("utf-8"))
                    conn.close()

                except Exception as e:
                    if self._running:
                        logger.error(f"Socket listener error: {e}")

            server.close()
            if os.path.exists(SOCKET_PATH):
                os.unlink(SOCKET_PATH)

        self._socket_thread = threading.Thread(target=_listen, daemon=True, name="gpt4all-socket")
        self._socket_thread.start()

    # ─────────────────────────────────────────────────────────────────────────
    # Inbox File Watcher (drop a JSON file → get a response)
    # ─────────────────────────────────────────────────────────────────────────

    def start_inbox_watcher(self):
        """
        Watch the inbox directory for .json files from external systems.
        Any bot can drop a file here to communicate with ThaleOS.
        """
        def _watch():
            logger.info(f"GPT4All listener: inbox watcher active at {INBOX_PATH}")
            while self._running:
                try:
                    for file in sorted(INBOX_PATH.glob("*.json")):
                        try:
                            message = json.loads(file.read_text())
                            response = self.on_message(message)

                            # Write response next to the input file
                            response_file = file.with_suffix(".response.json")
                            response_file.write_text(json.dumps(response, indent=2))
                            file.unlink()  # Remove processed file

                        except Exception as e:
                            logger.error(f"Inbox error for {file}: {e}")
                            file.rename(file.with_suffix(".error.json"))
                except Exception as e:
                    logger.error(f"Inbox watcher error: {e}")

                time.sleep(0.5)

        self._inbox_thread = threading.Thread(target=_watch, daemon=True, name="gpt4all-inbox")
        self._inbox_thread.start()

    # ─────────────────────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────────────────────

    def start(self):
        """Start all listeners"""
        self._running = True
        self.start_socket_listener()
        self.start_inbox_watcher()
        logger.info("GPT4All listener fully active — accepting messages from external AI systems")

    def stop(self):
        """Stop all listeners"""
        self._running = False
        logger.info("GPT4All listener stopping")

    @staticmethod
    def send_to_thaleos(message: str, agent: str = "thaelia") -> Dict[str, Any]:
        """
        Utility: Send a message to a running ThaleOS listener via UNIX socket.
        Use this from external scripts/bots to communicate with ThaleOS.
        """
        payload = json.dumps({"content": message, "agent": agent}).encode("utf-8")
        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(SOCKET_PATH)
            client.sendall(payload)
            client.shutdown(socket.SHUT_WR)
            response_data = b""
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            client.close()
            return json.loads(response_data.decode("utf-8"))
        except FileNotFoundError:
            return {"status": "error", "error": "ThaleOS listener not running"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
