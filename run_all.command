#!/bin/bash
cd "$(dirname "$0")"

echo "🔁 Resetting and assigning reviewers..."
python3 reset_and_assign.py

echo "📊 Generating all reports..."
python3 scheduler.py generate_reports --type all

echo "📂 Opening visual outputs..."
open workload_report_*.csv
open overdue_alerts_*.csv
open monthly_schedule_*.csv

read -n 1 -s -r -p "✅ Done! Press any key to close..."
