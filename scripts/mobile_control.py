#!/usr/bin/env python3
"""
Humbu Mobile Control - Control your $147k SaaS from your phone
Termux-optimized interface with vibration feedback
"""

import os
import sys
import json
import requests
from datetime import datetime
import time

API_BASE = "http://localhost:8083"

class MobileController:
    def __init__(self):
        self.api_online = False
        self.check_api()
        
    def check_api(self):
        """Check if API is online"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
            self.api_online = response.status_code == 200
            return self.api_online
        except:
            self.api_online = False
            return False
    
    def vibrate(self, pattern="short"):
        """Vibrate phone if Termux API is available"""
        try:
            if pattern == "short":
                os.system("termux-vibrate -d 200")
            elif pattern == "success":
                os.system("termux-vibrate -d 100")
                time.sleep(0.1)
                os.system("termux-vibrate -d 100")
            elif pattern == "alert":
                os.system("termux-vibrate -d 1000")
            elif pattern == "revenue":
                os.system("termux-vibrate -d 500")
                time.sleep(0.2)
                os.system("termux-vibrate -d 300")
            elif pattern == "error":
                os.system("termux-vibrate -d 300")
                time.sleep(0.1)
                os.system("termux-vibrate -d 300")
                time.sleep(0.1)
                os.system("termux-vibrate -d 300")
        except:
            pass  # Not running in Termux or vibration not available
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_header(self):
        """Show application header"""
        self.clear_screen()
        print("="*60)
        print("📱 HUMBU MOBILE CONTROL")
        print("   $147,575/month Government SaaS")
        print("="*60)
        print()
        
        # Show API status
        status = "✅ ONLINE" if self.api_online else "❌ OFFLINE"
        print(f"API Status: {status}")
        
        if self.api_online:
            try:
                revenue = requests.get(f"{API_BASE}/revenue").json()
                current = revenue.get('current_revenue', 0)
                target = revenue.get('monthly_target', 147575)
                percent = (current / target * 100) if target > 0 else 0
                
                print(f"Monthly Revenue: ${current:,.2f} / ${target:,.2f}")
                print(f"Progress: {percent:.1f}%")
                print(f"Transactions Today: {revenue.get('transactions_today', 0)}")
            except:
                print("Could not load revenue data")
        print()
    
    def show_menu(self):
        """Show main menu"""
        self.show_header()
        
        print("MAIN MENU:")
        print("  1. 📊 Dashboard & Revenue Status")
        print("  2. 🚀 Generate Revenue Transactions")
        print("  3. 🔌 Hardware Control")
        print("  4. 📈 Revenue Reports")
        print("  5. ⚙️  System Settings")
        print("  6. 🆘 Emergency Stop")
        print("  7. 🔄 Refresh")
        print("  8. 🚪 Exit")
        print()
    
    def dashboard_view(self):
        """Show detailed dashboard"""
        self.show_header()
        
        try:
            # Get API status
            status = requests.get(f"{API_BASE}/").json()
            revenue = requests.get(f"{API_BASE}/revenue").json()
            health = requests.get(f"{API_BASE}/health").json()
            
            print("📊 SYSTEM DASHBOARD")
            print("-"*40)
            
            # Revenue progress bar
            current = revenue.get('current_revenue', 0)
            target = revenue.get('monthly_target', 147575)
            percent = int((current / target * 100)) if target > 0 else 0
            bar = "█" * (percent // 2) + "░" * (50 - (percent // 2))
            print(f"Monthly Revenue: [ {bar} ]")
            print(f"   ${current:,.2f} / ${target:,.2f} ({percent}%)")
            print()
            
            # System info
            print("🏢 System Information:")
            print(f"   API Status: {status.get('status', 'unknown')}")
            print(f"   Port: {status.get('port', 'unknown')}")
            print(f"   Hardware: {'Connected' if health.get('hardware_connected', False) else 'Simulation'}")
            print(f"   Clients: {', '.join(status.get('clients', []))}")
            print()
            
            # Recent transactions
            print("💸 Recent Activity:")
            transactions = revenue.get('recent_transactions', [])
            if transactions:
                for t in transactions[-5:]:
                    time_str = datetime.fromisoformat(t['timestamp']).strftime('%H:%M')
                    print(f"   {time_str}: ${t['amount']} - {t['type']}")
            else:
                print("   No recent transactions")
            print()
            
        except Exception as e:
            print(f"❌ Error loading dashboard: {e}")
            print()
        
        input("Press Enter to continue...")
    
    def generate_revenue(self):
        """Generate revenue transactions"""
        self.show_header()
        print("🚀 GENERATE REVENUE")
        print("-"*40)
        
        print("Transaction types:")
        print("  1. Delivery Status ($0.47)")
        print("  2. GPS Tracking ($0.25)")
        print("  3. Soil Moisture ($0.15)")
        print("  4. Livestock Health ($0.32)")
        print("  5. Auto-generate 10 transactions")
        print("  6. Continuous generation")
        print()
        
        choice = input("Select (1-6): ").strip()
        
        try:
            if choice == "1":
                self._send_transaction("delivery_status")
            elif choice == "2":
                self._send_transaction("gps_tracking")
            elif choice == "3":
                self._send_transaction("soil_moisture")
            elif choice == "4":
                self._send_transaction("livestock_health")
            elif choice == "5":
                for i in range(10):
                    types = ["delivery_status", "gps_tracking", "soil_moisture", "livestock_health"]
                    import random
                    self._send_transaction(random.choice(types))
                    time.sleep(0.5)
                self.vibrate("revenue")
            elif choice == "6":
                print("\nStarting continuous revenue generation...")
                print("Press Ctrl+C to stop")
                try:
                    count = 0
                    import random
                    while True:
                        types = ["delivery_status", "gps_tracking", "soil_moisture", "livestock_health"]
                        self._send_transaction(random.choice(types))
                        count += 1
                        if count % 10 == 0:
                            print(f"Generated {count} transactions...")
                        time.sleep(random.uniform(1, 3))
                except KeyboardInterrupt:
                    print(f"\nStopped. Generated {count} transactions.")
                    self.vibrate("alert")
            else:
                print("Invalid choice")
                
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def _send_transaction(self, data_type):
        """Send a single transaction"""
        try:
            headers = {"X-API-Key": "GOV-AGRIC-SAAS-2024"}
            data = {
                "type": data_type,
                "source": "mobile_control",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{API_BASE}/api/v1/process_rural_data",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                revenue = result.get('revenue_generated', 0)
                print(f"✅ Generated: ${revenue} ({data_type})")
                self.vibrate("success")
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                self.vibrate("error")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.vibrate("error")
            return False
    
    def emergency_stop(self):
        """Emergency stop all processes"""
        self.show_header()
        print("🛑 EMERGENCY STOP")
        print("-"*40)
        print("This will stop all Humbu processes including:")
        print("  • Government SaaS API")
        print("  • Revenue generation")
        print("  • Watchdog monitor")
        print()
        
        confirm = input("Type 'STOP' to confirm: ")
        if confirm == "STOP":
            print("\nStopping processes...")
            os.system("pkill -f 'government_saas.py'")
            os.system("pkill -f 'api_watchdog.sh'")
            os.system("pkill -f 'revenue_booster.py'")
            time.sleep(2)
            print("✅ All processes stopped.")
            self.vibrate("alert")
        else:
            print("Cancelled.")
        
        time.sleep(2)
    
    def run(self):
        """Main application loop"""
        self.vibrate("short")  # Startup vibration
        
        while True:
            self.check_api()
            self.show_menu()
            
            try:
                choice = input("Select option (1-8): ").strip()
                
                if choice == "1":
                    self.dashboard_view()
                elif choice == "2":
                    self.generate_revenue()
                elif choice == "3":
                    os.system("python scripts/detect_hardware.py")
                    input("\nPress Enter to continue...")
                elif choice == "4":
                    self.show_reports()
                elif choice == "5":
                    self.settings_menu()
                elif choice == "6":
                    self.emergency_stop()
                elif choice == "7":
                    continue  # Just refresh
                elif choice == "8":
                    print("\n👋 Exiting Mobile Control")
                    self.vibrate("short")
                    break
                else:
                    print("Invalid option")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Exiting Mobile Control")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(2)
    
    def show_reports(self):
        """Show revenue reports"""
        self.show_header()
        print("📈 REVENUE REPORTS")
        print("-"*40)
        
        try:
            revenue = requests.get(f"{API_BASE}/revenue").json()
            
            print("Current Status:")
            print(f"  Monthly Target: ${revenue.get('monthly_target', 0):,.2f}")
            print(f"  Current Revenue: ${revenue.get('current_revenue', 0):,.2f}")
            print(f"  Remaining: ${revenue.get('remaining_target', 0):,.2f}")
            print(f"  Daily Average Needed: ${revenue.get('daily_average_needed', 0):,.2f}")
            print(f"  Transactions Today: {revenue.get('transactions_today', 0)}")
            print()
            
            # Calculate projections
            current = revenue.get('current_revenue', 0)
            daily_avg = revenue.get('daily_average_needed', 4919.17)
            days_in_month = 30
            today = datetime.now().day
            remaining_days = days_in_month - today
            
            if remaining_days > 0:
                required_daily = (147575 - current) / remaining_days
                print("📊 Projections:")
                print(f"  Days remaining: {remaining_days}")
                print(f"  Required daily: ${required_daily:,.2f}")
                
                if required_daily <= daily_avg:
                    print("  Status: ✅ On track to meet target")
                else:
                    print(f"  Status: ⚠️  Need {((required_daily/daily_avg)-1)*100:.1f}% more daily")
            
        except Exception as e:
            print(f"Error loading reports: {e}")
        
        print()
        input("Press Enter to continue...")
    
    def settings_menu(self):
        """System settings menu"""
        self.show_header()
        print("⚙️  SYSTEM SETTINGS")
        print("-"*40)
        
        print("  1. Restart API")
        print("  2. Start Watchdog")
        print("  3. View Logs")
        print("  4. Backup Revenue Data")
        print("  5. Hardware Configuration")
        print()
        
        choice = input("Select (1-5): ").strip()
        
        if choice == "1":
            print("\nRestarting API...")
            os.system("pkill -f 'government_saas.py'")
            time.sleep(2)
            os.system("python api/government_saas.py > data/logs/api_restart.log 2>&1 &")
            print("✅ API restarted")
            self.vibrate("success")
        elif choice == "2":
            print("\nStarting Watchdog...")
            os.system("./monitoring/api_watchdog.sh > data/logs/watchdog_start.log 2>&1 &")
            print("✅ Watchdog started")
            self.vibrate("success")
        elif choice == "3":
            print("\nRecent logs:")
            try:
                os.system("tail -20 data/logs/watchdog.log")
            except:
                print("No logs found")
        elif choice == "4":
            print("\nBacking up revenue data...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.system(f"cp data/revenue_database.json data/backups/revenue_backup_{timestamp}.json")
            os.system(f"cp data/transactions.csv data/backups/transactions_backup_{timestamp}.csv")
            print("✅ Backup completed")
            self.vibrate("success")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    controller = MobileController()
    controller.run()
