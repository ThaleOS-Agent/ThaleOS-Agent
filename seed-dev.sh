#!/usr/bin/env bash
# ThaleOS Database Seed Script
set -euo pipefail

echo "🌌 Seeding ThaleOS Database..."
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
    echo "❌ Database container not found"
    exit 1
fi

echo "📊 Found database container: $DB_CONT"

# Copy seed file
echo "📋 Copying seed.sql..."
$CONTAINER_CMD cp api/thaleos/db/seed.sql "$DB_CONT":/seed.sql

# Apply seed
echo "🌱 Inserting seed data..."
$CONTAINER_CMD exec -i "$DB_CONT" sh -c "psql -U thaleos -d thaleos -f /seed.sql"

echo ""
echo "✅ Seed data inserted successfully!"
