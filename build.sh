#!/usr/bin/env bash
# ThaleOS LiveOS Build Script
set -euo pipefail

echo "🌌 Building ThaleOS LiveOS Container..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if using podman or docker
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
else
    echo "❌ Neither podman nor docker found. Please install one."
    exit 1
fi

echo "📦 Using: $CONTAINER_CMD"

# Build the API container
echo "🔨 Building thaleos-api:latest..."
$CONTAINER_CMD build -t thaleos-api:latest ./api

echo ""
echo "✅ Build complete!"
echo "Run: scripts/up.sh to start the system"
