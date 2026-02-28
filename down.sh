#!/usr/bin/env bash
# ThaleOS LiveOS Stop Script
set -euo pipefail

echo "🌌 Stopping ThaleOS LiveOS Services..."

# Check for compose tool
if command -v podman-compose &> /dev/null; then
    COMPOSE_CMD="podman-compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ No compose tool found"
    exit 1
fi

$COMPOSE_CMD down

echo "✅ Services stopped"
