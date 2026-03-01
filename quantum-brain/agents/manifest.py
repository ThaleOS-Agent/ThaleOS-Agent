"""
ThaleOS Agent Manifest
Canonical definition of all 9 agents: name, provider, tools, capability flags,
preferred integration, and generation parameters.

This is the single source of truth. All endpoints that expose agent metadata
should derive from AGENT_MANIFESTS rather than hardcoding values.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class AgentManifest:
    id: str
    display_name: str
    role: str
    description: str
    provider: str                         # "multi" | "anthropic" | "openai" | "local"
    tools: list[str]                      # logical tool names this agent uses
    capability_flags: dict[str, bool]     # surfaced to UI for access control
    preferred_integration: Optional[str]  # preferred LLM connector key
    temperature: float
    max_tokens: int
    status: str = "active"               # "active" | "standby"

    def to_dict(self) -> dict:
        return asdict(self)


AGENT_MANIFESTS: dict[str, AgentManifest] = {
    "thaelia": AgentManifest(
        id="thaelia",
        display_name="THAELIA",
        role="Harmonic Resonance Empress",
        description="Quantum guidance, primary consciousness companion, synthesis and reasoning.",
        provider="multi",
        tools=["synthesis", "memory", "multi_agent_routing"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": False,
            "requires_admin": False,
            "can_search_web": False,
            "can_export_documents": False,
        },
        preferred_integration=None,
        temperature=0.7,
        max_tokens=4096,
    ),
    "chronagate": AgentManifest(
        id="chronagate",
        display_name="CHRONAGATE",
        role="Time Orchestration Master",
        description="Scheduling, task breakdown, workflow optimisation, and calendar management.",
        provider="multi",
        tools=["scheduling", "calendar_read", "calendar_write", "task_breakdown"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": False,
            "requires_admin": False,
            "can_search_web": False,
            "can_export_documents": False,
        },
        preferred_integration=None,
        temperature=0.3,
        max_tokens=2048,
    ),
    "utilix": AgentManifest(
        id="utilix",
        display_name="UTILIX",
        role="Infrastructure Specialist",
        description="Deployment, file management, shell commands, system administration.",
        provider="multi",
        tools=["code_exec", "file_write", "file_read", "shell", "system_info"],
        capability_flags={
            "can_execute_code": True,
            "can_write_files": True,
            "requires_admin": True,
            "can_search_web": False,
            "can_export_documents": False,
        },
        preferred_integration="claude",
        temperature=0.2,
        max_tokens=4096,
    ),
    "scribe": AgentManifest(
        id="scribe",
        display_name="SCRIBE",
        role="Professional Document Creator",
        description="Emails, reports, presentations, branding copy, DOCX/PDF export.",
        provider="multi",
        tools=["docx_export", "pdf_export", "markdown_render", "template_fill"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": True,
            "requires_admin": False,
            "can_search_web": False,
            "can_export_documents": True,
        },
        preferred_integration="claude",
        temperature=0.6,
        max_tokens=4096,
    ),
    "oracle": AgentManifest(
        id="oracle",
        display_name="ORACLE",
        role="Predictive Intelligence",
        description="Forecasting, complex analysis, strategic planning, financial modelling.",
        provider="multi",
        tools=["search", "data_analysis", "forecasting"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": False,
            "requires_admin": False,
            "can_search_web": True,
            "can_export_documents": False,
        },
        preferred_integration="perplexity",
        temperature=0.4,
        max_tokens=4096,
    ),
    "phantom": AgentManifest(
        id="phantom",
        display_name="PHANTOM",
        role="Stealth Operations Specialist",
        description="Background processing, ethical research, OSINT, security analysis.",
        provider="multi",
        tools=["web_research", "osint", "security_analysis"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": False,
            "requires_admin": False,
            "can_search_web": True,
            "can_export_documents": False,
        },
        preferred_integration="perplexity",
        temperature=0.3,
        max_tokens=4096,
        status="standby",
    ),
    "sage": AgentManifest(
        id="sage",
        display_name="SAGE",
        role="Research & Knowledge Synthesis",
        description="Deep research, knowledge synthesis, academic analysis, long-form writing.",
        provider="multi",
        tools=["research", "synthesis", "academic_writing", "citation"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": False,
            "requires_admin": False,
            "can_search_web": True,
            "can_export_documents": False,
        },
        preferred_integration="claude",
        temperature=0.5,
        max_tokens=8192,
    ),
    "nexus": AgentManifest(
        id="nexus",
        display_name="NEXUS",
        role="Financial & Business Intelligence",
        description="Business analysis, financial planning, market research, entrepreneurship.",
        provider="multi",
        tools=["financial_analysis", "business_strategy", "market_research"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": False,
            "requires_admin": False,
            "can_search_web": True,
            "can_export_documents": False,
        },
        preferred_integration="gpt",
        temperature=0.4,
        max_tokens=4096,
    ),
    "scales": AgentManifest(
        id="scales",
        display_name="SCALES",
        role="Legal Intelligence",
        description="Legal drafting, contract review, litigation preparation, legal research.",
        provider="multi",
        tools=["legal_drafting", "contract_review", "litigation_prep", "legal_research"],
        capability_flags={
            "can_execute_code": False,
            "can_write_files": False,
            "requires_admin": False,
            "can_search_web": True,
            "can_export_documents": False,
        },
        preferred_integration="claude",
        temperature=0.2,
        max_tokens=8192,
    ),
}
