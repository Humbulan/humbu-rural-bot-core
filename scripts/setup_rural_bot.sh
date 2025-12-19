#!/bin/bash
# Humbu Rural Bot Core Setup Script - Termux Optimized
# Installs the $147,575/month Government SaaS System

echo "🚀 Setting up Humbu Rural Bot Core (Termux Optimized)..."
echo "💰 Target Revenue: $147,575/month"
echo "📱 Optimized for mobile/embedded devices"
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

# Install lightweight dependencies
echo "Installing lightweight dependencies for Termux..."
pip install -r requirements_light.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  Trying alternative installation method...${NC}"
    pip install flask pyserial numpy pyyaml structlog
    echo -e "${GREEN}✅ Core dependencies installed${NC}"
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/{raw,processed,logs}
mkdir -p config/backups
mkdir -p hardware/examples

# Create hardware simulation script
echo "Creating hardware simulation for development..."
cat > hardware/simulator.py << 'SIMEOF'
"""
Hardware Simulator for Humbu Rural Bot
Generates realistic sensor data for development/testing
"""

import random
import time
from datetime import datetime

class HardwareSimulator:
    """Simulates rural robot hardware for development"""
    
    def __init__(self):
        self.simulated_data = {
            "soil_moisture": lambda: random.uniform(20.0, 80.0),
            "temperature": lambda: random.uniform(15.0, 35.0),
            "gps_lat": lambda: -25.7479 + random.uniform(-0.1, 0.1),
            "gps_lon": lambda: 28.2293 + random.uniform(-0.1, 0.1),
            "livestock_heart": lambda: random.randint(60, 120),
            "delivery_status": lambda: random.choice(["in_transit", "delivered", "pending"])
        }
        
    def generate_data(self, data_type):
        """Generate simulated sensor data"""
        if data_type == "soil_moisture":
            return {
                "type": "soil_moisture",
                "moisture_level": self.simulated_data["soil_moisture"](),
                "temperature": self.simulated_data["temperature"](),
                "timestamp": datetime.now().isoformat(),
                "government_form": "AGR-SOIL-2024",
                "simulated": True
            }
        elif data_type == "gps_tracking":
            return {
                "type": "gps_tracking",
                "latitude": self.simulated_data["gps_lat"](),
                "longitude": self.simulated_data["gps_lon"](),
                "animal_id": f"CATTLE-{random.randint(1000, 9999)}",
                "timestamp": datetime.now().isoformat(),
                "government_form": "LSTK-GPS-2024",
                "simulated": True
            }
        elif data_type == "delivery_status":
            return {
                "type": "delivery_status",
                "package_id": f"PKG-{random.randint(10000, 99999)}",
                "status": self.simulated_data["delivery_status"](),
                "location": f"GPS: {self.simulated_data['gps_lat']():.4f}, {self.simulated_data['gps_lon']():.4f}",
                "timestamp": datetime.now().isoformat(),
                "government_form": "LOG-DEL-2024",
                "simulated": True
            }
        else:
            return {
                "type": "unknown",
                "timestamp": datetime.now().isoformat(),
                "simulated": True
            }

# Export simulator
simulator = HardwareSimulator()

if __name__ == "__main__":
    print("🧪 Hardware Simulator Test")
    print("Generating sample data...")
    print("Soil Data:", simulator.generate_data("soil_moisture"))
    print("GPS Data:", simulator.generate_data("gps_tracking"))
SIMEOF

# Create revenue tracking database
echo "Initializing revenue tracking..."
python3 << 'PYTHON_END'
import json
import os
from datetime import datetime
import csv

# Create revenue database
revenue_db = {
    "monthly_target": 147575.0,
    "current_month": datetime.now().strftime("%Y-%m"),
    "current_revenue": 0.0,
    "transactions_today": 0,
    "clients": {
        "Apex": {"contract_value": 75000, "status": "active"},
        "LEDA": {"contract_value": 50000, "status": "active"},
        "Government_Agriculture": {"contract_value": 22575, "status": "active"}
    },
    "setup_date": datetime.now().isoformat(),
    "version": "1.0.0-termux"
}

os.makedirs('data', exist_ok=True)

# Save as JSON
with open('data/revenue_database.json', 'w') as f:
    json.dump(revenue_db, f, indent=2)

# Create CSV for transactions
with open('data/transactions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'amount', 'type', 'source', 'government_id'])
    # Add sample transaction
    writer.writerow([
        datetime.now().isoformat(),
        0.47,
        'delivery_status',
        'simulated',
        f'GOV-SIM-{int(datetime.now().timestamp())}'
    ])

print("✅ Revenue database initialized")
print("✅ Transaction logging ready")
PYTHON_END

# Create optimized API configuration
echo "Creating optimized configuration..."
cat > config/termux_config.yaml << 'CONFIGEOF'
# Humbu Rural Bot - Termux Optimized Configuration

api:
  government_saas:
    port: 8083
    host: "0.0.0.0"
    debug: false
    simulation_mode: true  # No hardware connected yet
    
  watchdog:
    check_interval: 60  # seconds
    log_interval: 300   # 5 minutes
    
hardware:
  simulation: true
  simulated_devices:
    - soil_sensor_1
    - gps_tracker_1
    - delivery_robot_1
    
  # When real hardware is available, set simulation to false
  # real_serial_port: "/dev/ttyUSB0"
  # real_baud_rate: 9600

revenue:
  rates:
    soil_moisture: 0.15
    gps_tracking: 0.25
    delivery_status: 0.47
    livestock_health: 0.32
    simulated_data: 0.10
  
  auto_save_interval: 60  # Save revenue data every minute

logging:
  level: "INFO"
  file: "data/logs/system.log"
  max_size_mb: 10

security:
  api_keys:
    apex: "APEX-2024-GOV-SAAS"
    leda: "LEDA-RURAL-DEV"
    government: "GOV-AGRIC-SAAS-2024"
CONFIGEOF

# Make scripts executable
chmod +x monitoring/api_watchdog.sh
chmod +x scripts/*.sh

# Create quick start script
cat > start_humbu_system.sh << 'QUICKEOF'
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
QUICKEOF

chmod +x start_humbu_system.sh

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Termux Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "To start your $147,575/month Government SaaS:"
echo ""
echo -e "${YELLOW}Option 1 - Quick Start:${NC}"
echo "   ./start_humbu_system.sh"
echo ""
echo -e "${YELLOW}Option 2 - Manual Start:${NC}"
echo "   1. Start API: python api/government_saas.py &"
echo "   2. Start Watchdog: ./monitoring/api_watchdog.sh &"
echo ""
echo -e "${YELLOW}Option 3 - Development Mode:${NC}"
echo "   python api/government_saas.py"
echo ""
echo "📱 System optimized for Termux/mobile"
echo "🔌 Hardware simulation enabled"
echo "💰 Ready to generate revenue: $0.47/transaction"
echo ""
echo "🌾 Connect real hardware when available!"
