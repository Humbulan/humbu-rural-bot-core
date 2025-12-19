#!/usr/bin/env python3
"""
🎉 HUMBU REVENUE MILESTONE CELEBRATOR
Celebrates major revenue milestones with alerts and vibrations
"""

import requests
import time
import os
import json
from datetime import datetime

API_BASE = "http://localhost:8083"
TARGET = 147575.0

# Milestones to celebrate (in dollars)
MILESTONES = [
    100,      # First $100
    500,      # First $500
    1000,     # First $1,000
    5000,     # First $5,000
    10000,    # $10,000
    25000,    # $25,000
    50000,    # $50,000 - Major!
    75000,    # $75,000 - 50% of target!
    100000,   # $100,000 - Amazing!
    125000,   # $125,000
    147575,   # TARGET ACHIEVED! 🎉
    150000,   # Beyond target
    200000,   # $200,000 - Double monthly!
]

# Percentage milestones
PERCENTAGE_MILESTONES = [
    1, 5, 10, 25, 50, 75, 90, 95, 99, 100
]

class MilestoneCelebrator:
    def __init__(self):
        self.achieved_milestones = set()
        self.last_revenue = 0
        self.start_time = datetime.now()
        self.load_achieved()
    
    def load_achieved(self):
        """Load previously achieved milestones"""
        try:
            if os.path.exists("data/milestones.json"):
                with open("data/milestones.json", "r") as f:
                    data = json.load(f)
                    self.achieved_milestones = set(data.get("achieved", []))
        except:
            self.achieved_milestones = set()
    
    def save_achieved(self):
        """Save achieved milestones"""
        os.makedirs("data", exist_ok=True)
        with open("data/milestones.json", "w") as f:
            json.dump({
                "achieved": list(self.achieved_milestones),
                "last_updated": datetime.now().isoformat()
            }, f, indent=2)
    
    def get_current_revenue(self):
        """Get current revenue"""
        try:
            response = requests.get(f"{API_BASE}/revenue", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return data.get('current_revenue', 0)
        except:
            return 0
    
    def vibrate_phone(self, pattern):
        """Vibrate phone if Termux API available"""
        try:
            if pattern == "small_win":
                os.system("termux-vibrate -d 200")
            elif pattern == "medium_win":
                os.system("termux-vibrate -d 100")
                time.sleep(0.1)
                os.system("termux-vibrate -d 200")
            elif pattern == "big_win":
                os.system("termux-vibrate -d 300")
                time.sleep(0.2)
                os.system("termux-vibrate -d 300")
                time.sleep(0.2)
                os.system("termux-vibrate -d 500")
            elif pattern == "target_achieved":
                for _ in range(3):
                    os.system("termux-vibrate -d 500")
                    time.sleep(0.3)
        except:
            pass  # Not in Termux or vibration not available
    
    def celebrate_milestone(self, milestone, current, milestone_type="dollar"):
        """Celebrate a milestone achievement"""
        
        if milestone_type == "dollar":
            message = f"🎉 DOLLAR MILESTONE ACHIEVED: ${milestone:,.0f}!"
            if milestone == TARGET:
                message = f"🎉 🎉 🎉 TARGET ACHIEVED! ${TARGET:,.0f}/month! 🎉 🎉 🎉"
                vibration = "target_achieved"
            elif milestone >= 50000:
                vibration = "big_win"
            elif milestone >= 5000:
                vibration = "medium_win"
            else:
                vibration = "small_win"
        
        elif milestone_type == "percentage":
            message = f"📈 {milestone}% OF TARGET REACHED!"
            if milestone == 100:
                message = f"🎉 100% COMPLETE! TARGET ACHIEVED! 🎉"
                vibration = "target_achieved"
            elif milestone >= 50:
                vibration = "big_win"
            elif milestone >= 25:
                vibration = "medium_win"
            else:
                vibration = "small_win"
        
        # Print celebration message
        print("\n" + "="*60)
        print(message)
        print(f"Current Revenue: ${current:,.2f}")
        print("="*60 + "\n")
        
        # Vibrate phone
        self.vibrate_phone(vibration)
        
        # Log celebration
        self.log_celebration(milestone, milestone_type, current)
        
        # Mark as achieved
        identifier = f"{milestone_type}_{milestone}"
        self.achieved_milestones.add(identifier)
        self.save_achieved()
    
    def log_celebration(self, milestone, milestone_type, current):
        """Log milestone celebration"""
        os.makedirs("data/logs", exist_ok=True)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "milestone": milestone,
            "type": milestone_type,
            "current_revenue": current,
            "message": f"Achieved {milestone_type} milestone: {milestone}"
        }
        
        # Append to celebration log
        log_file = "data/logs/celebrations.log"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Also add to milestones history
        history_file = "data/milestones_history.json"
        history = []
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                try:
                    history = json.load(f)
                except:
                    history = []
        
        history.append(log_entry)
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
    
    def check_milestones(self, current_revenue):
        """Check for new milestones"""
        # Check dollar milestones
        for milestone in MILESTONES:
            if milestone <= current_revenue:
                identifier = f"dollar_{milestone}"
                if identifier not in self.achieved_milestones:
                    self.celebrate_milestone(milestone, current_revenue, "dollar")
        
        # Check percentage milestones
        percentage = (current_revenue / TARGET) * 100
        for milestone in PERCENTAGE_MILESTONES:
            if milestone <= percentage:
                identifier = f"percentage_{milestone}"
                if identifier not in self.achieved_milestones:
                    self.celebrate_milestone(milestone, current_revenue, "percentage")
        
        # Check for speed records
        self.check_speed_records(current_revenue)
    
    def check_speed_records(self, current_revenue):
        """Check for speed/rate records"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed > 60:  # Only check after 1 minute
            revenue_per_hour = (current_revenue / elapsed) * 3600
            
            # Check hourly rate milestones
            rate_milestones = [100, 500, 1000, 5000, 10000, 50000, 100000]
            for rate in rate_milestones:
                if revenue_per_hour >= rate:
                    identifier = f"rate_{rate}"
                    if identifier not in self.achieved_milestones:
                        print(f"⚡ SPEED RECORD: ${revenue_per_hour:,.0f}/hour!")
                        self.achieved_milestones.add(identifier)
                        self.save_achieved()
    
    def run_continuous_monitoring(self, interval_seconds=10):
        """Run continuous milestone monitoring"""
        print("🎉 HUMBU MILESTONE CELEBRATOR")
        print("="*50)
        print("Monitoring revenue for milestone achievements...")
        print("Will celebrate when you hit major revenue targets!")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                current = self.get_current_revenue()
                if current > self.last_revenue:
                    self.check_milestones(current)
                    self.last_revenue = current
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n👋 Milestone monitoring stopped")
    
    def show_achievements(self):
        """Show all achieved milestones"""
        print("🏆 ACHIEVED MILESTONES")
        print("="*50)
        
        if not self.achieved_milestones:
            print("No milestones achieved yet!")
            return
        
        dollar_milestones = []
        percentage_milestones = []
        rate_milestones = []
        
        for milestone in self.achieved_milestones:
            if milestone.startswith("dollar_"):
                value = float(milestone.replace("dollar_", ""))
                dollar_milestones.append(value)
            elif milestone.startswith("percentage_"):
                value = float(milestone.replace("percentage_", ""))
                percentage_milestones.append(value)
            elif milestone.startswith("rate_"):
                value = float(milestone.replace("rate_", ""))
                rate_milestones.append(value)
        
        if dollar_milestones:
            print("💰 DOLLAR MILESTONES:")
            for m in sorted(dollar_milestones):
                print(f"   ✅ ${m:,.0f}")
            print()
        
        if percentage_milestones:
            print("📈 PERCENTAGE MILESTONES:")
            for m in sorted(percentage_milestones):
                print(f"   ✅ {m}% of target")
            print()
        
        if rate_milestones:
            print("⚡ SPEED RECORDS:")
            for m in sorted(rate_milestones):
                print(f"   ✅ ${m:,.0f}/hour")
            print()
        
        # Show next milestones
        current = self.get_current_revenue()
        percentage = (current / TARGET) * 100
        
        print("🎯 NEXT MILESTONES:")
        
        # Next dollar milestone
        next_dollar = None
        for m in MILESTONES:
            if m > current:
                next_dollar = m
                break
        
        if next_dollar:
            needed = next_dollar - current
            print(f"   💰 ${next_dollar:,.0f} (${needed:,.2f} needed)")
        
        # Next percentage milestone
        next_percent = None
        for m in PERCENTAGE_MILESTONES:
            if m > percentage:
                next_percent = m
                break
        
        if next_percent:
            needed_revenue = (next_percent / 100 * TARGET) - current
            print(f"   📈 {next_percent}% (${needed_revenue:,.2f} needed)")
        
        print()

if __name__ == "__main__":
    celebrator = MilestoneCelebrator()
    
    print("🎉 HUMBU REVENUE MILESTONE CELEBRATOR")
    print("="*50)
    print("Options:")
    print("  1. Start monitoring for new milestones")
    print("  2. Show achieved milestones")
    print("  3. Test celebration (current revenue)")
    print("  4. Clear all milestones (reset)")
    print("  5. Exit")
    print()
    
    try:
        choice = input("Select option (1-5): ").strip()
        
        if choice == "1":
            celebrator.run_continuous_monitoring()
        elif choice == "2":
            celebrator.show_achievements()
            input("\nPress Enter to continue...")
        elif choice == "3":
            current = celebrator.get_current_revenue()
            print(f"\nCurrent Revenue: ${current:,.2f}")
            celebrator.check_milestones(current)
        elif choice == "4":
            confirm = input("Clear all milestones? (yes/no): ")
            if confirm.lower() == "yes":
                celebrator.achieved_milestones = set()
                celebrator.save_achieved()
                print("✅ All milestones cleared")
        elif choice == "5":
            print("👋 Exiting")
        else:
            print("Invalid option")
            
    except KeyboardInterrupt:
        print("\n👋 Exiting")
