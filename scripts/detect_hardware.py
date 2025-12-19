#!/usr/bin/env python3
"""
Humbu Hardware Detector
Scans for connected rural hardware devices
"""

import serial.tools.list_ports
import subprocess
import json
from datetime import datetime

def detect_usb_devices():
    """Detect all USB serial devices"""
    print("🔍 Scanning for USB devices...")
    devices = []
    
    # List all serial ports
    ports = list(serial.tools.list_ports.comports())
    
    for port in ports:
        device_info = {
            "device": port.device,
            "name": port.name,
            "description": port.description,
            "manufacturer": port.manufacturer,
            "product": port.product,
            "hwid": port.hwid
        }
        devices.append(device_info)
        
        print(f"✅ Found: {port.device}")
        print(f"   Name: {port.name}")
        print(f"   Description: {port.description}")
        if port.manufacturer:
            print(f"   Manufacturer: {port.manufacturer}")
        if port.product:
            print(f"   Product: {port.product}")
        print()
    
    return devices

def detect_gpio():
    """Check for GPIO capabilities (Raspberry Pi)"""
    print("🔌 Checking GPIO capabilities...")
    
    gpio_info = {
        "has_gpio": False,
        "platform": "unknown",
        "gpio_pins": 0
    }
    
    try:
        # Check if we're on Raspberry Pi
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo:
                gpio_info["has_gpio"] = True
                gpio_info["platform"] = "Raspberry Pi"
                gpio_info["gpio_pins"] = 40
                print("✅ Raspberry Pi detected (40 GPIO pins)")
    except:
        pass
    
    return gpio_info

def detect_network_interfaces():
    """Detect network interfaces"""
    print("🌐 Checking network interfaces...")
    
    interfaces = []
    try:
        result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        current_iface = None
        for line in lines:
            if line and not line.startswith(' '):
                if ':' in line:
                    current_iface = line.split(':')[1].strip()
                    interfaces.append({
                        "interface": current_iface,
                        "ip_addresses": []
                    })
            elif 'inet ' in line and current_iface:
                ip = line.split('inet ')[1].split('/')[0]
                interfaces[-1]["ip_addresses"].append(ip)
        
        for iface in interfaces:
            if iface["ip_addresses"]:
                print(f"✅ {iface['interface']}: {', '.join(iface['ip_addresses'])}")
    except:
        print("⚠️  Could not detect network interfaces")
    
    return interfaces

def generate_hardware_report():
    """Generate complete hardware report"""
    print("="*60)
    print("🤖 HUMBU HARDWARE DETECTION REPORT")
    print("="*60)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "system": "Humbu Rural Bot Core",
        "usb_devices": detect_usb_devices(),
        "gpio": detect_gpio(),
        "network": detect_network_interfaces(),
        "recommendations": []
    }
    
    # Generate recommendations
    if not report["usb_devices"]:
        report["recommendations"].append(
            "No USB devices found. Connect sensors via USB OTG adapter."
        )
    else:
        report["recommendations"].append(
            f"Found {len(report['usb_devices'])} USB device(s). Update config/settings.yaml."
        )
    
    if report["gpio"]["has_gpio"]:
        report["recommendations"].append(
            "Raspberry Pi detected. Enable GPIO in hardware/serial_interface.py"
        )
    
    print("\n📋 RECOMMENDATIONS:")
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"  {i}. {rec}")
    
    print("\n💾 Saving report to data/hardware_report.json")
    with open('data/hardware_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("✅ Hardware detection complete!")
    return report

def auto_configure():
    """Auto-configure system based on detected hardware"""
    print("\n⚙️  Attempting auto-configuration...")
    
    report = generate_hardware_report()
    
    # Update config if USB devices found
    if report["usb_devices"]:
        print("\n🔧 Updating configuration for detected devices:")
        for device in report["usb_devices"]:
            print(f"  - Adding {device['device']} to config")
        
        # Create hardware configuration
        config_update = {
            "hardware": {
                "simulation_mode": False,
                "serial_ports": [d["device"] for d in report["usb_devices"]],
                "baud_rate": 9600,
                "auto_detect": True
            }
        }
        
        with open('config/auto_hardware.json', 'w') as f:
            json.dump(config_update, f, indent=2)
        
        print("✅ Auto-configuration saved to config/auto_hardware.json")
        print("\n📋 Next steps:")
        print("   1. Review config/auto_hardware.json")
        print("   2. Update config/termux_config.yaml")
        print("   3. Restart the API: pkill -f government_saas.py && python api/government_saas.py")
    else:
        print("\n⚠️  No hardware detected. Running in simulation mode.")
        print("   Connect hardware via USB and run this script again.")

if __name__ == "__main__":
    print("🤖 Humbu Hardware Detection Tool")
    print("="*40)
    
    print("\nOptions:")
    print("  1. Full hardware scan")
    print("  2. Auto-configure")
    print("  3. Check USB only")
    print("  4. Check network only")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            generate_hardware_report()
        elif choice == "2":
            auto_configure()
        elif choice == "3":
            detect_usb_devices()
        elif choice == "4":
            detect_network_interfaces()
        else:
            print("Invalid option")
            
    except KeyboardInterrupt:
        print("\n👋 Exiting")
