#!/usr/bin/env bash
# ThaleOS LiveOS Bootstrap Script
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)

echo "🌌 ThaleOS LiveOS Bootstrap"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Copy environment file
if [ ! -f "$ROOT_DIR/.env" ]; then
    echo "📝 Creating .env from template..."
    cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env" || cat > "$ROOT_DIR/.env" << 'EOF'
# ThaleOS Environment Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8080
POSTGRES_USER=thaleos
POSTGRES_PASSWORD=quantumpassword
POSTGRES_DB=thaleos
REDIS_HOST=redis
REDIS_PORT=6379

# AI APIs
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Blockchain
BLOCKCHAIN_NETWORK=ethereum
BLOCKCHAIN_ENABLE=true
WEB3_PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
EOF
    echo "✅ .env file created"
else
    echo "ℹ️  .env file already exists"
fi

# Create Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv "$ROOT_DIR/api/.venv"
source "$ROOT_DIR/api/.venv/bin/activate"

# Upgrade pip and install dependencies
echo "📦 Installing Python dependencies..."
pip install -U pip
pip install -e "$ROOT_DIR/api" || echo "⚠️  Install from pyproject.toml manually if needed"

echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your configuration"
echo "  2. Run: scripts/build.sh"
echo "  3. Run: scripts/up.sh"
