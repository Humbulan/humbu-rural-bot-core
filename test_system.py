#!/usr/bin/env python3
"""
Test the complete Humbu Rural Bot System
"""

import requests
import time
import sys

API_BASE = "http://localhost:8083"

def test_api_connection():
    print("🔗 Testing API connection...")
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Online: {data.get('service', 'Unknown')}")
            print(f"   Port: {data.get('port', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ API returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Connection Failed: {e}")
        return False

def test_revenue_endpoint():
    print("\n💰 Testing revenue endpoint...")
    try:
        response = requests.get(f"{API_BASE}/revenue", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Revenue Tracking Active")
            print(f"   Monthly Target: ${data.get('monthly_target', 0):,.2f}")
            print(f"   Current Revenue: ${data.get('current_revenue', 0):,.2f}")
            print(f"   Transactions Today: {data.get('transactions_today', 0)}")
            return True
        else:
            print(f"❌ Revenue endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Revenue test failed: {e}")
        return False

def test_hardware_endpoint():
    print("\n🔌 Testing hardware endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/v1/hardware/read", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('data', {}).get('simulated'):
                print("✅ Hardware Simulation Active")
                print(f"   Generated: {data['data']['type']}")
                print(f"   Revenue: ${data.get('revenue', 0)}")
            else:
                print("✅ Real Hardware Detected!")
            return True
        else:
            print(f"❌ Hardware endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Hardware test failed: {e}")
        return False

def test_transaction_processing():
    print("\n💸 Testing transaction processing...")
    try:
        headers = {"X-API-Key": "GOV-AGRIC-SAAS-2024"}
        data = {
            "type": "delivery_status",
            "source": "system_test",
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        response = requests.post(
            f"{API_BASE}/api/v1/process_rural_data",
            json=data,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transaction Processing Active")
            print(f"   Revenue Generated: ${result.get('revenue_generated', 0)}")
            print(f"   Government ID: {result.get('government_reference', 'N/A')}")
            return True
        else:
            print(f"❌ Transaction processing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Transaction test failed: {e}")
        return False

def run_full_test():
    print("="*60)
    print("🤖 HUMBU RURAL BOT SYSTEM TEST")
    print("   $147,575/month Government SaaS")
    print("="*60)
    
    tests = [
        ("API Connection", test_api_connection),
        ("Revenue Tracking", test_revenue_endpoint),
        ("Hardware Interface", test_hardware_endpoint),
        ("Transaction Processing", test_transaction_processing)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            failed += 1
        
        time.sleep(1)
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed))*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready for production.")
        print("   Revenue generation can begin immediately.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check system configuration.")
    
    print("\n🚀 Quick Start Commands:")
    print("   ./scripts/mobile_control.py  # Mobile interface")
    print("   python scripts/revenue_booster.py  # Auto-revenue")
    print("   curl http://localhost:8083/  # Check API")
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1)
