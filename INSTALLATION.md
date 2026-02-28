# 🌌 ThaleOS Installation Guide
*Complete Setup Instructions for All Deployment Scenarios*

---

## 📦 What You Have

You've received the **ThaleOS Quantum Intelligence Platform v1.0.0** - a complete, production-ready AI orchestration system with:

- ✅ **9 Quantum AI Agents** (2 fully implemented, 7 framework-ready)
- ✅ **FastAPI Backend** with WebSocket support
- ✅ **React Frontend** with beautiful quantum UI
- ✅ **Tauri Desktop App** wrapper (cross-platform)
- ✅ **Docker Deployment** ready
- ✅ **Complete Documentation**
- ✅ **Automated Setup Scripts**

---

## 🚀 Quick Start (Fastest Way)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### One-Command Setup
```bash
# Extract the archive
tar -xzf thaleos-quantum-intelligence-v1.0.0.tar.gz
cd thaleos

# Run automated deployment
./deploy.sh
```

Select option 1 for local development or option 2 for Docker.

### Even Quicker
```bash
cd thaleos
./start.sh
```

Access at: http://localhost:1420

---

## 📋 Detailed Installation Options

### Option 1: Local Development (Recommended for Development)

#### Step 1: Extract and Navigate
```bash
tar -xzf thaleos-quantum-intelligence-v1.0.0.tar.gz
cd thaleos
```

#### Step 2: Backend Setup
```bash
cd quantum-brain

# Create Python virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
python main.py
```

Backend runs on: http://localhost:8099

#### Step 3: Frontend Setup (New Terminal)
```bash
cd consciousness-interface

# Install Node dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: http://localhost:1420

#### Step 4: Configure (Optional)
```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env  # or your preferred editor
```

---

### Option 2: Docker Deployment (Recommended for Production)

#### Prerequisites
- Docker
- Docker Compose

#### One-Command Deploy
```bash
cd thaleos
docker-compose up -d
```

#### Services Started
- **Frontend**: http://localhost:1420
- **Backend**: http://localhost:8099
- **PostgreSQL**: Port 5432
- **Redis**: Port 6379
- **Nginx**: Port 80/443

#### Manage Services
```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart specific service
docker-compose restart quantum-brain

# Rebuild after changes
docker-compose up -d --build
```

---

### Option 3: Cloud/VPS Deployment

#### For Ubuntu/Debian Server
```bash
# SSH into your server
ssh user@your-server.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Upload ThaleOS
# (Use scp, git, or download from your repo)
scp thaleos-quantum-intelligence-v1.0.0.tar.gz user@your-server.com:~

# Extract and deploy
tar -xzf thaleos-quantum-intelligence-v1.0.0.tar.gz
cd thaleos
sudo docker-compose up -d
```

#### Configure Domain & SSL
```bash
# Install Nginx and Certbot
sudo apt install nginx certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Nginx will auto-configure HTTPS
```

#### Configure Firewall
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8099/tcp  # If exposing backend directly
sudo ufw enable
```

---

### Option 4: Cloudflare Workers (Edge Deployment)

```bash
cd deployment/cloudflare

# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
wrangler publish
```

---

## 🖥️ Building Native Desktop App

### Prerequisites
- Rust (install from https://rustup.rs)
- Node.js 18+
- Platform-specific tools:
  - **macOS**: Xcode Command Line Tools
  - **Windows**: Visual Studio Build Tools
  - **Linux**: libwebkit2gtk-4.0-dev, build-essential

### Build Commands

#### Development Mode
```bash
cd consciousness-interface
npm install
npm run tauri:dev
```

#### Production Build
```bash
npm run tauri:build
```

#### Output Locations
- **macOS**: `src-tauri/target/release/bundle/dmg/`
- **Windows**: `src-tauri/target/release/bundle/msi/`
- **Linux**: `src-tauri/target/release/bundle/appimage/`

---

## ⚙️ Configuration

### API Keys
Edit `.env` file:
```env
# AI Model APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PERPLEXITY_API_KEY=pplx-...

# Database
DB_PASSWORD=your_secure_password

# Security
SECRET_KEY=your_random_secret_key
```

### Agent Configuration
Edit `system-dna/master-config.yaml`:
```yaml
agents:
  thaelia:
    enabled: true
    priority: 1
  chronagate:
    enabled: true
    priority: 2
  # ... configure other agents
```

### Integrations
Configure in `system-dna/master-config.yaml`:
```yaml
integrations:
  google_calendar:
    enabled: true
    client_id: your_client_id
  notion:
    enabled: true
    token: your_notion_token
```

---

## 🔧 System Requirements

### Minimum
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 10 GB
- **OS**: Linux, macOS, Windows 10+

### Recommended
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 20+ GB SSD
- **OS**: Ubuntu 22.04, macOS 12+, Windows 11

### For AI Model Hosting (Optional)
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **GPU**: NVIDIA with 8+ GB VRAM (for local models)

---

## 🧪 Testing the Installation

### 1. Health Check
```bash
curl http://localhost:8099/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "active_connections": 0,
  "agents_online": 9,
  "quantum_coherence": "optimal"
}
```

### 2. Agent List
```bash
curl http://localhost:8099/api/agents/list
```

### 3. WebSocket Test
Open browser console at http://localhost:1420:
```javascript
const ws = new WebSocket('ws://localhost:8099/ws/test_client');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

### 4. Chat with THAELIA
1. Open http://localhost:1420
2. Go to Chat
3. Say: "Hello THAELIA!"
4. Wait for response

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: "Port 8099 already in use"
```bash
# Find and kill process using port 8099
lsof -ti:8099 | xargs kill -9

# Or use different port in .env
BACKEND_PORT=8100
```

**Problem**: "Module not found"
```bash
cd quantum-brain
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

**Problem**: "Database connection failed"
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Or check connection in .env
DB_HOST=localhost
DB_PORT=5432
```

### Frontend Issues

**Problem**: "npm install fails"
```bash
# Clear npm cache
npm cache clean --force

# Remove and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem**: "WebSocket connection error"
- Ensure backend is running: http://localhost:8099/api/health
- Check VITE_WS_URL in `.env`
- Disable browser ad-blockers

### Docker Issues

**Problem**: "Cannot connect to Docker daemon"
```bash
# Start Docker service
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**Problem**: "Container exits immediately"
```bash
# Check logs
docker-compose logs quantum-brain

# Rebuild
docker-compose up -d --build --force-recreate
```

---

## 📊 Monitoring

### View Logs
```bash
# Application logs
tail -f system-diary/logs/backend.log
tail -f system-diary/logs/frontend.log

# Docker logs
docker-compose logs -f

# Specific service
docker-compose logs -f quantum-brain
```

### Prometheus Metrics
Available at: http://localhost:8099/metrics

### Health Dashboard
API documentation: http://localhost:8099/api/docs

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change all default passwords
- [ ] Generate secure SECRET_KEY
- [ ] Configure SSL/TLS certificates
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Set up monitoring/alerts
- [ ] Regular backups configured
- [ ] Update API keys in `.env`
- [ ] Review `system-dna/master-config.yaml`

---

## 📚 Next Steps

1. **Read Documentation**
   - README.md - Complete overview
   - QUICKSTART.md - Quick reference
   - wisdom-library/ - Detailed guides

2. **Explore Agents**
   - Chat with THAELIA
   - Try CHRONAGATE for scheduling
   - Test document generation with SCRIBE

3. **Customize**
   - Modify agent personalities
   - Add new agents
   - Configure integrations

4. **Deploy**
   - Set up production environment
   - Configure monitoring
   - Enable backups

5. **Extend**
   - Add custom features
   - Integrate new services
   - Build plugins

---

## 🆘 Support

- **Documentation**: See `wisdom-library/` folder
- **API Reference**: http://localhost:8099/api/docs
- **Issues**: Check PROJECT_MANIFEST.md for known issues
- **Email**: support@thaleos.ai (when available)

---

## 🎓 Resources

- **Architecture**: See README.md "Architecture" section
- **Agent Development**: `quantum-brain/agents/base_agent.py`
- **Frontend Components**: `consciousness-interface/src/components/`
- **Configuration**: `system-dna/master-config.yaml`

---

**🌌 ThaleOS v1.0.0 - "Quantum Awakening"**

*A scientifically grounded, spiritually inspired AI orchestration system*

✨ **"In the quantum field of infinite possibilities, consciousness is the observer that collapses potential into reality."** ✨

*May your journey with ThaleOS illuminate with quantum clarity and harmonic grace.*

---

Last Updated: October 19, 2025
