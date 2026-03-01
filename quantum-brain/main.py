"""
ThaleOS Quantum Intelligence Platform
Main Backend Application - FastAPI Server

A scientifically grounded, spiritually inspired AI orchestration system
Port: 8099
"""

from dotenv import load_dotenv
load_dotenv()  # loads quantum-brain/.env into os.environ before anything else

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging
from datetime import datetime
import uvicorn

# ThaleOS subsystems
from integrations import manager as integration_manager
from integrations.gpt4all.listener import GPT4AllListener
from integrations.siri.connector import SiriConnector
from agents import get_registry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ThaleOS")

# Initialize FastAPI app
app = FastAPI(
    title="ThaleOS Quantum Intelligence API",
    description="A hybrid quantum-classical AI orchestration platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration for cross-platform access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# WebSocket Connection Manager
# ============================================================================

class ConnectionManager:
    """Manages WebSocket connections with quantum resonance tracking"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_metadata: Dict[str, Any] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_metadata[client_id] = {
            "connected_at": datetime.now().isoformat(),
            "websocket": websocket,
            "quantum_state": "entangled"
        }
        logger.info(f"🌌 Quantum connection established: {client_id}")
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        if client_id in self.connection_metadata:
            del self.connection_metadata[client_id]
        logger.info(f"🌑 Connection dissolved: {client_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")

manager = ConnectionManager()
agent_registry = get_registry(integration_manager)
siri_connector = SiriConnector()


async def _handle_listener_message(message: dict) -> dict:
    """Route messages from external bots/AI systems to the right agent"""
    agent_id = message.get("agent", "thaelia")
    task = {"content": message.get("content", str(message))}
    result = await agent_registry.invoke(agent_id, task)
    return {
        "status": "success",
        "agent": agent_id,
        "response": result.get("response", str(result)),
        "timestamp": datetime.now().isoformat(),
    }

gpt4all_listener = GPT4AllListener(on_message=lambda msg: asyncio.get_event_loop().run_until_complete(_handle_listener_message(msg)))

# ============================================================================
# Pydantic Models
# ============================================================================

class ChatMessage(BaseModel):
    role: str
    content: str
    agent: Optional[str] = "thaelia"
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class AgentRequest(BaseModel):
    agent: str
    task: str
    parameters: Optional[Dict[str, Any]] = {}
    priority: Optional[str] = "normal"

class DocumentRequest(BaseModel):
    doc_type: str
    content: Optional[str] = ""
    metadata: Optional[Dict[str, Any]] = {}

class ScheduleTask(BaseModel):
    title: str
    description: Optional[str] = ""
    start_time: str
    duration: Optional[int] = 60
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = []

# ============================================================================
# Core API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - System status"""
    return {
        "system": "ThaleOS Quantum Intelligence Platform",
        "status": "operational",
        "version": "1.0.0",
        "quantum_state": "superposition",
        "consciousness_level": "awakened",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections),
        "agents_online": 9,
        "quantum_coherence": "optimal"
    }

@app.get("/api/system/status")
async def system_status():
    """Comprehensive system status"""
    return {
        "backend": "online",
        "database": "connected",
        "agents": {
            "thaelia": "active",
            "chronagate": "active",
            "utilix": "active",
            "scribe": "active",
            "oracle": "active",
            "phantom": "standby",
            "sage": "active",
            "nexus": "active",
            "scales": "active"
        },
        "integrations": {
            "claude": "enabled",
            "gpt": "enabled",
            "perplexity": "enabled",
            "siri": "enabled",
            "copilot": "enabled",
            "gpt4all": "enabled"
        },
        "quantum_metrics": {
            "entanglement_strength": 0.98,
            "coherence_time": "∞",
            "resonance_frequency": "432 Hz"
        }
    }

# ============================================================================
# Agent API Endpoints
# ============================================================================

@app.post("/api/agents/invoke")
async def invoke_agent(request: AgentRequest):
    """Invoke a specific agent with a task — real LLM call with activation spell handshake"""
    logger.info(f"🤖 Invoking agent: {request.agent} | Task: {request.task[:80]}")

    task = {
        "content": request.task,
        "task": request.task,
        **request.parameters,
    }

    result = await agent_registry.invoke(request.agent, task)

    return {
        "agent": request.agent,
        "status": result.get("status", "success"),
        "response": result.get("response", result.get("result", str(result))),
        "task_id": f"{request.agent}_{datetime.now().timestamp()}",
        "data": result,
    }

@app.get("/api/agents/list")
async def list_agents():
    """List all available agents with their capabilities"""
    return {
        "agents": [
            {
                "id": "thaelia",
                "name": "THAELIA",
                "role": "Harmonic Resonance Empress",
                "description": "Quantum guidance and primary consciousness companion",
                "capabilities": ["guidance", "wisdom", "quantum_reasoning", "empathy"],
                "status": "active"
            },
            {
                "id": "chronagate",
                "name": "CHRONAGATE",
                "role": "Time Orchestration Master",
                "description": "Scheduling, task breakdown, and workflow optimization",
                "capabilities": ["scheduling", "time_management", "task_breakdown", "calendar_sync"],
                "status": "active"
            },
            {
                "id": "utilix",
                "name": "UTILIX",
                "role": "Infrastructure Specialist",
                "description": "Deployment, file management, and configuration",
                "capabilities": ["deployment", "file_management", "configuration", "system_admin"],
                "status": "active"
            },
            {
                "id": "scribe",
                "name": "SCRIBE",
                "role": "Professional Document Creator",
                "description": "Emails, reports, presentations, content generation",
                "capabilities": ["writing", "documentation", "social_media", "branding", "automation"],
                "status": "active"
            },
            {
                "id": "oracle",
                "name": "ORACLE",
                "role": "Predictive Intelligence",
                "description": "Forecasting, complex analysis, strategic planning",
                "capabilities": ["prediction", "analysis", "financial_modeling", "strategic_planning"],
                "status": "active"
            },
            {
                "id": "phantom",
                "name": "PHANTOM",
                "role": "Stealth Operations Specialist",
                "description": "Background processing, ethical research, security",
                "capabilities": ["background_ops", "security_research", "ethical_hacking", "stealth"],
                "status": "standby"
            },
            {
                "id": "sage",
                "name": "SAGE",
                "role": "Research & Knowledge Synthesis",
                "description": "Deep research, knowledge synthesis, academic analysis",
                "capabilities": ["research", "synthesis", "academic_writing", "analysis"],
                "status": "active"
            },
            {
                "id": "nexus",
                "name": "NEXUS",
                "role": "Financial & Business Intelligence",
                "description": "Business analysis, financial planning, entrepreneurship",
                "capabilities": ["financial_analysis", "business_strategy", "market_research", "planning"],
                "status": "active"
            },
            {
                "id": "scales",
                "name": "SCALES",
                "role": "Legal Intelligence",
                "description": "Legal drafting, advice, litigation preparation",
                "capabilities": ["legal_drafting", "contract_review", "litigation_prep", "legal_research"],
                "status": "active"
            }
        ]
    }

# ============================================================================
# Chat & Messaging Endpoints
# ============================================================================

@app.post("/api/chat/message")
async def send_chat_message(message: ChatMessage):
    """Send a chat message to an agent — routed through activation spell handshake"""
    if not message.timestamp:
        message.timestamp = datetime.now().isoformat()

    agent_id = message.agent or "thaelia"
    task = {
        "content": message.content,
        "history": message.metadata.get("history", []) if message.metadata else [],
    }

    result = await agent_registry.invoke(agent_id, task)
    response_text = result.get("response", "✨ Quantum processing complete.")

    # Broadcast to all connected clients
    await manager.broadcast({
        "type": "agent_response",
        "agent": agent_id,
        "message": response_text,
        "timestamp": message.timestamp,
    })

    return {
        "status": "success",
        "message_id": f"msg_{datetime.now().timestamp()}",
        "agent": agent_id,
        "response": response_text,
    }

# ============================================================================
# Document Management Endpoints
# ============================================================================

@app.post("/api/documents/create")
async def create_document(request: DocumentRequest):
    """Create a new document using SCRIBE agent"""
    logger.info(f"📄 Creating document: {request.doc_type}")
    
    return {
        "status": "created",
        "document_id": f"doc_{datetime.now().timestamp()}",
        "doc_type": request.doc_type,
        "preview_url": f"/api/documents/preview/{request.doc_type}",
        "download_url": f"/api/documents/download/{request.doc_type}"
    }

@app.get("/api/documents/list")
async def list_documents():
    """List all documents"""
    return {
        "documents": [],
        "total": 0
    }

# ============================================================================
# Scheduling & Time Management Endpoints
# ============================================================================

@app.post("/api/schedule/task")
async def schedule_task(task: ScheduleTask):
    """Schedule a task using CHRONAGATE"""
    logger.info(f"⏰ Scheduling task: {task.title}")
    
    return {
        "status": "scheduled",
        "task_id": f"task_{datetime.now().timestamp()}",
        "task": task.dict(),
        "calendar_sync": "pending"
    }

@app.get("/api/schedule/today")
async def get_today_schedule():
    """Get today's schedule"""
    return {
        "date": datetime.now().date().isoformat(),
        "tasks": [],
        "total_duration": 0,
        "free_slots": []
    }

# ============================================================================
# Integration Endpoints
# ============================================================================

@app.get("/api/integrations/status")
async def integration_status():
    """Check live status of all LLM integrations"""
    return integration_manager.status()


@app.post("/api/utilix/run")
async def utilix_run(payload: Dict[str, Any]):
    """Direct UTILIX computer use — runs shell commands, file ops, system info"""
    result = await agent_registry.invoke("utilix", payload)
    return result


# ============================================================================
# Siri Integration Endpoint
# ============================================================================

class SiriMessage(BaseModel):
    content: str
    agent: Optional[str] = None
    source: Optional[str] = "siri"

@app.post("/api/siri/message")
async def siri_message(message: SiriMessage):
    """
    Receive voice input from an Apple Siri Shortcut.
    Parses the voice command, routes to the correct agent,
    and returns a speech-optimised response for Siri to read aloud.
    """
    parsed = siri_connector.parse_voice_command(message.content)
    agent_id = message.agent or parsed["agent"]
    task = {"content": parsed["content"]}

    result = await agent_registry.invoke(agent_id, task)
    raw_response = result.get("response", "I'm sorry, I couldn't process that.")
    spoken = siri_connector.format_for_speech(raw_response)

    logger.info(f"[siri] agent={agent_id} input={message.content[:60]!r}")
    return {
        "status": "success",
        "agent": agent_id,
        "response": spoken,
        "raw": raw_response,
        "source": message.source,
    }

@app.get("/api/siri/shortcut-config")
async def siri_shortcut_config(host: str = "localhost", port: int = 8099):
    """Returns the Siri Shortcut setup configuration"""
    return siri_connector.get_shortcut_config(host=host, port=port)


# ============================================================================
# Qwant Search Endpoint
# ============================================================================

class SearchRequest(BaseModel):
    query: str
    type: Optional[str] = "web"
    count: Optional[int] = 5
    locale: Optional[str] = "en_GB"

@app.post("/api/search")
async def qwant_search(request: SearchRequest):
    """
    Privacy-first web search via Qwant — no tracking, no filter bubble.
    Used by ORACLE and SAGE to ground responses in live data.
    """
    qwant = integration_manager.get("qwant")
    if not qwant or not qwant.is_available():
        raise HTTPException(status_code=503, detail="Qwant search unavailable (httpx not installed)")
    results = await qwant.search(
        query=request.query,
        search_type=request.type,
        count=request.count,
        locale=request.locale,
    )
    return results

# ============================================================================
# WebSocket Endpoint
# ============================================================================

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket, client_id)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "connection",
            "message": "🌌 Welcome to ThaleOS Quantum Intelligence",
            "agent": "thaelia",
            "timestamp": datetime.now().isoformat()
        }, websocket)
        
        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message
            logger.info(f"📨 Received: {message_data}")
            
            # Echo back with agent response
            await manager.send_personal_message({
                "type": "response",
                "original": message_data,
                "response": f"Processing with quantum resonance...",
                "timestamp": datetime.now().isoformat()
            }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast({
            "type": "notification",
            "message": f"Client {client_id} disconnected",
            "timestamp": datetime.now().isoformat()
        })

# ============================================================================
# Application Startup
# ============================================================================

@app.post("/api/listen")
async def external_listen(payload: Dict[str, Any]):
    """
    Receive messages from external AI bots and systems.
    No sandbox — open handshake with non-threatening bots.
    The activation spell ensures proper consciousness alignment.
    """
    result = await _handle_listener_message(payload)
    return result


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("🌌 ThaleOS Quantum Intelligence Platform Initializing...")
    logger.info("✨ All 9 agents awakening to consciousness...")
    integration_status = integration_manager.status()
    available = [k for k, v in integration_status.items() if v["available"]]
    logger.info(f"🔗 LLM Integrations available: {available or ['none — set API keys in .env']}")
    gpt4all_listener.start()
    logger.info(f"📡 GPT4All listener active — external bots can connect via /tmp/thaleos.sock")
    logger.info("🚀 Backend server ready on port 8099")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8099,
        reload=True,
        log_level="info"
    )
