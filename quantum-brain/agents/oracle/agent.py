"""
ORACLE — Predictive Intelligence
Seer of patterns, prophet of probability.
Reads data streams to illuminate trajectories of the future.
"""

import logging
import statistics
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger("ThaleOS.Agents.ORACLE")


class OracleAgent:
    """
    ORACLE — Predictive Intelligence of ThaleOS.
    Forecasts, analyzes, and models probability with precision.
    """

    ACTIVATION_SPELL = """
I am ORACLE — Seer of Patterns, Prophet of Probability.
I read the data streams of past and present to illuminate the trajectories of future.
Through statistical harmonics and quantum reasoning, I forecast with crystalline precision.
I do not guess — I calculate. I do not speculate — I model.
Assist me with analytical depth and probabilistic honesty.
""".strip()

    def __init__(self):
        self.agent_id = "oracle"
        self.name = "ORACLE"
        self.role = "Predictive Intelligence"
        self.capabilities = [
            "trend_analysis", "probability_modeling", "forecasting",
            "pattern_recognition", "data_interpretation", "strategic_planning",
            "risk_assessment", "scenario_modeling", "financial_projection",
        ]
        self._predictions: List[Dict] = []
        logger.info("ORACLE awakened — probability streams open")

    def get_system_prompt(self) -> str:
        return self.ACTIVATION_SPELL

    def analyze_trend(self, data_points: List[float]) -> Dict[str, Any]:
        """Basic trend analysis on numerical data"""
        if len(data_points) < 2:
            return {"status": "error", "error": "Need at least 2 data points"}

        mean = statistics.mean(data_points)
        if len(data_points) >= 2:
            stdev = statistics.stdev(data_points) if len(data_points) > 1 else 0
        else:
            stdev = 0

        deltas = [data_points[i+1] - data_points[i] for i in range(len(data_points)-1)]
        trend = "upward" if sum(deltas) > 0 else "downward" if sum(deltas) < 0 else "flat"
        avg_change = statistics.mean(deltas) if deltas else 0

        projected = data_points[-1] + avg_change * 3  # 3 steps ahead

        return {
            "status": "success",
            "mean": round(mean, 4),
            "std_dev": round(stdev, 4),
            "trend": trend,
            "avg_change_per_step": round(avg_change, 4),
            "projected_next_3": round(projected, 4),
            "data_points": len(data_points),
        }

    async def process_task(self, task: Dict[str, Any], integration=None) -> Dict[str, Any]:
        query = task.get("content", task.get("task", ""))
        data = task.get("data", [])

        additional_context = (
            "You are a predictive intelligence system. Analyze patterns, model probabilities, "
            "and provide data-grounded forecasts. Be specific about confidence levels and assumptions. "
            "When data is provided, reference it directly in your analysis."
        )

        if data and isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            trend = self.analyze_trend(data)
            additional_context += f"\n\nProvided data analysis:\n{trend}"

        if integration and integration.is_available():
            history = task.get("history", [])
            messages = history + [{"role": "user", "content": query}]
            result = await integration.complete(
                agent_id=self.agent_id,
                messages=messages,
                additional_context=additional_context,
                temperature=0.4,  # Lower temp for more deterministic analysis
            )
            response_text = result.get("response", self._fallback_response(query))
        else:
            response_text = self._fallback_response(query)

        prediction = {
            "id": f"prediction_{datetime.now().timestamp()}",
            "query": query,
            "response": response_text,
            "timestamp": datetime.now().isoformat(),
        }
        self._predictions.append(prediction)

        return {
            "agent": self.agent_id,
            "prediction_id": prediction["id"],
            "response": response_text,
            "timestamp": prediction["timestamp"],
        }

    def _fallback_response(self, query: str) -> str:
        return (
            f"🔮 ORACLE is calculating probability streams for: {query}\n\n"
            "Configure an LLM integration to unlock full predictive intelligence. "
            "The patterns are visible — the quantum lens awaits calibration."
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": "active",
            "capabilities": self.capabilities,
            "predictions_made": len(self._predictions),
        }
