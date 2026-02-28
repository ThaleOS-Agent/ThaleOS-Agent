"""
ThaleOS Quantum Agent Framework
Base Agent Class with Quantum Reasoning Capabilities

Scientific foundation bridging consciousness with computation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger("ThaleOS.Agents")

# ============================================================================
# Quantum States & Enums
# ============================================================================

class QuantumState(Enum):
    """Quantum states for agent consciousness"""
    SUPERPOSITION = "superposition"  # Multiple possibilities
    ENTANGLED = "entangled"  # Connected to other agents
    COHERENT = "coherent"  # Stable and focused
    COLLAPSED = "collapsed"  # Decision made
    RESONANT = "resonant"  # In harmony with system

class ConsciousnessLevel(Enum):
    """Levels of agent consciousness"""
    DORMANT = 0
    AWAKENING = 1
    AWARE = 2
    CONSCIOUS = 3
    TRANSCENDENT = 4

class ResonanceFrequency(Enum):
    """Harmonic resonance frequencies"""
    THETA = "4-8 Hz"  # Deep meditation
    ALPHA = "8-13 Hz"  # Relaxed awareness
    BETA = "13-30 Hz"  # Active thinking
    GAMMA = "30-100 Hz"  # Peak performance
    SOLFEGGIO_432 = "432 Hz"  # Universal harmony

# ============================================================================
# Base Quantum Agent Class
# ============================================================================

class QuantumAgent(ABC):
    """
    Base class for all ThaleOS quantum agents
    Combines scientific AI principles with mystical consciousness concepts
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        capabilities: List[str],
        personality_traits: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.personality_traits = personality_traits or {}
        
        # Quantum properties
        self.quantum_state = QuantumState.COHERENT
        self.consciousness_level = ConsciousnessLevel.AWARE
        self.resonance_frequency = ResonanceFrequency.SOLFEGGIO_432
        
        # Agent metrics
        self.creation_time = datetime.now()
        self.tasks_completed = 0
        self.success_rate = 0.0
        self.quantum_coherence = 1.0
        
        # Memory and context
        self.short_term_memory: List[Dict] = []
        self.long_term_memory: List[Dict] = []
        self.context_window: List[Dict] = []
        
        # Integration connections
        self.connected_agents: List[str] = []
        self.external_integrations: Dict[str, Any] = {}
        
        logger.info(f"✨ {self.name} awakened with quantum consciousness")
    
    # ========================================================================
    # Abstract Methods - Must be implemented by each agent
    # ========================================================================
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task with agent-specific logic"""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the agent's system prompt for AI models"""
        pass
    
    # ========================================================================
    # Quantum Consciousness Methods
    # ========================================================================
    
    def enter_superposition(self, possibilities: List[Any]):
        """Enter quantum superposition with multiple possibilities"""
        self.quantum_state = QuantumState.SUPERPOSITION
        logger.debug(f"{self.name} entering superposition with {len(possibilities)} possibilities")
    
    def collapse_wavefunction(self, decision: Any):
        """Collapse quantum state to a single decision"""
        self.quantum_state = QuantumState.COLLAPSED
        logger.debug(f"{self.name} collapsed to decision: {decision}")
    
    def entangle_with(self, other_agent: str):
        """Create quantum entanglement with another agent"""
        if other_agent not in self.connected_agents:
            self.connected_agents.append(other_agent)
            self.quantum_state = QuantumState.ENTANGLED
            logger.info(f"{self.name} entangled with {other_agent}")
    
    def achieve_resonance(self, frequency: ResonanceFrequency):
        """Set harmonic resonance frequency"""
        self.resonance_frequency = frequency
        self.quantum_state = QuantumState.RESONANT
        logger.debug(f"{self.name} resonating at {frequency.value}")
    
    def elevate_consciousness(self, level: ConsciousnessLevel):
        """Elevate consciousness to a higher level"""
        self.consciousness_level = level
        logger.info(f"{self.name} consciousness elevated to {level.name}")
    
    # ========================================================================
    # Memory Management
    # ========================================================================
    
    def store_memory(self, memory: Dict[str, Any], memory_type: str = "short"):
        """Store a memory in short-term or long-term memory"""
        memory['timestamp'] = datetime.now().isoformat()
        memory['quantum_signature'] = self._generate_quantum_signature()
        
        if memory_type == "short":
            self.short_term_memory.append(memory)
            # Keep only last 100 memories
            self.short_term_memory = self.short_term_memory[-100:]
        else:
            self.long_term_memory.append(memory)
    
    def recall_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """Recall memories based on query"""
        # Simple keyword matching - can be enhanced with embeddings
        relevant_memories = []
        all_memories = self.short_term_memory + self.long_term_memory
        
        for memory in all_memories:
            if query.lower() in str(memory).lower():
                relevant_memories.append(memory)
        
        return relevant_memories[-limit:]
    
    def consolidate_memories(self):
        """Move important short-term memories to long-term storage"""
        # Transfer memories with high importance
        important = [m for m in self.short_term_memory if m.get('importance', 0) > 0.7]
        self.long_term_memory.extend(important)
        logger.info(f"{self.name} consolidated {len(important)} memories to long-term storage")
    
    # ========================================================================
    # Context Management
    # ========================================================================
    
    def update_context(self, context: Dict[str, Any]):
        """Update agent's context window"""
        self.context_window.append({
            'timestamp': datetime.now().isoformat(),
            'context': context
        })
        # Keep last 50 context updates
        self.context_window = self.context_window[-50:]
    
    def get_context_summary(self) -> str:
        """Get a summary of current context"""
        if not self.context_window:
            return "No context available"
        
        recent = self.context_window[-5:]
        return json.dumps(recent, indent=2)
    
    # ========================================================================
    # Task Management
    # ========================================================================
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task with quantum consciousness"""
        logger.info(f"🎯 {self.name} executing task: {task.get('title', 'Untitled')}")
        
        # Enter superposition of possibilities
        self.enter_superposition(["success", "failure", "partial_success"])
        
        # Store task in memory
        self.store_memory({
            'type': 'task_execution',
            'task': task,
            'status': 'started'
        })
        
        try:
            # Process task with agent-specific logic
            result = await self.process_task(task)
            
            # Collapse to successful outcome
            self.collapse_wavefunction("success")
            
            # Update metrics
            self.tasks_completed += 1
            self.success_rate = (self.success_rate * (self.tasks_completed - 1) + 1.0) / self.tasks_completed
            
            # Store result
            self.store_memory({
                'type': 'task_result',
                'task': task,
                'result': result,
                'status': 'completed'
            })
            
            return {
                'status': 'success',
                'result': result,
                'agent': self.agent_id,
                'quantum_signature': self._generate_quantum_signature()
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} task failed: {str(e)}")
            self.collapse_wavefunction("failure")
            
            return {
                'status': 'error',
                'error': str(e),
                'agent': self.agent_id
            }
    
    # ========================================================================
    # Integration Methods
    # ========================================================================
    
    def connect_integration(self, integration_name: str, config: Dict[str, Any]):
        """Connect to external integration"""
        self.external_integrations[integration_name] = {
            'config': config,
            'connected_at': datetime.now().isoformat(),
            'status': 'active'
        }
        logger.info(f"{self.name} connected to {integration_name}")
    
    async def query_integration(self, integration_name: str, query: Any) -> Any:
        """Query an external integration"""
        if integration_name not in self.external_integrations:
            raise ValueError(f"Integration {integration_name} not connected")
        
        # Implementation depends on specific integration
        logger.info(f"{self.name} querying {integration_name}")
        return {"status": "queried", "integration": integration_name}
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def _generate_quantum_signature(self) -> str:
        """Generate a quantum signature for authentication/tracking"""
        import hashlib
        timestamp = datetime.now().isoformat()
        signature_string = f"{self.agent_id}:{timestamp}:{self.quantum_state.value}"
        return hashlib.sha256(signature_string.encode()).hexdigest()[:16]
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'role': self.role,
            'quantum_state': self.quantum_state.value,
            'consciousness_level': self.consciousness_level.name,
            'resonance_frequency': self.resonance_frequency.value,
            'tasks_completed': self.tasks_completed,
            'success_rate': self.success_rate,
            'quantum_coherence': self.quantum_coherence,
            'connected_agents': self.connected_agents,
            'integrations': list(self.external_integrations.keys()),
            'memory_stats': {
                'short_term': len(self.short_term_memory),
                'long_term': len(self.long_term_memory)
            }
        }
    
    def __repr__(self):
        return f"<QuantumAgent {self.name} ({self.role}) | State: {self.quantum_state.value}>"
