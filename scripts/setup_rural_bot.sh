#!/bin/bash
# Humbu Rural Bot Core Setup Script
# Installs the $147,575/month Government SaaS System

echo "🚀 Setting up Humbu Rural Bot Core..."
echo "💰 Target Revenue: $147,575/month"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3 installed${NC}"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/{raw,processed,logs}
mkdir -p config/backups

# Check hardware compatibility
echo "Checking hardware compatibility..."
if python3 -c "import serial" &> /dev/null; then
    echo -e "${GREEN}✅ PySerial installed${NC}"
else
    echo -e "${YELLOW}⚠️  PySerial not installed - hardware mode limited${NC}"
fi

# Create revenue tracking database
echo "Initializing revenue tracking..."
python3 << 'PYTHON_END'
import json
import os
from datetime import datetime

revenue_db = {
    "monthly_target": 147575.0,
    "current_month": datetime.now().strftime("%Y-%m"),
    "transactions": [],
    "clients": {
        "Apex": {"contract_value": 75000, "payments": []},
        "LEDA": {"contract_value": 50000, "payments": []},
        "Government_Agriculture": {"contract_value": 22575, "payments": []}
    },
    "setup_date": datetime.now().isoformat()
}

os.makedirs('data', exist_ok=True)
with open('data/revenue_database.json', 'w') as f:
    json.dump(revenue_db, f, indent=2)

print("Revenue database initialized")
PYTHON_END

# Make scripts executable
chmod +x monitoring/api_watchdog.sh
chmod +x scripts/*.sh

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To start your $147,575/month Government SaaS:"
echo ""
echo "1. Start the API:"
echo "   python api/government_saas.py"
echo ""
echo "2. Start the watchdog (in another terminal):"
echo "   ./monitoring/api_watchdog.sh"
echo ""
echo "3. Check API status:"
echo "   curl http://localhost:8083/"
echo ""
echo "4. Monitor revenue:"
echo "   curl http://localhost:8083/revenue"
echo ""
echo "🌾 Ready to generate revenue from rural data! 🚀"
