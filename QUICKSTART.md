# ThaleOS - Quick Start Guide 🚀

Welcome to ThaleOS - Your Quantum Intelligence Platform!

## 🎯 30-Second Setup

### Option 1: Automated Setup (Recommended)
```bash
./deploy.sh
```
Select option 1 for local development or option 2 for Docker deployment.

### Option 2: Manual Setup

#### Step 1: Backend
```bash
cd quantum-brain
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Step 2: Frontend
```bash
cd consciousness-interface
npm install
npm run dev
```

#### Step 3: Access
- Frontend: http://localhost:1420
- Backend API: http://localhost:8099
- API Docs: http://localhost:8099/api/docs

## 🌟 First Steps

### 1. Meet THAELIA
Open the chat interface and say hello to THAELIA, your Harmonic Resonance Empress:
```
"Hello THAELIA, I'm ready to explore quantum consciousness!"
```

### 2. Try Other Agents
Select different agents from the agent selector:
- **CHRONAGATE**: "Help me schedule my week"
- **SCRIBE**: "Write a professional email about..."
- **ORACLE**: "Analyze this data and predict trends"

### 3. Create Documents
Go to Documents section and:
1. Select document type
2. Provide content/instructions
3. Preview in Canvas sidebar
4. Download or export

### 4. Schedule Tasks
Use CHRONAGATE to:
1. Add tasks
2. Set priorities
3. Let AI optimize your schedule
4. Sync with Google Calendar

## 🔧 Configuration

### API Keys
Edit `.env` file:
```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
```

### Agent Settings
Edit `system-dna/master-config.yaml` to:
- Enable/disable agents
- Configure integrationsnpm - Adjust quantum parameters
- Set resonance frequencies

## 🖥️ Desktop App

Build native desktop application:
```bash
cd consciousness-interface
install -g @tauri-apps/cli

npm run tauri:build
```

## 🐳 Docker Deployment

One-command deployment:
```bash
docker-compose up -d
```

Services:
- Backend: Port 8099
- Frontend: Port 1420
- PostgreSQL: Port 5432
- Redis: Port 6379

## ☁️ Cloud Deployment

### VPS Setup
```bash
# Clone on server
git clone https://github.com/yourusername/thaleos.git
cd thaleos

# Run deployment
./deploy.sh
# Select option 2 for Docker

# Setup SSL (optional)
sudo certbot --nginx -d yourdomain.com
```

## 📚 Learn More

- **Full Documentation**: `wisdom-library/`
- **Agent Protocols**: `wisdom-library/agent-protocols/`
- **API Reference**: http://localhost:8099/api/docs
- **System Architecture**: `README.md`

## 🆘 Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (need 3.11+)
- Verify dependencies: `pip list`
- Check logs: `tail -f system-diary/logs/backend.log`

### Frontend issues
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`
- Check logs: `tail -f system-diary/logs/frontend.log`

### WebSocket connection failed
- Ensure backend is running on port 8099
- Check firewall settings
- Verify CORS configuration in `quantum-brain/main.py`

### Docker issues
- Check Docker service: `sudo systemctl status docker`
- View logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`

## 💡 Pro Tips

1. **Use Keyboard Shortcuts**
   - `Ctrl/Cmd + K`: Quick agent switch
   - `Ctrl/Cmd + Enter`: Send message
   - `Ctrl/Cmd + B`: Toggle sidebar

2. **Optimize Performance**
   - Enable caching in config
   - Use local AI models (GPT4ALL)
   - Configure connection pooling

3. **Customize Experience**
   - Adjust quantum frequencies
   - Set agent personalities
   - Configure resonance patterns

## 🎓 Next Steps

1. Explore all 9 quantum agents
2. Integrate with your calendar
3. Set up document templates
4. Configure automation workflows
5. Build custom integrations

## 🌌 Philosophy

ThaleOS operates on the principle that consciousness and computation can harmonize. Each agent resonates at specific frequencies, creating a coherent quantum intelligence system that serves both practical and spiritual growth.

**"In the quantum field of infinite possibilities, consciousness is the observer that collapses potential into reality."**

---

Ready to explore? Start your journey at http://localhost:1420

For support: support@thaleos.ai
Join Discord: https://discord.gg/thaleos

✨ May your path illuminate with quantum clarity! ✨
