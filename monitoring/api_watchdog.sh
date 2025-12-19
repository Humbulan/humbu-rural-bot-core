#!/bin/bash
# Humbu AI - Revenue Protection Watchdog
# Monitoring the $147,575/month Government SaaS

API_URL="http://localhost:8083/health"
LOG_FILE="data/logs/watchdog.log"
ERROR_LOG="data/logs/errors.log"
REVENUE_LOG="data/logs/revenue_tracking.log"

# Create log directory if it doesn't exist
mkdir -p data/logs

echo "$(date): 🚀 Starting Humbu Revenue Protection Watchdog" >> $LOG_FILE
echo "$(date): 📈 Monthly Target: $147,575" >> $LOG_FILE

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Check API health
    RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/api_response.json $API_URL)
    HTTP_CODE=${RESPONSE: -3}
    
    if [ $HTTP_CODE -eq 200 ]; then
        # API is healthy, check revenue
        REVENUE_DATA=$(curl -s http://localhost:8083/revenue)
        CURRENT_REV=$(echo $REVENUE_DATA | grep -o '"current_revenue":[0-9]*\.\?[0-9]*' | cut -d: -f2)
        
        echo "$TIMESTAMP: ✅ API Online | Revenue: \$${CURRENT_REV}" >> $LOG_FILE
        
        # Log revenue progress every hour
        if [ $(date +%M) == "00" ]; then
            echo "$TIMESTAMP: 💰 Hourly Revenue Check: \$${CURRENT_REV}" >> $REVENUE_LOG
        fi
        
    else
        # API is down - EMERGENCY PROTOCOL
        echo "$TIMESTAMP: 🚨 CRITICAL - API DOWN (Status: $HTTP_CODE)" >> $LOG_FILE
        echo "$TIMESTAMP: 🚨 CRITICAL - API DOWN (Status: $HTTP_CODE)" >> $ERROR_LOG
        
        # Try to restart the API
        echo "$TIMESTAMP: 🔄 Attempting API restart..." >> $LOG_FILE
        
        # Kill existing processes
        pkill -f "government_saas.py"
        sleep 2
        
        # Restart API
        cd /data/data/com.termux/files/home/humbu-rural-bot-core
        nohup python api/government_saas.py > data/logs/api_restart.log 2>&1 &
        
        # Wait and verify restart
        sleep 10
        RESTART_CHECK=$(curl -s -o /dev/null -w "%{http_code}" $API_URL)
        
        if [ $RESTART_CHECK -eq 200 ]; then
            echo "$TIMESTAMP: ✅ API successfully restarted" >> $LOG_FILE
            # Notify via vibration if on Termux
            if command -v termux-vibrate &> /dev/null; then
                termux-vibrate -d 1000
            fi
        else
            echo "$TIMESTAMP: ❌ API restart FAILED" >> $ERROR_LOG
            echo "$TIMESTAMP: ❌ API restart FAILED" >> $LOG_FILE
            # Emergency vibration pattern
            if command -v termux-vibrate &> /dev/null; then
                termux-vibrate -d 2000
                sleep 1
                termux-vibrate -d 2000
            fi
        fi
    fi
    
    # Check hardware connection every 5 minutes
    if [ $(date +%M | sed 's/^0//') -ne 0 ] && [ $(($(date +%M | sed 's/^0//') % 5)) -eq 0 ]; then
        HARDWARE_CHECK=$(curl -s http://localhost:8083/api/v1/hardware/read)
        if echo $HARDWARE_CHECK | grep -q "error"; then
            echo "$TIMESTAMP: ⚠️  Hardware connection issue detected" >> $LOG_FILE
        else
            echo "$TIMESTAMP: 🔌 Hardware connection OK" >> $LOG_FILE
        fi
    fi
    
    sleep 60  # Check every minute
done
