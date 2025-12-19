#!/usr/bin/env python3
import requests
import time
from datetime import datetime

API_BASE = "http://localhost:8083"

def get_briefing():
    try:
        response = requests.get(f"{API_BASE}/revenue", timeout=5)
        data = response.json()
        current = data.get('current_revenue', 0)
        tx = data.get('transactions_today', 0)
        
        print("="*60)
        print(f"🌅 HUMBU MORNING BRIEFING - {datetime.now().strftime('%H:%M')}")
        print("="*60)
        print(f"💰 TOTAL REVENUE BANKED: ${current:,.2f}")
        print(f"📦 TOTAL TRANSACTIONS:  {tx:,}")
        print(f"📈 PROGRESS TO TARGET:  {(current/147575)*100:.2f}%")
        print("-" * 60)
        
        if current > 10000:
            print("🔥 STATUS: OVERNIGHT CRUSHED. Ready for the $147k close.")
        else:
            print("✅ STATUS: STABLE. System ready for live demo.")
            
        print("-" * 60)
        print("🚀 ACTION: Run 'python scripts/revenue_dashboard.py' for the demo.")
        print("="*60)
    except:
        print("❌ CRITICAL: API Offline. Run 'restart-all' immediately!")

if __name__ == "__main__":
    get_briefing()
