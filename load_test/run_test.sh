#!/bin/bash

# ChromaDB Load Test Runner
# Usage: ./run_test.sh [scenario] [host] [users] [duration]

# Default values
SCENARIO=${1:-"quick"}
HOST=${2:-"http://localhost:5115"}
USERS=${3:-"10"}
DURATION=${4:-"1m"}

echo "Starting ChromaDB Load Test..."
echo "Scenario: $SCENARIO"
echo "Host: $HOST"
echo "Users: $USERS"
echo "Duration: $DURATION"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

case $SCENARIO in
    "quick")
        echo "Running Quick Test (10 users, 1 minute)"
        locust -f load_test.py --host=$HOST --users=10 --spawn-rate=2 --run-time=1m --headless --html=quick_test_report.html
        ;;
    "stress")
        echo "Running Stress Test (100 users, 5 minutes)"
        locust -f load_test.py --host=$HOST --users=100 --spawn-rate=10 --run-time=5m --headless --html=stress_test_report.html
        ;;
    "endurance")
        echo "Running Endurance Test (20 users, 30 minutes)"
        locust -f load_test.py --host=$HOST --users=20 --spawn-rate=2 --run-time=30m --headless --html=endurance_test_report.html
        ;;
    "custom")
        echo "Running Custom Test ($USERS users, $DURATION)"
        locust -f load_test.py --host=$HOST --users=$USERS --spawn-rate=5 --run-time=$DURATION --headless --html=custom_test_report.html
        ;;
    "interactive")
        echo "Starting Interactive Test (Web UI at http://localhost:8089)"
        locust -f load_test.py --host=$HOST
        ;;
    *)
        echo "Available scenarios: quick, stress, endurance, custom, interactive"
        echo "Usage: ./run_test.sh [scenario] [host] [users] [duration]"
        echo ""
        echo "Examples:"
        echo "  ./run_test.sh quick"
        echo "  ./run_test.sh stress http://localhost:7000"
        echo "  ./run_test.sh custom http://localhost:5000 50 3m"
        echo "  ./run_test.sh interactive"
        exit 1
        ;;
esac

echo ""
echo "Test completed! Check the generated HTML report for detailed results."
