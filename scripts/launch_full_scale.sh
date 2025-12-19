#!/bin/bash
# 🚀 HUMBU FULL-SCALE REVENUE LAUNCHER
# Launches the complete $147,575/month revenue generation system

echo "🚀 HUMBU FULL-SCALE REVENUE LAUNCH"
echo "💰 Target: $147,575/month ($0.47 per transaction)"
echo "📈 Required: 314,000 transactions/month"
echo "="*60

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to print colored messages
print_status() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: System Check
print_status "Step 1: System Health Check..."
if curl -s http://localhost:8083/health > /dev/null; then
    print_success "API is online"
else
    print_warning "API not running. Starting it..."
    python api/government_saas.py > data/logs/api_launch.log 2>&1 &
    sleep 5
fi

# Step 2: Check current revenue
print_status "Step 2: Checking current revenue..."
REVENUE_DATA=$(curl -s http://localhost:8083/revenue)
CURRENT_REV=$(echo $REVENUE_DATA | grep -o '"current_revenue":[0-9]*\.\?[0-9]*' | cut -d: -f2)
TODAY_TX=$(echo $REVENUE_DATA | grep -o '"transactions_today":[0-9]*' | cut -d: -f2)

print_success "Current Revenue: \$${CURRENT_REV:-0}"
print_success "Transactions Today: ${TODAY_TX:-0}"

# Step 3: Calculate needed transactions
print_status "Step 3: Calculating target..."
TARGET=147575
REMAINING=$(echo "$TARGET - ${CURRENT_REV:-0}" | bc)
DAILY_NEEDED=$(echo "$REMAINING / 11" | bc)  # 11 days remaining in month
TX_NEEDED=$(echo "$DAILY_NEEDED / 0.47" | bc)

print_warning "Remaining Target: \$$REMAINING"
print_warning "Daily Needed: \$$DAILY_NEEDED"
print_warning "Transactions Needed Today: $TX_NEEDED"

# Step 4: Launch Revenue Rocket
print_status "Step 4: Launching Revenue Rocket..."
echo ""
echo "🚀 SELECT LAUNCH MODE:"
echo "   1. FULL POWER - Continuous generation (Recommended)"
echo "   2. BURST MODE - Generate $TX_NEEDED transactions now"
echo "   3. GOVERNMENT SURGE - High-volume simulation"
echo "   4. MOBILE CONTROL - Manual control"
echo "   5. CANCEL"
echo ""

read -p "Select mode (1-5): " MODE

case $MODE in
    1)
        print_status "🚀 LAUNCHING FULL POWER MODE..."
        print_warning "This will generate continuous revenue until stopped"
        print_warning "Press Ctrl+C to stop when target reached"
        echo ""
        
        # Calculate target transactions per minute
        TX_PER_MINUTE=$(echo "$TX_NEEDED / (24 * 60)" | bc)
        TX_PER_MINUTE=$(( TX_PER_MINUTE > 100 ? 100 : TX_PER_MINUTE ))
        TX_PER_MINUTE=$(( TX_PER_MINUTE < 10 ? 10 : TX_PER_MINUTE ))
        
        print_success "Setting rate: $TX_PER_MINUTE transactions/minute"
        print_success "Expected revenue: \$$(echo "$TX_PER_MINUTE * 0.47 * 60" | bc)/hour"
        
        # Launch in background
        python scripts/revenue_rocket.py 3 $TX_PER_MINUTE > data/logs/rocket_launch.log 2>&1 &
        ROCKET_PID=$!
        
        print_success "Revenue Rocket launched with PID: $ROCKET_PID"
        echo ""
        echo "📊 MONITORING COMMANDS:"
        echo "   Revenue: curl http://localhost:8083/revenue"
        echo "   Logs: tail -f data/logs/rocket_launch.log"
        echo "   Stop: kill $ROCKET_PID"
        echo ""
        
        # Start monitoring loop
        while kill -0 $ROCKET_PID 2>/dev/null; do
            sleep 30
            CURRENT=$(curl -s http://localhost:8083/revenue | grep -o '"current_revenue":[0-9]*\.\?[0-9]*' | cut -d: -f2)
            PERCENT=$(echo "scale=2; $CURRENT / $TARGET * 100" | bc)
            echo -e "${BLUE}[Progress]${NC} \$$CURRENT / \$$TARGET (${PERCENT}%)"
            
            if (( $(echo "$CURRENT >= $TARGET" | bc -l) )); then
                print_success "🎉 TARGET REACHED! Monthly revenue goal achieved!"
                kill $ROCKET_PID
                break
            fi
        done
        ;;
    
    2)
        print_status "🚀 LAUNCHING BURST MODE..."
        print_warning "Generating $TX_NEEDED transactions now..."
        
        # Split into manageable batches
        BATCH_SIZE=100
        BATCHES=$(( (TX_NEEDED + BATCH_SIZE - 1) / BATCH_SIZE ))
        
        for ((i=1; i<=BATCHES; i++)); do
            print_status "Batch $i/$BATCHES ($((i*BATCH_SIZE)) transactions)..."
            python scripts/revenue_rocket.py 1 $BATCH_SIZE > /dev/null 2>&1
            
            # Update progress
            CURRENT=$(curl -s http://localhost:8083/revenue | grep -o '"current_revenue":[0-9]*\.\?[0-9]*' | cut -d: -f2)
            PERCENT=$(echo "scale=2; $CURRENT / $TARGET * 100" | bc)
            echo -e "${BLUE}[Progress]${NC} \$$CURRENT / \$$TARGET (${PERCENT}%)"
        done
        
        print_success "🎉 Burst complete!"
        ;;
    
    3)
        print_status "🏛️  LAUNCHING GOVERNMENT SURGE..."
        python scripts/revenue_rocket.py 4
        ;;
    
    4)
        print_status "📱 LAUNCHING MOBILE CONTROL..."
        python scripts/mobile_control.py
        ;;
    
    5)
        print_status "Launch cancelled"
        exit 0
        ;;
    
    *)
        print_error "Invalid selection"
        exit 1
        ;;
esac

# Final status
print_status "Final System Status:"
curl -s http://localhost:8083/revenue | python3 -c "
import sys, json
data = json.load(sys.stdin)
current = data.get('current_revenue', 0)
target = data.get('monthly_target', 147575)
percent = (current / target * 100) if target > 0 else 0
print(f'💰 Revenue: \${current:,.2f} / \${target:,.2f}')
print(f'📈 Progress: {percent:.2f}%')
print(f'🎯 Target Status: {\"✅ ACHIEVED\" if current >= target else \"🚀 IN PROGRESS\"}')
"

print_success "🚀 Humbu Revenue System active and generating!"
echo "Monitor at: http://localhost:8083/"
