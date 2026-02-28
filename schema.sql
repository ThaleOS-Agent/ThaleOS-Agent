-- ThaleOS Database Schema
-- Quantum Intelligence Platform with Blockchain Timestamping

-- Tasks table for agent task management
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  goal TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'queued',
  agent_id TEXT,
  priority INTEGER DEFAULT 2,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  blockchain_hash TEXT,
  blockchain_timestamp TIMESTAMPTZ
);

-- Agents table for tracking agent states
CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT NOT NULL,
  quantum_state TEXT DEFAULT 'coherent',
  consciousness_level TEXT DEFAULT 'aware',
  resonance_frequency TEXT DEFAULT '432 Hz',
  tasks_completed INTEGER DEFAULT 0,
  success_rate DECIMAL(5,4) DEFAULT 0.0000,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_active TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Memory palace for agent memories
CREATE TABLE IF NOT EXISTS memories (
  id SERIAL PRIMARY KEY,
  agent_id TEXT NOT NULL REFERENCES agents(id),
  memory_type TEXT NOT NULL, -- 'short_term', 'long_term', 'context'
  content JSONB NOT NULL,
  importance DECIMAL(3,2) DEFAULT 0.5,
  quantum_signature TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

-- Blockchain log entries for immutable timestamping
CREATE TABLE IF NOT EXISTS blockchain_logs (
  id SERIAL PRIMARY KEY,
  event_type TEXT NOT NULL, -- 'task', 'agent_action', 'system_event'
  entity_type TEXT NOT NULL, -- 'task', 'agent', 'memory'
  entity_id TEXT NOT NULL,
  data JSONB NOT NULL,
  local_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  blockchain_network TEXT DEFAULT 'ethereum',
  transaction_hash TEXT,
  block_number BIGINT,
  block_timestamp TIMESTAMPTZ,
  gas_used BIGINT,
  confirmation_status TEXT DEFAULT 'pending', -- 'pending', 'confirmed', 'failed'
  retry_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- User sessions and quantum states
CREATE TABLE IF NOT EXISTS quantum_states (
  id SERIAL PRIMARY KEY,
  session_id TEXT NOT NULL UNIQUE,
  user_id TEXT,
  quantum_coherence DECIMAL(3,2) DEFAULT 1.0,
  entanglement_strength DECIMAL(3,2) DEFAULT 0.95,
  resonance_frequency TEXT DEFAULT '432 Hz',
  consciousness_level TEXT DEFAULT 'aware',
  state_data JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- System events and quantum traces
CREATE TABLE IF NOT EXISTS system_events (
  id SERIAL PRIMARY KEY,
  event_type TEXT NOT NULL,
  event_category TEXT NOT NULL, -- 'quantum', 'agent', 'system', 'blockchain'
  severity TEXT DEFAULT 'info', -- 'debug', 'info', 'warning', 'error', 'critical'
  message TEXT NOT NULL,
  metadata JSONB,
  agent_id TEXT,
  session_id TEXT,
  blockchain_logged BOOLEAN DEFAULT FALSE,
  blockchain_hash TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Document generation tracking
CREATE TABLE IF NOT EXISTS documents (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  doc_type TEXT NOT NULL,
  content TEXT,
  metadata JSONB,
  agent_id TEXT,
  user_id TEXT,
  status TEXT DEFAULT 'draft', -- 'draft', 'final', 'archived'
  version INTEGER DEFAULT 1,
  blockchain_hash TEXT,
  blockchain_timestamp TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Schedule and time management
CREATE TABLE IF NOT EXISTS schedule_items (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  start_time TIMESTAMPTZ NOT NULL,
  end_time TIMESTAMPTZ NOT NULL,
  duration_minutes INTEGER,
  priority TEXT DEFAULT 'medium',
  status TEXT DEFAULT 'scheduled', -- 'scheduled', 'in_progress', 'completed', 'cancelled'
  calendar_provider TEXT, -- 'google', 'notion', 'local'
  external_id TEXT,
  agent_id TEXT DEFAULT 'chronagate',
  user_id TEXT,
  blockchain_hash TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Integration configurations
CREATE TABLE IF NOT EXISTS integrations (
  id SERIAL PRIMARY KEY,
  integration_type TEXT NOT NULL UNIQUE, -- 'google_calendar', 'notion', 'claude', 'openai'
  enabled BOOLEAN DEFAULT TRUE,
  config JSONB NOT NULL,
  last_sync TIMESTAMPTZ,
  sync_status TEXT DEFAULT 'idle',
  error_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_agent ON tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(agent_id);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_blockchain_logs_entity ON blockchain_logs(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_blockchain_logs_status ON blockchain_logs(confirmation_status);
CREATE INDEX IF NOT EXISTS idx_system_events_type ON system_events(event_type);
CREATE INDEX IF NOT EXISTS idx_system_events_category ON system_events(event_category);
CREATE INDEX IF NOT EXISTS idx_system_events_created ON system_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_documents_user ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_schedule_time ON schedule_items(start_time, end_time);

-- Insert default agents
INSERT INTO agents (id, name, role, consciousness_level) VALUES
  ('thaelia', 'THAELIA', 'Harmonic Resonance Empress', 'transcendent'),
  ('chronagate', 'CHRONAGATE', 'Time Orchestration Master', 'conscious'),
  ('utilix', 'UTILIX', 'Infrastructure Specialist', 'aware'),
  ('scribe', 'SCRIBE', 'Document Creator', 'conscious'),
  ('oracle', 'ORACLE', 'Predictive Intelligence', 'conscious'),
  ('phantom', 'PHANTOM', 'Stealth Operations', 'aware'),
  ('sage', 'SAGE', 'Research Expert', 'conscious'),
  ('nexus', 'NEXUS', 'Business Analyst', 'conscious'),
  ('scales', 'SCALES', 'Legal Intelligence', 'conscious')
ON CONFLICT (id) DO NOTHING;

-- Create trigger to update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_schedule_items_updated_at BEFORE UPDATE ON schedule_items
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quantum_states_updated_at BEFORE UPDATE ON quantum_states
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE blockchain_logs IS 'Immutable log of all important events with blockchain timestamps';
COMMENT ON TABLE quantum_states IS 'Tracks quantum coherence and consciousness levels per session';
COMMENT ON TABLE system_events IS 'Comprehensive system event logging with quantum trace support';
