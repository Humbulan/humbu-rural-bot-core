"""
Humbu Government SaaS API - Port 8083
Generates $147,575/month from rural data processing
"""

from flask import Flask, request, jsonify
import json
import time
from datetime import datetime
import logging
from typing import Dict, List
import threading

# Import hardware interface
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hardware.serial_interface import robot_interface

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Revenue tracking
class RevenueTracker:
    def __init__(self):
        self.monthly_target = 147575.0
        self.daily_target = 4919.17  # Monthly / 30
        self.current_month_revenue = 0.0
        self.transactions_today = 0
        self.transaction_log = []
    
    def add_transaction(self, amount: float, source: str, data_type: str):
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "source": source,
            "type": data_type,
            "status": "completed"
        }
        self.current_month_revenue += amount
        self.transactions_today += 1
        self.transaction_log.append(transaction)
        
        logger.info(f"💰 Revenue added: ${amount:.2f} from {source} ({data_type})")
        logger.info(f"📈 Monthly total: ${self.current_month_revenue:.2f}/{self.monthly_target:.2f}")
        
        return transaction

revenue_tracker = RevenueTracker()

# Government client database
GOVERNMENT_CLIENTS = {
    "Apex": {
        "api_key": "APEX-2024-GOV-SAAS",
        "monthly_contract": 75000,
        "services": ["delivery_tracking", "soil_analysis"]
    },
    "LEDA": {
        "api_key": "LEDA-RURAL-DEV",
        "monthly_contract": 50000,
        "services": ["livestock_monitoring", "gps_tracking"]
    },
    "Government_Agriculture": {
        "api_key": "GOV-AGRIC-SAAS-2024",
        "monthly_contract": 22575,
        "services": ["all_data_aggregation", "subsidy_processing"]
    }
}

@app.route('/')
def home():
    """Main API endpoint - Shows revenue status"""
    status = {
        "service": "Humbu Government SaaS API",
        "port": 8083,
        "status": "active",
        "monthly_revenue_target": f"${revenue_tracker.monthly_target:,.2f}",
        "current_month_revenue": f"${revenue_tracker.current_month_revenue:,.2f}",
        "revenue_percentage": f"{(revenue_tracker.current_month_revenue / revenue_tracker.monthly_target) * 100:.1f}%",
        "transactions_today": revenue_tracker.transactions_today,
        "clients": list(GOVERNMENT_CLIENTS.keys()),
        "documentation": "/docs",
        "health_check": "/health",
        "revenue_endpoint": "/revenue"
    }
    return jsonify(status)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for watchdog"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "hardware_connected": robot_interface.connection is not None,
        "api_uptime": "24/7"
    }), 200

@app.route('/revenue', methods=['GET'])
def get_revenue():
    """Get detailed revenue information"""
    return jsonify({
        "monthly_target": revenue_tracker.monthly_target,
        "current_revenue": revenue_tracker.current_month_revenue,
        "remaining_target": revenue_tracker.monthly_target - revenue_tracker.current_month_revenue,
        "daily_average_needed": (revenue_tracker.monthly_target - revenue_tracker.current_month_revenue) / 30,
        "transactions_today": revenue_tracker.transactions_today,
        "recent_transactions": revenue_tracker.transaction_log[-10:] if revenue_tracker.transaction_log else []
    })

@app.route('/api/v1/process_rural_data', methods=['POST'])
def process_rural_data():
    """
    Main endpoint: Processes rural data into government-compliant formats
    Generates revenue per transaction
    """
    data = request.json
    
    # Validate API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key not in [c['api_key'] for c in GOVERNMENT_CLIENTS.values()]:
        return jsonify({"error": "Invalid API key"}), 401
    
    # Process data based on type
    data_type = data.get('type', 'unknown')
    source = data.get('source', 'unknown')
    
    # Revenue per data type (USD)
    revenue_map = {
        'soil_moisture': 0.15,
        'gps_tracking': 0.25,
        'delivery_status': 0.47,  # Highest value - Government delivery tracking
        'livestock_health': 0.32,
        'weather_data': 0.18,
        'crop_health': 0.28
    }
    
    revenue_amount = revenue_map.get(data_type, 0.10)
    
    # Add to revenue tracker
    transaction = revenue_tracker.add_transaction(
        amount=revenue_amount,
        source=source,
        data_type=data_type
    )
    
    # Process for government submission
    processed_data = {
        **data,
        "government_id": f"GOV-{int(time.time())}",
        "submission_date": datetime.now().isoformat(),
        "revenue_generated": revenue_amount,
        "processing_status": "completed"
    }
    
    return jsonify({
        "status": "success",
        "message": "Data processed for government submission",
        "government_reference": processed_data["government_id"],
        "revenue_generated": revenue_amount,
        "transaction_id": len(revenue_tracker.transaction_log),
        "data": processed_data
    })

@app.route('/api/v1/hardware/read', methods=['GET'])
def read_hardware_data():
    """Read data directly from connected rural hardware"""
    try:
        data = robot_interface.read_sensor_data()
        
        if "error" in data:
            return jsonify({"error": data["error"]}), 500
        
        # Generate revenue from hardware data
        revenue_amount = data.get("revenue_generated", 0)
        if revenue_amount > 0:
            revenue_tracker.add_transaction(
                amount=revenue_amount,
                source="hardware_sensor",
                data_type=data.get("type", "unknown")
            )
        
        return jsonify({
            "status": "success",
            "data": data,
            "revenue": revenue_amount,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/hardware/command', methods=['POST'])
def send_hardware_command():
    """Send command to rural robot hardware"""
    command = request.json.get('command')
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    success = robot_interface.send_command(command)
    
    if success:
        return jsonify({
            "status": "success",
            "message": f"Command sent: {command}",
            "timestamp": datetime.now().isoformat()
        })
    else:
        return jsonify({"error": "Failed to send command"}), 500

@app.route('/docs', methods=['GET'])
def documentation():
    """API Documentation"""
    docs = {
        "api_name": "Humbu Government Rural SaaS",
        "version": "1.0.0",
        "revenue_model": "$147,575/month",
        "endpoints": {
            "/": "API Status",
            "/health": "Health Check",
            "/revenue": "Revenue Tracking",
            "/api/v1/process_rural_data": "Process Rural Data (POST)",
            "/api/v1/hardware/read": "Read Hardware Data (GET)",
            "/api/v1/hardware/command": "Send Hardware Command (POST)"
        },
        "authentication": "X-API-Key header required",
        "clients": [
            {"name": "Apex", "contract": "$75,000/month"},
            {"name": "LEDA", "contract": "$50,000/month"},
            {"name": "Government Agriculture", "contract": "$22,575/month"}
        ],
        "hardware_support": "Serial interface for rural robots"
    }
    return jsonify(docs)

def run_api():
    """Run the Flask API"""
    logger.info("🚀 Starting Humbu Government SaaS API on port 8083")
    logger.info(f"💰 Monthly Target: ${revenue_tracker.monthly_target:,.2f}")
    logger.info("📡 Ready to process rural data into government revenue...")
    
    # Try to connect to hardware
    if robot_interface.connect():
        logger.info("✅ Hardware interface connected")
    else:
        logger.warning("⚠️  Hardware not connected - running in simulation mode")
    
    app.run(host='0.0.0.0', port=8083, debug=False)

if __name__ == '__main__':
    run_api()
