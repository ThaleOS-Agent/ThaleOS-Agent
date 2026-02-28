#!/usr/bin/env bash
# ThaleOS LiveOS Start Script
set -euo pipefail

echo "🌌 Starting ThaleOS LiveOS Services..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for compose tool
if command -v podman-compose &> /dev/null; then
    COMPOSE_CMD="podman-compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ No compose tool found. Install podman-compose or docker-compose"
    exit 1
fi

echo "📦 Using: $COMPOSE_CMD"

# Start services
$COMPOSE_CMD --env-file .env up --build -d

echo ""
echo "✅ Services started!"
echo ""
echo "Access points:"
echo "  🌐 API: http://localhost:8080"
echo "  📚 Docs: http://localhost:8080/docs"
echo ""
echo "View logs: scripts/logs.sh"
echo "Test activation: scripts/call-activate.sh"
