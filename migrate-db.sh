#!/usr/bin/env bash
# ThaleOS Database Migration Script
set -euo pipefail

echo "🌌 Running ThaleOS Database Migration..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Determine container command
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
else
    echo "❌ Neither podman nor docker found"
    exit 1
fi

# Find database container
DB_CONT=$($CONTAINER_CMD ps --format '{{.Names}}' | grep -E '(db|postgres)' | head -n1)

if [ -z "$DB_CONT" ]; then
    echo "❌ Database container not found. Is it running?"
    echo "Run: scripts/up.sh first"
    exit 1
fi

echo "📊 Found database container: $DB_CONT"

# Copy schema file
echo "📋 Copying schema.sql..."
$CONTAINER_CMD cp api/thaleos/db/schema.sql "$DB_CONT":/schema.sql

# Apply migration
echo "🔨 Applying migration..."
$CONTAINER_CMD exec -i "$DB_CONT" sh -c "psql -U thaleos -d thaleos -f /schema.sql"

echo ""
echo "✅ Migration applied successfully!"
