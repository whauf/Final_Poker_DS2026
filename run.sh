#!/bin/bash
# run.sh - One-liner launcher for Poker Advisor

set -e  # Exit on error

echo " Building Poker Advisor Docker image..."
docker build -t poker-advisor:latest .

echo " Running Poker Advisor on http://localhost:8000..."
docker run --rm \
  -p 8000:8000 \
  --env-file .env.example \
  poker-advisor:latest

echo "   Poker Advisor is running. Visit http://localhost:8000 in your browser."
