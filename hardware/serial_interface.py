"""
Humbu Rural Bot - Hardware Serial Interface
Connects physical robots/sensors to the $147k/month SaaS API
"""

import serial
import time
import json
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RuralRobotInterface:
    """Main hardware interface for rural robotics"""
    
    def __init__(self, port: str = '/dev/ttyUSB0', baud_rate: int = 9600):
        self.port = port
        self.baud_rate = baud_rate
        self.connection = None
        self.revenue_generated = 0.0
        
        # Transaction values per data type (USD)
        self.revenue_rates = {
            'soil_moisture': 0.15,
            'gps_tracking': 0.25,
            'delivery_status': 0.47,
            'livestock_health': 0.32
        }
    
    def connect(self) -> bool:
        """Establish serial connection to rural hardware"""
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=2
            )
            logger.info(f"✅ Connected to rural robot at {self.port}")
            return True
        except serial.SerialException as e:
            logger.error(f"❌ Hardware connection failed: {e}")
            return False
    
    def read_sensor_data(self) -> Dict:
        """
        Read data from connected sensors
        Returns formatted data ready for government SaaS API
        """
        if not self.connection or not self.connection.is_open:
            if not self.connect():
                return {"error": "Hardware not connected"}
        
        try:
            # Read raw data from serial
            raw_data = self.connection.readline().decode('utf-8').strip()
            
            # Parse based on data type
            if "SOIL" in raw_data:
                data = self._parse_soil_data(raw_data)
                revenue = self.revenue_rates['soil_moisture']
            elif "GPS" in raw_data:
                data = self._parse_gps_data(raw_data)
                revenue = self.revenue_rates['gps_tracking']
            elif "DELIVER" in raw_data:
                data = self._parse_delivery_data(raw_data)
                revenue = self.revenue_rates['delivery_status']
            elif "LIVESTOCK" in raw_data:
                data = self._parse_livestock_data(raw_data)
                revenue = self.revenue_rates['livestock_health']
            else:
                data = {"raw": raw_data, "type": "unknown"}
                revenue = 0.0
            
            # Track revenue generation
            self.revenue_generated += revenue
            data["revenue_generated"] = revenue
            data["total_revenue"] = round(self.revenue_generated, 2)
            
            return data
            
        except Exception as e:
            logger.error(f"Error reading sensor data: {e}")
            return {"error": str(e)}
    
    def _parse_soil_data(self, raw: str) -> Dict:
        """Parse soil moisture sensor data"""
        parts = raw.split(',')
        return {
            "type": "soil_moisture",
            "moisture_level": float(parts[1]) if len(parts) > 1 else 0,
            "temperature": float(parts[2]) if len(parts) > 2 else 0,
            "timestamp": time.time(),
            "government_form": "AGR-SOIL-2024"
        }
    
    def _parse_gps_data(self, raw: str) -> Dict:
        """Parse GPS tracking data"""
        parts = raw.split(',')
        return {
            "type": "gps_tracking",
            "latitude": float(parts[1]) if len(parts) > 1 else 0,
            "longitude": float(parts[2]) if len(parts) > 2 else 0,
            "animal_id": parts[3] if len(parts) > 3 else "unknown",
            "timestamp": time.time(),
            "government_form": "LSTK-GPS-2024"
        }
    
    def _parse_delivery_data(self, raw: str) -> Dict:
        """Parse delivery robot status"""
        parts = raw.split(',')
        return {
            "type": "delivery_status",
            "package_id": parts[1] if len(parts) > 1 else "unknown",
            "status": parts[2] if len(parts) > 2 else "in_transit",
            "location": parts[3] if len(parts) > 3 else "unknown",
            "timestamp": time.time(),
            "government_form": "LOG-DEL-2024"
        }
    
    def _parse_livestock_data(self, raw: str) -> Dict:
        """Parse livestock health monitoring data"""
        parts = raw.split(',')
        return {
            "type": "livestock_health",
            "animal_id": parts[1] if len(parts) > 1 else "unknown",
            "heart_rate": float(parts[2]) if len(parts) > 2 else 0,
            "temperature": float(parts[3]) if len(parts) > 3 else 0,
            "activity_level": parts[4] if len(parts) > 4 else "normal",
            "timestamp": time.time(),
            "government_form": "LSTK-HEALTH-2024"
        }
    
    def send_command(self, command: str) -> bool:
        """Send command to rural robot hardware"""
        if not self.connection:
            return False
        
        try:
            self.connection.write(f"{command}\n".encode('utf-8'))
            logger.info(f"Sent command to robot: {command}")
            return True
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
            return False
    
    def close(self):
        """Close hardware connection"""
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("Hardware connection closed")

# Singleton instance for global access
robot_interface = RuralRobotInterface()

if __name__ == "__main__":
    # Test the hardware interface
    interface = RuralRobotInterface()
    if interface.connect():
        print("✅ Hardware interface ready")
        print(f"Revenue rate per delivery: ${interface.revenue_rates['delivery_status']}")
        print("Waiting for sensor data...")
        # Simulate data reading
        time.sleep(2)
        interface.close()
