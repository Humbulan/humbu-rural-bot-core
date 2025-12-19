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
