#!/bin/bash
# Quick Start - Humbu Rural Bot System

echo "🚀 Starting Humbu $147,575/month System..."

# Check if already running
if pgrep -f "government_saas.py" > /dev/null; then
    echo "⚠️  API is already running. Restarting..."
    pkill -f "government_saas.py"
    sleep 2
fi

# Start the Government SaaS API
echo "Starting Government SaaS API (Port 8083)..."
cd "$(dirname "$0")"
nohup python api/government_saas.py > data/logs/api.log 2>&1 &
API_PID=$!
echo "API started with PID: $API_PID"

# Wait for API to start
sleep 3

# Check if API is running
if curl -s http://localhost:8083/health > /dev/null; then
    echo "✅ Government SaaS API is LIVE on port 8083"
    echo "🌐 Access dashboard: http://localhost:8083"
    echo "💰 Revenue tracking: http://localhost:8083/revenue"
else
    echo "❌ API failed to start. Check data/logs/api.log"
    exit 1
fi

# Start watchdog if not running
if ! pgrep -f "api_watchdog.sh" > /dev/null; then
    echo "Starting Revenue Protection Watchdog..."
    nohup ./monitoring/api_watchdog.sh > data/logs/watchdog.log 2>&1 &
    echo "✅ Watchdog started"
fi

# Show status
echo ""
echo "========================================"
echo "HUMBU RURAL BOT SYSTEM STATUS"
echo "========================================"
echo "💰 Monthly Target: $147,575"
echo "🌱 Mode: Simulation (Ready for hardware)"
echo "📡 API: http://localhost:8083"
echo "🔧 Hardware: Simulated - Connect real devices via USB"
echo "📊 Logs: data/logs/"
echo ""
echo "To test the system:"
echo "curl http://localhost:8083/"
echo "curl http://localhost:8083/revenue"
echo ""
echo "Press Ctrl+C to stop (API continues in background)"
echo "Use: pkill -f 'government_saas.py' to stop completely"
