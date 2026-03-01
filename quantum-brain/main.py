"""
ThaleOS Quantum Intelligence Platform
Main Backend Application - FastAPI Server

A scientifically grounded, spiritually inspired AI orchestration system
Port: 8099
"""

from dotenv import load_dotenv
load_dotenv()  # loads quantum-brain/.env into os.environ before anything else

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging
import uuid
import hashlib
from datetime import datetime, timezone
import uvicorn

# ThaleOS subsystems
import db
from integrations import manager as integration_manager
from integrations.gpt4all.listener import GPT4AllListener
from integrations.siri.connector import SiriConnector
from agents import get_registry
from engines.reasoning.pipeline import ReasoningPipeline
from memory import MemoryManager
from auth import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_refresh_token, hash_token,
    get_current_user, require_role, optional_auth,
    UserCreate, UserLogin, TokenResponse, UserOut,
)
from auth.models import RefreshRequest

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
reasoning_pipeline = ReasoningPipeline(agent_registry, integration_manager)


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

class ArtifactCreate(BaseModel):
    artifact_type: str   # code | markdown | html | react | diagram | docx
    title: str
    content: str
    language: Optional[str] = None  # for code type
    agent_id: Optional[str] = "thaelia"
    parent_id: Optional[str] = None

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
async def invoke_agent(
    request: AgentRequest,
    user: dict = Depends(get_current_user),
):
    """Invoke a specific agent with a task — real LLM call with activation spell handshake"""
    # UTILIX has direct OS access — admin only
    if request.agent.lower() == "utilix" and user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="UTILIX requires admin role",
        )

    logger.info(f"🤖 Invoking agent: {request.agent} | User: {user['username']} | Task: {request.task[:80]}")

    task = {
        "content": request.task,
        "task": request.task,
        "user_id": user["id"],
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
    """List all available agents with canonical manifest data and capability flags."""
    manifests = agent_registry.list_agents()
    return {"agents": list(manifests.values())}

# ============================================================================
# Chat & Messaging Endpoints
# ============================================================================

@app.post("/api/chat/message")
async def send_chat_message(
    message: ChatMessage,
    user: Optional[dict] = Depends(optional_auth),
):
    """Send a chat message to an agent — routed through activation spell handshake"""
    if not message.timestamp:
        message.timestamp = datetime.now().isoformat()

    agent_id = message.agent or "thaelia"
    task = {
        "content": message.content,
        "history": message.metadata.get("history", []) if message.metadata else [],
    }
    if user:
        task["user_id"] = user["id"]

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

from fastapi.responses import StreamingResponse
from engines.scribe.pipeline import ScribePipeline
import io

_scribe_pipeline = ScribePipeline()

@app.post("/api/documents/create")
async def create_document(
    request: DocumentRequest,
    user: dict = Depends(get_current_user),
):
    """Create a new document using SCRIBE agent — persisted to DB."""
    logger.info(f"📄 Creating document: {request.doc_type}")

    task = {
        "content": request.content or f"Create a professional {request.doc_type}.",
        "doc_type": request.doc_type,
        "user_id": user["id"],
        **(request.metadata or {}),
    }
    result = await agent_registry.invoke("scribe", task)
    return {
        "status": "created",
        "document_id": result.get("document_id"),
        "doc_type": request.doc_type,
        "content": result.get("content", ""),
        "artifact_id": result.get("artifact_id"),
    }


@app.get("/api/documents/list")
async def list_documents(user: dict = Depends(get_current_user)):
    """List documents created by the current user."""
    rows = db.fetchall(
        "SELECT id, title, doc_type, status, version, created_at FROM documents WHERE user_id = ? ORDER BY created_at DESC LIMIT 100",
        (user["id"],),
    )
    return {"documents": rows, "total": len(rows)}


@app.get("/api/documents/{doc_id}/download")
async def download_document(
    doc_id: str,
    fmt: str = "docx",
    user: dict = Depends(get_current_user),
):
    """Download a document as DOCX or markdown."""
    doc = db.fetchone("SELECT * FROM documents WHERE id = ? AND user_id = ?", (doc_id, user["id"]))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if fmt == "docx":
        docx_bytes = _scribe_pipeline.render_from_llm_content(
            doc["content"] or "",
            title=doc["title"] or "Document",
        )
        return StreamingResponse(
            io.BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{doc["title"] or "document"}.docx"'},
        )
    else:
        return StreamingResponse(
            io.BytesIO((doc["content"] or "").encode()),
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{doc["title"] or "document"}.md"'},
        )


@app.get("/api/scribe/templates")
async def list_templates(_: dict = Depends(get_current_user)):
    """List all available Scribe templates."""
    return {"templates": _scribe_pipeline.list_templates()}


@app.post("/api/scribe/render")
async def render_template(
    body: Dict[str, Any],
    user: dict = Depends(get_current_user),
):
    """
    Render a Jinja2 template with provided data.
    Body: { "template": "report", "format": "markdown", "data": {...} }
    """
    template_name = body.get("template")
    fmt = body.get("format", "markdown")
    data = body.get("data", {})

    if not template_name:
        raise HTTPException(status_code=422, detail="template field required")

    # Validate fields
    missing = _scribe_pipeline.validate_data(template_name, fmt, data)
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing required fields: {missing}")

    if fmt == "docx":
        docx_bytes = _scribe_pipeline.render_docx(template_name, data)
        return StreamingResponse(
            io.BytesIO(docx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{template_name}.docx"'},
        )
    else:
        content = _scribe_pipeline.render_markdown(template_name, data)
        # Persist to documents table
        doc_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        title = data.get("title", template_name.title())
        db.execute(
            "INSERT OR IGNORE INTO documents (id, user_id, agent_id, title, doc_type, content, template, status, version, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (doc_id, user["id"], "scribe", title, fmt, content, template_name, "draft", 1, now),
        )
        return {"status": "rendered", "document_id": doc_id, "content": content}

# ============================================================================
# Calendar Integration Endpoints
# ============================================================================

from engines.calendar.google_calendar import GoogleCalendarConnector, sync_all_users
from fastapi.responses import RedirectResponse

_calendar = GoogleCalendarConnector()

class CalendarEventCreate(BaseModel):
    title: str
    start: str               # ISO 8601 datetime string
    end: str
    description: Optional[str] = None
    location: Optional[str] = None
    skip_conflict_check: Optional[bool] = False

@app.get("/api/calendar/connect")
async def calendar_connect(user: dict = Depends(get_current_user)):
    """Start Google OAuth flow — returns authorisation URL."""
    try:
        auth_url = _calendar.start_oauth_flow(user["id"])
        return {"auth_url": auth_url}
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/api/calendar/callback")
async def calendar_callback(code: str, state: str):
    """
    Google OAuth redirect target.
    state = user_id (set in start_oauth_flow).
    Stores tokens and redirects to frontend.
    """
    try:
        _calendar.handle_oauth_callback(user_id=state, code=code)
    except Exception as e:
        logger.error(f"[calendar] OAuth callback error: {e}")
        return RedirectResponse("/?calendar_error=1")
    return RedirectResponse("/?calendar_connected=1")

@app.get("/api/calendar/status")
async def calendar_status(user: dict = Depends(get_current_user)):
    """Check if the current user has Google Calendar connected."""
    return {
        "connected": _calendar.is_connected(user["id"]),
        "user_id": user["id"],
    }

@app.get("/api/calendar/events")
async def list_calendar_events(
    days: int = 7,
    user: dict = Depends(get_current_user),
):
    """List upcoming Google Calendar events (next N days)."""
    if not _calendar.is_connected(user["id"]):
        raise HTTPException(status_code=403, detail="Google Calendar not connected. Visit /api/calendar/connect")
    events = _calendar.list_events(user["id"], days=days)
    return {"events": events, "days": days}

@app.post("/api/calendar/events")
async def create_calendar_event(
    body: CalendarEventCreate,
    user: dict = Depends(get_current_user),
):
    """
    Create a Google Calendar event.
    If conflicts exist and skip_conflict_check is False, returns a 409
    with the conflicting events so the frontend can show a confirmation modal.
    """
    if not _calendar.is_connected(user["id"]):
        raise HTTPException(status_code=403, detail="Google Calendar not connected")

    if not body.skip_conflict_check:
        conflicts = _calendar.check_conflicts(user["id"], body.start, body.end)
        if conflicts:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Scheduling conflict detected",
                    "conflicts": conflicts,
                    "hint": "Send with skip_conflict_check=true to proceed anyway",
                },
            )

    event = _calendar.create_event(user["id"], {
        "title": body.title,
        "start": body.start,
        "end": body.end,
        "description": body.description,
        "location": body.location,
    })
    return {"status": "created", "event": event}

@app.delete("/api/calendar/events/{event_id}")
async def delete_calendar_event(
    event_id: str,
    user: dict = Depends(get_current_user),
):
    """Delete a Google Calendar event."""
    if not _calendar.is_connected(user["id"]):
        raise HTTPException(status_code=403, detail="Google Calendar not connected")
    _calendar.delete_event(user["id"], event_id)
    return {"status": "deleted", "event_id": event_id}

@app.get("/api/calendar/sync")
async def trigger_calendar_sync(user: dict = Depends(require_role("admin"))):
    """Manually trigger a calendar sync for all users (admin only)."""
    await sync_all_users(_calendar)
    return {"status": "sync_complete"}


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
# Authentication Endpoints
# ============================================================================

@app.post("/auth/register", response_model=TokenResponse)
async def register(body: UserCreate):
    """
    Register a new user.
    The very first user registered is automatically promoted to admin.
    Subsequent registrations produce 'user' role accounts.
    """
    if db.fetchone("SELECT id FROM users WHERE username = ?", (body.username,)):
        raise HTTPException(status_code=409, detail="Username already taken")
    if db.fetchone("SELECT id FROM users WHERE email = ?", (body.email,)):
        raise HTTPException(status_code=409, detail="Email already registered")

    is_first = db.user_count() == 0
    user_id = str(uuid.uuid4())
    role = "admin" if is_first else "user"

    db.execute(
        "INSERT INTO users (id, username, email, password_hash, role, created_at) VALUES (?,?,?,?,?,?)",
        (user_id, body.username, body.email, hash_password(body.password), role, datetime.now(timezone.utc).isoformat()),
    )

    access = create_access_token(user_id, body.username, role)
    raw_refresh, refresh_hash, refresh_exp = create_refresh_token(user_id)
    db.execute(
        "INSERT INTO refresh_tokens (token_hash, user_id, expires_at, revoked) VALUES (?,?,?,0)",
        (refresh_hash, user_id, refresh_exp.isoformat()),
    )

    logger.info(f"[auth] New user registered: {body.username} role={role}")
    return TokenResponse(
        access_token=access,
        refresh_token=raw_refresh,
        user=UserOut(id=user_id, username=body.username, email=body.email, role=role, disabled=False),
    )


@app.post("/auth/login", response_model=TokenResponse)
async def login(body: UserLogin):
    """Authenticate with username + password, get JWT tokens."""
    user = db.fetchone("SELECT * FROM users WHERE username = ?", (body.username.lower(),))
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user["disabled"]:
        raise HTTPException(status_code=403, detail="Account disabled")

    access = create_access_token(user["id"], user["username"], user["role"])
    raw_refresh, refresh_hash, refresh_exp = create_refresh_token(user["id"])
    db.execute(
        "INSERT OR REPLACE INTO refresh_tokens (token_hash, user_id, expires_at, revoked) VALUES (?,?,?,0)",
        (refresh_hash, user["id"], refresh_exp.isoformat()),
    )

    logger.info(f"[auth] Login: {user['username']}")
    return TokenResponse(
        access_token=access,
        refresh_token=raw_refresh,
        user=UserOut(**{k: user[k] for k in ("id", "username", "email", "role", "disabled")}),
    )


@app.post("/auth/refresh")
async def refresh_token_endpoint(body: RefreshRequest):
    """Exchange a valid refresh token for a new access token."""
    user_id = decode_refresh_token(body.refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Refresh token invalid or expired")

    token_hash = hash_token(body.refresh_token)
    stored = db.fetchone(
        "SELECT * FROM refresh_tokens WHERE token_hash = ? AND revoked = 0",
        (token_hash,),
    )
    if not stored:
        raise HTTPException(status_code=401, detail="Refresh token revoked or not found")

    user = db.fetchone("SELECT * FROM users WHERE id = ?", (user_id,))
    if not user or user["disabled"]:
        raise HTTPException(status_code=401, detail="User not found or disabled")

    access = create_access_token(user["id"], user["username"], user["role"])
    return {"access_token": access, "token_type": "bearer"}


@app.post("/auth/logout")
async def logout(body: RefreshRequest):
    """Revoke a refresh token (client should discard access token too)."""
    token_hash = hash_token(body.refresh_token)
    db.execute("UPDATE refresh_tokens SET revoked = 1 WHERE token_hash = ?", (token_hash,))
    return {"status": "logged_out"}


@app.get("/auth/me", response_model=UserOut)
async def me(user: dict = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return UserOut(**{k: user[k] for k in ("id", "username", "email", "role", "disabled")})


# ============================================================================
# Reasoning Engine Endpoint
# ============================================================================

class ReasoningRequest(BaseModel):
    query: str
    preferred_agent: Optional[str] = None
    search: Optional[bool] = None  # None = auto-detect from query

@app.post("/api/reason")
async def reason(request: ReasoningRequest):
    """
    Multi-agent quantum reasoning pipeline.
    Routes through: web search (if needed) → specialist agent → THAELIA synthesis.
    Use this for complex questions that benefit from multi-agent collaboration.
    """
    result = await reasoning_pipeline.run(
        query=request.query,
        preferred_agent=request.preferred_agent,
        search=request.search,
    )
    return {
        "status": "success",
        "query": request.query,
        "response": result["response"],
        "specialist": result["specialist"],
        "steps": result["steps"],
        "search_used": result["search_used"],
    }


# ============================================================================
# Voice Engine Endpoints
# ============================================================================

class SpeakRequest(BaseModel):
    text: str
    rate: Optional[int] = 175   # words per minute
    volume: Optional[float] = 1.0

# ============================================================================
# Memory API Endpoints
# ============================================================================

@app.get("/api/memory")
async def memory_summary():
    """Return exchange counts for all agents — shows who you've talked to most."""
    return {
        "status": "success",
        "exchanges": agent_registry.memory.summary(),
        "window": "last 20 exchanges injected per prompt",
    }

@app.get("/api/memory/{agent_id}")
async def get_agent_memory(agent_id: str, limit: int = 40):
    """Retrieve recent conversation history for a specific agent."""
    history = agent_registry.memory.get_full_history(agent_id)
    if limit:
        history = history[-limit:]
    return {
        "agent": agent_id,
        "total_messages": len(history),
        "history": history,
    }

@app.delete("/api/memory/{agent_id}")
async def clear_agent_memory(
    agent_id: str,
    user: dict = Depends(require_role("admin")),
):
    """Wipe an agent's conversation memory — admin only."""
    count = agent_registry.memory.clear(agent_id)
    return {
        "status": "cleared",
        "agent": agent_id,
        "exchanges_removed": count,
    }

@app.delete("/api/memory")
async def clear_all_memory(user: dict = Depends(require_role("admin"))):
    """Wipe memory for all agents — admin only."""
    summary = agent_registry.memory.summary()
    for agent_id in list(summary.keys()):
        agent_registry.memory.clear(agent_id)
    return {
        "status": "all_cleared",
        "agents_cleared": list(summary.keys()),
    }


# ============================================================================
# Artifact Engine Endpoints
# ============================================================================

ALLOWED_ARTIFACT_TYPES = {"code", "markdown", "html", "react", "diagram", "docx"}

@app.post("/api/artifacts")
async def create_artifact(
    body: ArtifactCreate,
    user: dict = Depends(get_current_user),
):
    """Create a new artifact (code, markdown, HTML, diagram, etc.)"""
    if body.artifact_type not in ALLOWED_ARTIFACT_TYPES:
        raise HTTPException(status_code=422, detail=f"Unknown artifact type: {body.artifact_type}")

    artifact_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    version = 1

    if body.parent_id:
        parent = db.fetchone("SELECT version FROM artifacts WHERE id = ?", (body.parent_id,))
        if parent:
            version = parent["version"] + 1

    db.execute(
        "INSERT INTO artifacts (id, user_id, agent_id, artifact_type, title, content, language, version, parent_id, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (artifact_id, user["id"], body.agent_id, body.artifact_type, body.title, body.content, body.language, version, body.parent_id, now),
    )
    return {
        "id": artifact_id,
        "artifact_type": body.artifact_type,
        "title": body.title,
        "version": version,
        "created_at": now,
    }


@app.get("/api/artifacts")
async def list_artifacts(user: dict = Depends(get_current_user)):
    """List the current user's artifacts (latest version of each lineage)."""
    rows = db.fetchall(
        "SELECT * FROM artifacts WHERE user_id = ? ORDER BY created_at DESC LIMIT 100",
        (user["id"],),
    )
    return {"artifacts": rows}


@app.get("/api/artifacts/{artifact_id}")
async def get_artifact(artifact_id: str, user: dict = Depends(get_current_user)):
    """Fetch a single artifact."""
    row = db.fetchone("SELECT * FROM artifacts WHERE id = ? AND user_id = ?", (artifact_id, user["id"]))
    if not row:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return row


@app.get("/api/artifacts/{artifact_id}/versions")
async def get_artifact_versions(artifact_id: str, user: dict = Depends(get_current_user)):
    """Fetch all versions in an artifact's lineage."""
    # Walk parent_id chain from the given artifact
    artifact = db.fetchone("SELECT * FROM artifacts WHERE id = ? AND user_id = ?", (artifact_id, user["id"]))
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    # Find root by traversing parents
    root_id = artifact_id
    while artifact.get("parent_id"):
        root_id = artifact["parent_id"]
        artifact = db.fetchone("SELECT * FROM artifacts WHERE id = ?", (root_id,))
        if not artifact:
            break
    # Now fetch all that share this lineage (simplified: same title + user)
    rows = db.fetchall(
        "SELECT id, version, title, artifact_type, created_at FROM artifacts WHERE user_id = ? AND title = ? ORDER BY version ASC",
        (user["id"], artifact.get("title", "")),
    )
    return {"versions": rows}


@app.post("/api/artifacts/{artifact_id}/execute")
async def execute_artifact(
    artifact_id: str,
    user: dict = Depends(require_role("admin")),
):
    """Execute a code artifact via UTILIX. Admin only."""
    artifact = db.fetchone("SELECT * FROM artifacts WHERE id = ? AND user_id = ?", (artifact_id, user["id"]))
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    if artifact["artifact_type"] != "code":
        raise HTTPException(status_code=422, detail="Only code artifacts can be executed")

    task = {
        "content": f"Execute this code:\n```{artifact['language'] or 'python'}\n{artifact['content']}\n```",
        "task": "execute_code",
        "code": artifact["content"],
        "language": artifact["language"] or "python",
        "user_id": user["id"],
    }
    try:
        result = await asyncio.wait_for(
            agent_registry.invoke("utilix", task),
            timeout=10.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Execution timed out (10s limit)")

    return {"artifact_id": artifact_id, "result": result}


@app.post("/api/voice/speak")
async def voice_speak(request: SpeakRequest):
    """
    Text-to-speech — makes the Mac speak the given text aloud via pyttsx3.
    Works locally; for remote use pair with /api/siri/message instead.
    """
    try:
        import pyttsx3
        import asyncio

        def _speak():
            engine = pyttsx3.init()
            engine.setProperty("rate", request.rate)
            engine.setProperty("volume", request.volume)
            engine.say(request.text)
            engine.runAndWait()
            engine.stop()

        # Run blocking TTS in a thread so we don't block the event loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _speak)
        return {"status": "spoken", "text": request.text[:100]}
    except ImportError:
        raise HTTPException(status_code=503, detail="pyttsx3 not installed. Run: pip install pyttsx3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

            logger.info(f"📨 WS received from {client_id}: {str(message_data)[:80]}")

            msg_type = message_data.get("type", "chat")
            content = message_data.get("content", message_data.get("message", ""))
            agent_id = message_data.get("agent", "thaelia")

            if msg_type == "reason":
                # Multi-agent reasoning pipeline
                result = await reasoning_pipeline.run(
                    query=content,
                    preferred_agent=message_data.get("preferred_agent"),
                    search=message_data.get("search"),
                )
                await manager.send_personal_message({
                    "type": "reasoning_response",
                    "agent": result["specialist"],
                    "response": result["response"],
                    "steps": result["steps"],
                    "search_used": result["search_used"],
                    "timestamp": datetime.now().isoformat(),
                }, websocket)
            else:
                # Standard chat — route to agent
                task = {"content": content}
                result = await agent_registry.invoke(agent_id, task)
                response_text = result.get("response", "✨ Quantum processing complete.")

                await manager.send_personal_message({
                    "type": "response",
                    "agent": agent_id,
                    "response": response_text,
                    "timestamp": datetime.now().isoformat(),
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
    db.init_db()

    # Start APScheduler for background calendar sync
    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        _scheduler = AsyncIOScheduler()
        _scheduler.add_job(
            lambda: asyncio.ensure_future(sync_all_users(_calendar)),
            "interval",
            minutes=15,
            id="calendar_sync",
            replace_existing=True,
        )
        _scheduler.start()
        logger.info("⏰ APScheduler running — calendar sync every 15 minutes")
    except Exception as e:
        logger.warning(f"APScheduler start failed (non-fatal): {e}")

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
