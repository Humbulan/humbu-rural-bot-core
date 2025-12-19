#!/usr/bin/env python3
"""
💰 HUMBU REAL-TIME REVENUE DASHBOARD
Live tracking of your $147,575/month Government SaaS
"""

import requests
import time
import os
import sys
from datetime import datetime
import threading

API_BASE = "http://localhost:8083"
TARGET = 147575.0

class RevenueDashboard:
    def __init__(self):
        self.start_time = time.time()
        self.highest_rate = 0
        self.total_transactions = 0
        self.running = True
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def get_revenue_data(self):
        """Get current revenue data"""
        try:
            response = requests.get(f"{API_BASE}/revenue", timeout=2)
            if response.status_code == 200:
                return response.json()
        except:
            return None
    
    def get_api_status(self):
        """Get API status"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def format_money(self, amount):
        """Format money with commas"""
        return f"${amount:,.2f}"
    
    def calculate_progress_bar(self, percentage, width=50):
        """Create a progress bar"""
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        return bar
    
    def calculate_time_to_target(self, current, rate_per_hour):
        """Calculate time to reach target"""
        if rate_per_hour <= 0:
            return "∞"
        
        remaining = TARGET - current
        hours = remaining / rate_per_hour
        days = hours / 24
        
        if days > 1:
            return f"{days:.1f} days"
        elif hours > 1:
            return f"{hours:.1f} hours"
        else:
            minutes = hours * 60
            return f"{minutes:.1f} minutes"
    
    def display_dashboard(self):
        """Display the main dashboard"""
        while self.running:
            data = self.get_revenue_data()
            if not data:
                print("❌ Cannot connect to API")
                time.sleep(5)
                continue
            
            current = data.get('current_revenue', 0)
            transactions_today = data.get('transactions_today', 0)
            percentage = (current / TARGET) * 100
            
            # Calculate rates
            elapsed = time.time() - self.start_time
            revenue_per_hour = (current / elapsed) * 3600 if elapsed > 0 else 0
            transactions_per_hour = (transactions_today / elapsed) * 3600 if elapsed > 0 else 0
            
            if revenue_per_hour > self.highest_rate:
                self.highest_rate = revenue_per_hour
            
            self.clear_screen()
            
            # Header
            print("="*70)
            print("💰 HUMBU REAL-TIME REVENUE DASHBOARD")
            print(f"   $147,575/month Government SaaS • Live Tracking")
            print("="*70)
            print()
            
            # Main progress
            print("🎯 MONTHLY REVENUE TARGET")
            bar = self.calculate_progress_bar(percentage)
            print(f"[{bar}]")
            print(f"   {self.format_money(current)} / {self.format_money(TARGET)} ({percentage:.4f}%)")
            print()
            
            # Stats grid
            print("📊 LIVE STATISTICS")
            print("-"*40)
            print(f"💰 Revenue/Hour: {self.format_money(revenue_per_hour)}")
            print(f"💸 Transactions/Hour: {transactions_per_hour:,.0f}")
            print(f"📈 Avg Revenue/Transaction: ${0.47:.2f}")
            print(f"⚡ Peak Rate: {self.format_money(self.highest_rate)}/hour")
            print()
            
            # Time projections
            print("⏱️  PROJECTIONS")
            print("-"*40)
            time_to_target = self.calculate_time_to_target(current, revenue_per_hour)
            daily_projection = revenue_per_hour * 24
            monthly_projection = daily_projection * 30
            
            print(f"⏳ Time to target: {time_to_target}")
            print(f"📅 Projected Daily: {self.format_money(daily_projection)}")
            print(f"📈 Projected Monthly: {self.format_money(monthly_projection)}")
            
            if monthly_projection >= TARGET:
                print(f"✅ STATUS: ON TRACK ({monthly_projection/TARGET*100:.1f}% of target)")
            else:
                print(f"⚠️  STATUS: NEEDS BOOST ({monthly_projection/TARGET*100:.1f}% of target)")
            print()
            
            # Recent activity
            print("📝 RECENT ACTIVITY")
            print("-"*40)
            recent = data.get('recent_transactions', [])
            if recent:
                for tx in recent[-5:]:
                    ts = datetime.fromisoformat(tx['timestamp']).strftime('%H:%M:%S')
                    print(f"   [{ts}] ${tx['amount']} - {tx['type']} - {tx['source']}")
            else:
                print("   No recent transactions")
            print()
            
            # System status
            print("🔧 SYSTEM STATUS")
            print("-"*40)
            api_online = self.get_api_status()
            print(f"   API: {'✅ ONLINE' if api_online else '❌ OFFLINE'}")
            print(f"   Uptime: {elapsed/3600:.1f} hours")
            print(f"   Total Transactions: {transactions_today:,}")
            print()
            
            # Controls
            print("🚀 CONTROLS")
            print("-"*40)
            print("   [R] Refresh   [A] Accelerate   [S] Stop   [Q] Quit")
            print()
            
            # Wait for input or auto-refresh
            try:
                # Non-blocking input check
                import select
                if select.select([sys.stdin], [], [], 5)[0]:
                    key = sys.stdin.read(1).lower()
                    if key == 'q':
                        self.running = False
                        print("Exiting dashboard...")
                        break
                    elif key == 'a':
                        self.launch_accelerator()
                    elif key == 's':
                        self.stop_all()
                    elif key == 'r':
                        continue
            except:
                # Auto-refresh every 5 seconds
                time.sleep(5)
    
    def launch_accelerator(self):
        """Launch revenue accelerator"""
        print("\n🚀 Launching Revenue Accelerator...")
        os.system("python scripts/revenue_accelerator.py &")
        print("✅ Accelerator launched in background")
        time.sleep(2)
    
    def stop_all(self):
        """Stop all revenue generation"""
        print("\n🛑 Stopping all processes...")
        os.system("pkill -f 'revenue_rocket.py'")
        os.system("pkill -f 'revenue_accelerator.py'")
        print("✅ Revenue generation stopped")
        time.sleep(2)
    
    def run(self):
        """Run the dashboard"""
        print("💰 Starting Humhu Real-Time Revenue Dashboard...")
        print("   Tracking $147,575/month Government SaaS")
        print("   Press Ctrl+C to exit")
        print()
        
        try:
            self.display_dashboard()
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")
            self.running = False

if __name__ == "__main__":
    dashboard = RevenueDashboard()
    dashboard.run()
