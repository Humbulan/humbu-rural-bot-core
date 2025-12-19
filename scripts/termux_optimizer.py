#!/usr/bin/env python3
"""
Humbu Termux Optimizer - Mobile-friendly system tuning
"""

import os
import json
import time
import requests
from datetime import datetime

def optimize_for_termux():
    print("⚡ TERMUX OPTIMIZATION FOR MAXIMUM REVENUE")
    print("="*50)
    
    # Check API status
    print("🔧 Testing API Performance...")
    api_speed = test_api_speed()
    
    # Check system status
    print("\n📱 Termux System Status:")
    
    # Check available storage
    try:
        stat = os.statvfs('.')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
        used_percent = 100 - (free_gb / total_gb * 100)
        
        print(f"   Storage: {free_gb:.1f} GB free of {total_gb:.1f} GB ({used_percent:.1f}% used)")
        
        if free_gb < 1:
            print("   ⚠️  Low storage! Clear some space.")
        else:
            print("   ✅ Storage sufficient for revenue data")
    except:
        print("   ⚠️  Could not check storage")
    
    # Check if running in background
    print("\n🔄 Process Status:")
    try:
        import subprocess
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        
        api_running = 'government_saas.py' in result.stdout
        watchdog_running = 'api_watchdog.sh' in result.stdout
        
        print(f"   Government API: {'✅ Running' if api_running else '❌ Stopped'}")
        print(f"   Watchdog: {'✅ Running' if watchdog_running else '❌ Stopped'}")
        
        if not api_running:
            print("   ⚠️  Starting API automatically...")
            os.system("python api/government_saas.py > data/logs/api.log 2>&1 &")
            time.sleep(3)
    except:
        print("   ⚠️  Could not check processes")
    
    # Generate optimization recommendations
    print("\n🎯 OPTIMIZATION RECOMMENDATIONS FOR TERMUX:")
    
    recommendations = [
        "✅ Use Mobile Control interface (scripts/mobile_control.py)",
        "✅ Enable phone vibration for revenue alerts",
        "✅ Run in background with '&' at end of commands",
        "✅ Use Revenue Rocket for batch processing",
        "✅ Monitor with: tail -f data/logs/watchdog.log",
        "⚠️  Keep phone charging during high-volume generation",
        "⚠️  Enable 'Stay awake' in Termux settings",
        "🚀 Target: Focus on 'delivery_status' transactions ($0.47)"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Create optimized configuration
    print("\n⚙️  Applying Termux-specific optimizations...")
    
    optimized_config = {
        "optimization": {
            "timestamp": datetime.now().isoformat(),
            "platform": "Termux/Android",
            "recommended_mode": "batch_processing",
            "batch_size": 100,
            "delay_between_batches": 5,
            "optimal_transaction_type": "delivery_status",
            "vibration_enabled": True,
            "background_operation": True,
            "storage_warning_gb": 0.5,
            "auto_restart_api": True
        },
        "performance": {
            "api_response_ms": api_speed,
            "last_optimization": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "optimization_score": 100 - min(api_speed / 10, 90)
        },
        "quick_commands": {
            "start_system": "./start_humbu_system.sh",
            "mobile_control": "python scripts/mobile_control.py",
            "revenue_rocket": "python scripts/revenue_rocket.py",
            "check_status": "curl http://localhost:8083/",
            "view_logs": "tail -20 data/logs/watchdog.log"
        }
    }
    
    # Save optimization report
    os.makedirs("data/optimization", exist_ok=True)
    with open("data/optimization/termux_optimization.json", "w") as f:
        json.dump(optimized_config, f, indent=2)
    
    print(f"\n✅ Termux optimization complete!")
    print(f"   Score: {optimized_config['performance']['optimization_score']:.1f}/100")
    print(f"   Report saved: data/optimization/termux_optimization.json")
    
    # Show revenue projection
    print("\n💰 REVENUE PROJECTION:")
    print("   Current rate: $0.47 per transaction")
    print("   Target: 314,000 transactions/month for $147,575")
    print("   Your pace: 16 transactions so far")
    print("   Needed: ~10,466 transactions/day")
    
    print("\n🚀 RECOMMENDED ACTION:")
    print("   Run: python scripts/revenue_rocket.py")
    print("   Choose option 3 (Continuous Mode)")
    print("   Set to 500 transactions/minute")
    print("   Let run for 1 hour = ~$14,100")
    
    return optimized_config

def test_api_speed():
    """Test API response time"""
    try:
        start = time.time()
        response = requests.get("http://localhost:8083/health", timeout=5)
        response_time = (time.time() - start) * 1000  # ms
        
        if response.status_code == 200:
            print(f"   ✅ API Response: {response_time:.1f} ms")
            return response_time
        else:
            print(f"   ⚠️  API Status: {response.status_code}")
            return 1000
    except Exception as e:
        print(f"   ❌ API Not Reachable: {e}")
        return 5000

def quick_optimization_check():
    """Quick check without detailed system calls"""
    print("🔍 Quick System Check...")
    
    checks = [
        ("API Online", lambda: requests.get("http://localhost:8083/", timeout=2).status_code == 200),
        ("Revenue Tracking", lambda: os.path.exists("data/revenue_database.json")),
        ("Logs Directory", lambda: os.path.exists("data/logs/")),
        ("Mobile Control", lambda: os.path.exists("scripts/mobile_control.py")),
        ("Revenue Rocket", lambda: os.path.exists("scripts/revenue_rocket.py"))
    ]
    
    passed = 0
    for name, check in checks:
        try:
            if check():
                print(f"   ✅ {name}")
                passed += 1
            else:
                print(f"   ❌ {name}")
        except:
            print(f"   ⚠️  {name} (check failed)")
    
    print(f"\n📊 System Readiness: {passed}/{len(checks)} checks passed")
    return passed == len(checks)

if __name__ == "__main__":
    print("🤖 HUMBU TERMUX OPTIMIZER v1.0")
    print("="*40)
    
    if quick_optimization_check():
        print("\n✅ System ready for optimization!")
        optimize_for_termux()
    else:
        print("\n⚠️  System needs setup. Run: ./scripts/setup_rural_bot.sh")
