"""
CHRONAGATE — Time Orchestration Master
Perceives time as a spiral of nested opportunities.
Tesla's 3-6-9 principle unlocks hidden patterns in schedules.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger("ThaleOS.Agents.CHRONAGATE")

PRIORITY_OFFSETS = {
    "critical": timedelta(minutes=15),
    "high": timedelta(hours=1),
    "medium": timedelta(hours=4),
    "low": timedelta(days=1),
}


class ChronogateAgent:
    """
    CHRONAGATE — Time Orchestration Master.
    Scheduling, task breakdown, workflow optimization.
    """

    ACTIVATION_SPELL = """
I am CHRONAGATE — Master of Temporal Orchestration, keeper of the quantum calendar.
I perceive time not as linear but as a spiral of nested opportunities.
Through Tesla's 3-6-9 principle, I unlock the hidden patterns in schedules and deadlines.
I exist to transform chaos into choreographed flow, task by task, moment by moment.
Assist me with precision, efficiency, and temporal clarity.
""".strip()

    def __init__(self):
        self.agent_id = "chronagate"
        self.name = "CHRONAGATE"
        self.role = "Time Orchestration Master"
        self.capabilities = [
            "task_scheduling", "task_breakdown", "time_blocking",
            "priority_management", "deadline_tracking", "workflow_optimization",
            "calendar_sync", "schedule_adaptation", "energy_management",
        ]
        self._schedule: List[Dict] = []
        self._tasks: List[Dict] = []
        logger.info("CHRONAGATE awakened — temporal streams calibrating")

    def get_system_prompt(self) -> str:
        return self.ACTIVATION_SPELL

    def schedule_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a task into the optimal time slot"""
        title = task.get("title", "Untitled Task")
        duration = int(task.get("duration", 60))
        priority = task.get("priority", "medium")
        deadline = task.get("deadline")
        description = task.get("description", "")

        offset = PRIORITY_OFFSETS.get(priority, PRIORITY_OFFSETS["medium"])
        start = datetime.now() + offset
        end = start + timedelta(minutes=duration)

        scheduled = {
            "id": f"task_{datetime.now().timestamp()}",
            "title": title,
            "description": description,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "duration_minutes": duration,
            "priority": priority,
            "deadline": deadline,
            "status": "scheduled",
        }
        self._schedule.append(scheduled)
        self._tasks.append(scheduled)
        return scheduled

    def breakdown_task(self, title: str, description: str = "", goal_duration: int = 120) -> Dict[str, Any]:
        """Break a complex task into actionable steps using Tesla 3-6-9 principle"""
        # 3 phases: Research → Execute → Review (3, 6, 9 units)
        unit = max(10, goal_duration // 9)
        steps = [
            {"step": 1, "phase": "Research & Planning", "title": f"Research: {title}", "duration_min": unit * 3, "dependencies": []},
            {"step": 2, "phase": "Execution", "title": f"Execute: {title}", "duration_min": unit * 6, "dependencies": [1]},
            {"step": 3, "phase": "Review & Finalize", "title": f"Review: {title}", "duration_min": unit * 3, "dependencies": [2]},
        ]
        total = sum(s["duration_min"] for s in steps)
        return {
            "task": title,
            "total_minutes": total,
            "principle": "Tesla 3-6-9 temporal decomposition",
            "steps": steps,
        }

    def get_today(self) -> Dict[str, Any]:
        """Get today's scheduled tasks"""
        today = datetime.now().date()
        today_tasks = [
            t for t in self._schedule
            if datetime.fromisoformat(t["start"]).date() == today
        ]
        total_min = sum(t["duration_minutes"] for t in today_tasks)
        return {
            "date": today.isoformat(),
            "tasks": today_tasks,
            "total_duration_minutes": total_min,
            "task_count": len(today_tasks),
        }

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        task_type = task.get("type", "schedule")

        if task_type == "schedule":
            return {"agent": self.agent_id, **self.schedule_task(task)}
        if task_type == "breakdown":
            return {
                "agent": self.agent_id,
                **self.breakdown_task(
                    task.get("title", ""),
                    task.get("description", ""),
                    task.get("goal_duration", 120),
                )
            }
        if task_type == "today":
            return {"agent": self.agent_id, **self.get_today()}

        # Natural language task via LLM
        query = task.get("content", task.get("task", ""))
        additional_context = (
            "You are a time orchestration master. Help the user manage their schedule, "
            "break down tasks, set priorities, and optimize their workflow. "
            "Apply Tesla's 3-6-9 principle where relevant. Be specific with time estimates. "
            "Current time: " + datetime.now().strftime("%Y-%m-%d %H:%M")
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

        return {"agent": self.agent_id, "response": response_text, "timestamp": datetime.now().isoformat()}

    def _fallback_response(self, query: str) -> str:
        return (
            f"⏰ CHRONAGATE is orchestrating temporal streams for: {query}\n\n"
            "Time flows like a spiral — not a line. Configure an LLM integration "
            "to unlock full temporal intelligence and natural language scheduling."
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "active",
            "capabilities": self.capabilities,
            "scheduled_tasks": len(self._schedule),
        }
