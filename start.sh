#!/bin/bash
# ThaleOS One-Command Launcher
# Quick start for development

echo "🌌 ThaleOS Quantum Intelligence Platform"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Start backend
echo "🧠 Starting Quantum Brain (Backend)..."
cd quantum-brain
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
python main.py &
BACKEND_PID=$!
cd ..

sleep 3

# Start frontend
echo "✨ Starting Consciousness Interface (Frontend)..."
cd consciousness-interface
npm install --silent 2>/dev/null
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ThaleOS is now running!"
echo ""
echo "🌐 Frontend: http://localhost:1420"
echo "🔧 Backend:  http://localhost:8099"
echo "📚 API Docs: http://localhost:8099/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Wait for Ctrl+C
trap "echo ''; echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
