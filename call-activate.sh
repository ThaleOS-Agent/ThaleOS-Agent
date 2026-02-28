#!/usr/bin/env bash
# ThaleOS LiveOS Activation Test
set -euo pipefail

echo "🌌 Testing ThaleOS Activation Endpoint..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test if jq is available
if ! command -v jq &> /dev/null; then
    echo "⚠️  jq not found, showing raw response"
    curl -s -X POST http://localhost:8080/activate \
      -H 'Content-Type: application/json' \
      -d '{"goal":"smoke test full harmonic resonance"}'
else
    curl -s -X POST http://localhost:8080/activate \
      -H 'Content-Type: application/json' \
      -d '{"goal":"smoke test full harmonic resonance"}' | jq
fi

echo ""
