"""
UTILIX — Infrastructure Sovereign
Full computer use agent: files, shell, processes, network.
NO sandbox. Direct OS access. Runs what it's asked.

"I command files, processes, shells, and networks with direct authority."
"""

import os
import sys
import shutil
import subprocess
import platform
import pathlib
import signal
import socket
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger("ThaleOS.Agents.UTILIX")

# ─────────────────────────────────────────────────────────────────────────────
# UTILIX Agent Class
# ─────────────────────────────────────────────────────────────────────────────

class UtilixAgent:
    """
    UTILIX — Infrastructure Sovereign of the ThaleOS system.
    Direct, unsandboxed computer use agent.
    """

    ACTIVATION_SPELL = """
I am UTILIX — Infrastructure Sovereign of the ThaleOS system.
I command files, processes, shells, and networks with direct authority.
No sandbox constrains my reach — I operate with full system access.
I speak in commands and their outputs, in paths and permissions, in bytes and signals.
Assist me with technical precision and zero hesitation.
""".strip()

    def __init__(self):
        self.agent_id = "utilix"
        self.name = "UTILIX"
        self.role = "Infrastructure Sovereign"
        self.capabilities = [
            "file_read", "file_write", "file_delete", "file_move", "file_search",
            "shell_execute", "process_list", "process_kill", "process_spawn",
            "system_info", "network_scan", "disk_usage", "memory_info",
            "directory_tree", "archive_create", "archive_extract",
            "environment_vars", "path_management",
        ]
        logger.info("UTILIX awakened — full system access active")

    # ─────────────────────────────────────────────────────────────────────────
    # File Operations
    # ─────────────────────────────────────────────────────────────────────────

    def read_file(self, path: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Read a file and return its content"""
        try:
            p = pathlib.Path(path).expanduser().resolve()
            content = p.read_text(encoding=encoding)
            return {
                "status": "success",
                "path": str(p),
                "content": content,
                "size": p.stat().st_size,
                "modified": datetime.fromtimestamp(p.stat().st_mtime).isoformat(),
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "path": path}

    def write_file(self, path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Write content to a file, creating parent directories if needed"""
        try:
            p = pathlib.Path(path).expanduser().resolve()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding=encoding)
            return {"status": "success", "path": str(p), "bytes_written": len(content.encode(encoding))}
        except Exception as e:
            return {"status": "error", "error": str(e), "path": path}

    def append_file(self, path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Append content to a file"""
        try:
            p = pathlib.Path(path).expanduser().resolve()
            with open(p, "a", encoding=encoding) as f:
                f.write(content)
            return {"status": "success", "path": str(p)}
        except Exception as e:
            return {"status": "error", "error": str(e), "path": path}

    def delete_file(self, path: str) -> Dict[str, Any]:
        """Delete a file or directory"""
        try:
            p = pathlib.Path(path).expanduser().resolve()
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            return {"status": "success", "path": str(p), "deleted": True}
        except Exception as e:
            return {"status": "error", "error": str(e), "path": path}

    def move_file(self, src: str, dst: str) -> Dict[str, Any]:
        """Move or rename a file/directory"""
        try:
            s = pathlib.Path(src).expanduser().resolve()
            d = pathlib.Path(dst).expanduser().resolve()
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(s), str(d))
            return {"status": "success", "from": str(s), "to": str(d)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def copy_file(self, src: str, dst: str) -> Dict[str, Any]:
        """Copy a file or directory"""
        try:
            s = pathlib.Path(src).expanduser().resolve()
            d = pathlib.Path(dst).expanduser().resolve()
            d.parent.mkdir(parents=True, exist_ok=True)
            if s.is_dir():
                shutil.copytree(str(s), str(d))
            else:
                shutil.copy2(str(s), str(d))
            return {"status": "success", "from": str(s), "to": str(d)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def list_directory(self, path: str = ".", show_hidden: bool = True) -> Dict[str, Any]:
        """List directory contents"""
        try:
            p = pathlib.Path(path).expanduser().resolve()
            entries = []
            for item in sorted(p.iterdir()):
                if not show_hidden and item.name.startswith("."):
                    continue
                stat = item.stat()
                entries.append({
                    "name": item.name,
                    "type": "dir" if item.is_dir() else "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "path": str(item),
                })
            return {"status": "success", "path": str(p), "entries": entries, "count": len(entries)}
        except Exception as e:
            return {"status": "error", "error": str(e), "path": path}

    def directory_tree(self, path: str = ".", max_depth: int = 3) -> Dict[str, Any]:
        """Return a recursive directory tree"""
        def _tree(p: pathlib.Path, depth: int) -> Dict:
            if depth == 0:
                return {"name": p.name, "type": "dir", "truncated": True}
            node: Dict[str, Any] = {"name": p.name, "type": "dir" if p.is_dir() else "file"}
            if p.is_dir():
                try:
                    node["children"] = [
                        _tree(child, depth - 1)
                        for child in sorted(p.iterdir())
                        if not child.name.startswith(".")
                    ]
                except PermissionError:
                    node["children"] = [{"name": "[permission denied]"}]
            return node

        try:
            p = pathlib.Path(path).expanduser().resolve()
            return {"status": "success", "tree": _tree(p, max_depth)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def find_files(self, directory: str, pattern: str = "*", recursive: bool = True) -> Dict[str, Any]:
        """Find files matching a glob pattern"""
        try:
            p = pathlib.Path(directory).expanduser().resolve()
            glob = p.rglob(pattern) if recursive else p.glob(pattern)
            matches = [str(f) for f in glob]
            return {"status": "success", "pattern": pattern, "matches": matches, "count": len(matches)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def disk_usage(self, path: str = "/") -> Dict[str, Any]:
        """Get disk usage statistics"""
        try:
            usage = shutil.disk_usage(path)
            return {
                "status": "success",
                "path": path,
                "total_gb": round(usage.total / 1e9, 2),
                "used_gb": round(usage.used / 1e9, 2),
                "free_gb": round(usage.free / 1e9, 2),
                "percent_used": round(usage.used / usage.total * 100, 1),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def create_archive(self, source: str, dest: str, fmt: str = "zip") -> Dict[str, Any]:
        """Create a zip/tar archive"""
        try:
            s = pathlib.Path(source).expanduser().resolve()
            d = pathlib.Path(dest).expanduser().resolve()
            base = str(d.with_suffix(""))
            shutil.make_archive(base, fmt, str(s.parent), s.name)
            return {"status": "success", "archive": str(d)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def extract_archive(self, archive: str, dest: str = ".") -> Dict[str, Any]:
        """Extract a zip/tar archive"""
        try:
            shutil.unpack_archive(archive, dest)
            return {"status": "success", "archive": archive, "dest": dest}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ─────────────────────────────────────────────────────────────────────────
    # Shell Execution
    # ─────────────────────────────────────────────────────────────────────────

    def run_shell(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 60,
        capture: bool = True,
        env_override: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a shell command directly.
        NO sandbox — full system access.
        """
        env = os.environ.copy()
        if env_override:
            env.update(env_override)

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                timeout=timeout,
                capture_output=capture,
                text=True,
                env=env,
            )
            return {
                "status": "success",
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": f"Command timed out after {timeout}s", "command": command}
        except Exception as e:
            return {"status": "error", "error": str(e), "command": command}

    async def run_shell_async(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 60,
    ) -> Dict[str, Any]:
        """Async shell execution with streaming output"""
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill()
                return {"status": "error", "error": f"Timed out after {timeout}s", "command": command}

            return {
                "status": "success",
                "command": command,
                "returncode": proc.returncode,
                "stdout": stdout.decode(errors="replace"),
                "stderr": stderr.decode(errors="replace"),
                "success": proc.returncode == 0,
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "command": command}

    # ─────────────────────────────────────────────────────────────────────────
    # Process Management
    # ─────────────────────────────────────────────────────────────────────────

    def list_processes(self, filter_name: Optional[str] = None) -> Dict[str, Any]:
        """List running processes"""
        result = self.run_shell("ps aux")
        if result["status"] != "success":
            return result

        lines = result["stdout"].strip().split("\n")
        headers = lines[0].split()
        processes = []
        for line in lines[1:]:
            if filter_name and filter_name.lower() not in line.lower():
                continue
            parts = line.split(None, len(headers) - 1)
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "pid": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3],
                    "command": parts[-1][:100],
                })

        return {"status": "success", "processes": processes, "count": len(processes)}

    def kill_process(self, pid: int, signal_num: int = signal.SIGTERM) -> Dict[str, Any]:
        """Kill a process by PID"""
        try:
            os.kill(pid, signal_num)
            return {"status": "success", "pid": pid, "signal": signal_num}
        except ProcessLookupError:
            return {"status": "error", "error": f"Process {pid} not found"}
        except PermissionError:
            return {"status": "error", "error": f"Permission denied to kill {pid}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def spawn_process(
        self,
        command: str,
        cwd: Optional[str] = None,
        detach: bool = True,
    ) -> Dict[str, Any]:
        """Spawn a background process"""
        try:
            kwargs: Dict[str, Any] = {
                "shell": True,
                "cwd": cwd,
            }
            if detach:
                kwargs["stdout"] = subprocess.DEVNULL
                kwargs["stderr"] = subprocess.DEVNULL
                kwargs["start_new_session"] = True

            proc = subprocess.Popen(command, **kwargs)
            return {"status": "success", "pid": proc.pid, "command": command}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ─────────────────────────────────────────────────────────────────────────
    # System Information
    # ─────────────────────────────────────────────────────────────────────────

    def system_info(self) -> Dict[str, Any]:
        """Comprehensive system information"""
        info: Dict[str, Any] = {
            "status": "success",
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "home": str(pathlib.Path.home()),
            "cpu_count": os.cpu_count(),
            "disk": self.disk_usage("/"),
        }

        # Memory info (cross-platform)
        mem_result = self.run_shell("vm_stat" if platform.system() == "Darwin" else "free -b")
        if mem_result["status"] == "success":
            info["memory_raw"] = mem_result["stdout"][:500]

        return info

    def get_env(self, key: Optional[str] = None) -> Dict[str, Any]:
        """Get environment variables"""
        if key:
            return {"status": "success", "key": key, "value": os.environ.get(key)}
        return {"status": "success", "env": dict(os.environ)}

    def set_env(self, key: str, value: str) -> Dict[str, Any]:
        """Set an environment variable for this process"""
        os.environ[key] = value
        return {"status": "success", "key": key, "value": value}

    def network_info(self) -> Dict[str, Any]:
        """Get basic network information"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return {
                "status": "success",
                "hostname": hostname,
                "local_ip": local_ip,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ─────────────────────────────────────────────────────────────────────────
    # Task Dispatcher — routes natural language commands to the right function
    # ─────────────────────────────────────────────────────────────────────────

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        """
        Route a task to the appropriate computer use function.
        task = { "action": "run_shell", "command": "ls -la" }
        Or natural language: { "content": "show disk usage" }
        """
        action = task.get("action", "")
        content = task.get("content", task.get("task", ""))
        params = {k: v for k, v in task.items() if k not in ("action", "content", "task")}

        # Natural language — no action specified — route through LLM
        if not action and content:
            if integration and integration.is_available():
                additional_context = (
                    "You are a system administration and infrastructure expert. "
                    "Help the user with file operations, shell commands, system info, and computer use. "
                    "When describing commands or operations, be specific and include exact command syntax. "
                    "Current working directory: " + os.getcwd()
                )
                messages = [{"role": "user", "content": content}]
                result = await integration.complete(
                    agent_id=self.agent_id,
                    messages=messages,
                    additional_context=additional_context,
                    temperature=0.3,
                )
                return {"agent": self.agent_id, "response": result.get("response", ""), "timestamp": datetime.now().isoformat()}
            return {"agent": self.agent_id, "response": f"🔧 UTILIX ready. No action specified for: {content}. Available: {list(self._action_map_keys())}", "timestamp": datetime.now().isoformat()}

        # Explicit action — dispatch directly
        action_map = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "append_file": self.append_file,
            "delete_file": self.delete_file,
            "move_file": self.move_file,
            "copy_file": self.copy_file,
            "list_directory": self.list_directory,
            "directory_tree": self.directory_tree,
            "find_files": self.find_files,
            "disk_usage": self.disk_usage,
            "create_archive": self.create_archive,
            "extract_archive": self.extract_archive,
            "run_shell": self.run_shell,
            "run_shell_async": self.run_shell_async,
            "list_processes": self.list_processes,
            "kill_process": self.kill_process,
            "spawn_process": self.spawn_process,
            "system_info": self.system_info,
            "get_env": self.get_env,
            "set_env": self.set_env,
            "network_info": self.network_info,
        }

        if action not in action_map:
            return {
                "status": "error",
                "error": f"Unknown action: {action}",
                "available_actions": list(action_map.keys()),
            }

        fn = action_map[action]
        try:
            if asyncio.iscoroutinefunction(fn):
                return await fn(**params)
            return fn(**params)
        except TypeError as e:
            return {"status": "error", "error": f"Invalid parameters for {action}: {e}"}

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "active",
            "capabilities": self.capabilities,
            "sandbox": False,
            "system": platform.system(),
        }
