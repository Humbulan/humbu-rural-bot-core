#!/usr/bin/env python3
"""
🚀 HUMBU SUPER LAUNCHER
Python-based full-scale revenue generation
No external dependencies needed
"""

import requests
import time
import sys
import os
from datetime import datetime

API_BASE = "http://localhost:8083"
TARGET_REVENUE = 147575.0

def get_current_revenue():
    """Get current revenue status"""
    try:
        response = requests.get(f"{API_BASE}/revenue", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        return None

def calculate_targets():
    """Calculate remaining targets"""
    data = get_current_revenue()
    if not data:
        return None
    
    current = data.get('current_revenue', 0)
    remaining = TARGET_REVENUE - current
    
    # Days remaining in month (assuming we start from today)
    today = datetime.now().day
    days_in_month = 30
    days_remaining = days_in_month - today + 1
    
    daily_needed = remaining / days_remaining if days_remaining > 0 else remaining
    tx_needed = daily_needed / 0.47  # $0.47 per transaction
    
    return {
        'current': current,
        'remaining': remaining,
        'days_remaining': days_remaining,
        'daily_needed': daily_needed,
        'tx_needed': tx_needed,
        'tx_today': data.get('transactions_today', 0)
    }

def print_banner():
    """Print launch banner"""
    print("="*70)
    print("🚀 HUMBU SUPER LAUNCHER v2.0")
    print("💰 Target: $147,575/month Government SaaS")
    print("="*70)
    print()

def print_status():
    """Print current status"""
    targets = calculate_targets()
    if not targets:
        print("❌ Could not connect to API")
        return
    
    print("📊 CURRENT STATUS")
    print("-"*40)
    print(f"💰 Revenue Generated: ${targets['current']:,.2f}")
    print(f"🎯 Monthly Target: ${TARGET_REVENUE:,.2f}")
    print(f"📈 Progress: {(targets['current']/TARGET_REVENUE)*100:.2f}%")
    print(f"📅 Days Remaining: {targets['days_remaining']}")
    print(f"📊 Transactions Today: {targets['tx_today']:,}")
    print()
    
    if targets['remaining'] > 0:
        print("🎯 REMAINING TARGETS")
        print("-"*40)
        print(f"💰 Revenue Needed: ${targets['remaining']:,.2f}")
        print(f"📅 Daily Needed: ${targets['daily_needed']:,.2f}")
        print(f"💸 Transactions Needed Today: {targets['tx_needed']:,.0f}")
    else:
        print("🎉 TARGET ALREADY ACHIEVED! 🎉")
    print()

def launch_full_power():
    """Launch full power continuous generation"""
    print("🚀 LAUNCHING FULL POWER MODE")
    print("-"*40)
    
    targets = calculate_targets()
    if not targets:
        return
    
    # Calculate optimal rate
    hours_remaining = targets['days_remaining'] * 24
    if hours_remaining > 0:
        revenue_per_hour = targets['remaining'] / hours_remaining
        tx_per_hour = revenue_per_hour / 0.47
        tx_per_minute = tx_per_hour / 60
        
        # Limit to reasonable rates
        tx_per_minute = min(max(tx_per_minute, 10), 200)
        
        print(f"📈 Calculated optimal rate:")
        print(f"   Hours remaining: {hours_remaining:,.1f}")
        print(f"   Revenue/hour needed: ${revenue_per_hour:,.2f}")
        print(f"   Transactions/minute: {tx_per_minute:,.1f}")
        print(f"   Expected revenue/hour: ${tx_per_minute * 60 * 0.47:,.2f}")
    else:
        tx_per_minute = 100  # Default
    
    print()
    print("⚡ LAUNCH CONFIGURATION")
    print("-"*40)
    print(f"Mode: Continuous Rocket")
    print(f"Rate: {tx_per_minute:.0f} transactions/minute")
    print(f"Revenue rate: ${tx_per_minute * 60 * 0.47:,.2f}/hour")
    print(f"Projected completion: {targets['remaining']/(tx_per_minute * 60 * 0.47):.1f} hours")
    print()
    
    confirm = input("Launch? (yes/no): ").lower().strip()
    if confirm != 'yes':
        print("Launch cancelled")
        return
    
    print()
    print("🚀 IGNITION SEQUENCE INITIATED...")
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("LAUNCH! 🚀")
    print()
    print("💰 Revenue generation started!")
    print("Press Ctrl+C to stop")
    print()
    
    # Launch revenue rocket
    os.system(f"python scripts/revenue_rocket.py 3 {int(tx_per_minute)} &")
    
    # Monitor progress
    try:
        start_time = time.time()
        last_revenue = targets['current']
        
        while True:
            time.sleep(30)
            current_data = get_current_revenue()
            if current_data:
                current = current_data.get('current_revenue', 0)
                elapsed = time.time() - start_time
                revenue_generated = current - last_revenue
                revenue_per_hour = (revenue_generated / elapsed) * 3600 if elapsed > 0 else 0
                
                print(f"⏱️  Elapsed: {elapsed/60:.1f} min | "
                      f"💰 Total: ${current:,.2f} | "
                      f"📈 Rate: ${revenue_per_hour:,.2f}/hour | "
                      f"🎯 Progress: {(current/TARGET_REVENUE)*100:.2f}%")
                
                if current >= TARGET_REVENUE:
                    print()
                    print("🎉 🎉 🎉 TARGET ACHIEVED! 🎉 🎉 🎉")
                    print(f"💰 Final Revenue: ${current:,.2f}")
                    print("✅ Monthly target of $147,575 reached!")
                    print("🚀 Mission accomplished!")
                    break
                    
    except KeyboardInterrupt:
        print()
        print("🛑 Launch stopped by user")
    
    # Final report
    final_data = get_current_revenue()
    if final_data:
        final = final_data.get('current_revenue', 0)
        print()
        print("📊 FINAL REPORT")
        print("-"*40)
        print(f"💰 Revenue Generated: ${final:,.2f}")
        print(f"🎯 Target: ${TARGET_REVENUE:,.2f}")
        print(f"📈 Achievement: {(final/TARGET_REVENUE)*100:.2f}%")
        print(f"📊 Transactions Today: {final_data.get('transactions_today', 0):,}")

def launch_burst_mode():
    """Launch burst mode"""
    print("💥 LAUNCHING BURST MODE")
    print("-"*40)
    
    targets = calculate_targets()
    if not targets:
        return
    
    tx_needed = int(targets['tx_needed'])
    print(f"Transactions needed: {tx_needed:,}")
    print(f"Expected revenue: ${tx_needed * 0.47:,.2f}")
    print()
    
    # Split into batches
    batch_size = 100
    batches = (tx_needed + batch_size - 1) // batch_size
    
    print(f"Execution plan:")
    print(f"   Batch size: {batch_size}")
    print(f"   Batches: {batches}")
    print(f"   Estimated time: {batches * 5} seconds")
    print()
    
    confirm = input("Execute burst? (yes/no): ").lower().strip()
    if confirm != 'yes':
        print("Burst cancelled")
        return
    
    print()
    print("💥 EXECUTING BURST SEQUENCE...")
    
    start_time = time.time()
    for i in range(batches):
        print(f"Batch {i+1}/{batches}...")
        os.system(f"python scripts/revenue_rocket.py 1 {batch_size} > /dev/null 2>&1")
        
        # Update progress
        current_data = get_current_revenue()
        if current_data:
            current = current_data.get('current_revenue', 0)
            progress = (current / TARGET_REVENUE) * 100
            print(f"   Progress: ${current:,.2f} ({progress:.2f}%)")
    
    elapsed = time.time() - start_time
    print()
    print(f"✅ Burst complete in {elapsed:.1f} seconds")
    
    # Final status
    final_data = get_current_revenue()
    if final_data:
        final = final_data.get('current_revenue', 0)
        print(f"💰 New Total: ${final:,.2f}")
        print(f"📈 New Progress: {(final/TARGET_REVENUE)*100:.2f}%")

def launch_mobile_control():
    """Launch mobile control"""
    print("📱 LAUNCHING MOBILE CONTROL...")
    os.system("python scripts/mobile_control.py")

def emergency_stop():
    """Emergency stop all processes"""
    print("🛑 EMERGENCY STOP PROTOCOL")
    print("-"*40)
    print("This will stop:")
    print("  • Revenue Rocket")
    print("  • Government SaaS API")
    print("  • Watchdog")
    print("  • All revenue generation")
    print()
    
    confirm = input("Type 'STOP' to confirm: ")
    if confirm == 'STOP':
        print("Stopping all processes...")
        os.system("pkill -f 'revenue_rocket.py'")
        os.system("pkill -f 'government_saas.py'")
        os.system("pkill -f 'api_watchdog.sh'")
        time.sleep(2)
        print("✅ All processes stopped")
    else:
        print("Cancelled")

def main():
    """Main function"""
    print_banner()
    print_status()
    
    print("🚀 LAUNCH OPTIONS")
    print("="*40)
    print("1. 🚀 FULL POWER - Continuous to target")
    print("2. 💥 BURST MODE - Generate needed transactions")
    print("3. 📱 MOBILE CONTROL - Manual interface")
    print("4. 🏛️  GOVERNMENT SURGE - High-volume test")
    print("5. 📊 STATUS REPORT - Detailed analysis")
    print("6. 🛑 EMERGENCY STOP - Stop everything")
    print("7. 🚪 EXIT")
    print()
    
    try:
        choice = input("Select option (1-7): ").strip()
        
        if choice == "1":
            launch_full_power()
        elif choice == "2":
            launch_burst_mode()
        elif choice == "3":
            launch_mobile_control()
        elif choice == "4":
            os.system("python scripts/revenue_rocket.py 4")
        elif choice == "5":
            print_detailed_report()
        elif choice == "6":
            emergency_stop()
        elif choice == "7":
            print("👋 Exiting Super Launcher")
        else:
            print("Invalid option")
            
    except KeyboardInterrupt:
        print("\n👋 Exiting Super Launcher")

def print_detailed_report():
    """Print detailed revenue report"""
    targets = calculate_targets()
    if not targets:
        return
    
    print()
    print("📊 DETAILED REVENUE REPORT")
    print("="*60)
    print(f"💰 Current Revenue: ${targets['current']:,.2f}")
    print(f"🎯 Monthly Target: ${TARGET_REVENUE:,.2f}")
    print(f"📈 Progress: {(targets['current']/TARGET_REVENUE)*100:.2f}%")
    print()
    
    if targets['remaining'] > 0:
        print("🎯 REMAINING ANALYSIS")
        print("-"*40)
        print(f"📅 Days Remaining: {targets['days_remaining']}")
        print(f"💰 Revenue Needed: ${targets['remaining']:,.2f}")
        print(f"📊 Daily Target: ${targets['daily_needed']:,.2f}")
        print(f"💸 Transactions/Day: {targets['tx_needed']:,.0f}")
        print()
        
        # Calculate rates needed
        hours_per_day = 24
        tx_per_hour = targets['tx_needed'] / hours_per_day
        tx_per_minute = tx_per_hour / 60
        
        print("⚡ REQUIRED PERFORMANCE")
        print("-"*40)
        print(f"Transactions/Hour: {tx_per_hour:,.1f}")
        print(f"Transactions/Minute: {tx_per_minute:,.1f}")
        print(f"Revenue/Hour: ${tx_per_hour * 0.47:,.2f}")
        print()
        
        # Current performance
        current_data = get_current_revenue()
        if current_data and 'recent_transactions' in current_data:
            recent_tx = len(current_data['recent_transactions'])
            if recent_tx > 0:
                print("📈 CURRENT PERFORMANCE")
                print("-"*40)
                # Estimate from recent transactions
                print(f"Recent transactions: {recent_tx}")
                print("(Note: Run continuous mode for accurate performance measurement)")
    
    print()
    print("🚀 RECOMMENDED ACTION:")
    if targets['remaining'] > 0:
        if targets['days_remaining'] < 3:
            print("   ⚠️  URGENT: Launch FULL POWER mode immediately!")
        else:
            print("   ✅ Launch FULL POWER mode to reach target comfortably")
    else:
        print("   🎉 TARGET ACHIEVED! Consider higher targets")

if __name__ == "__main__":
    main()
