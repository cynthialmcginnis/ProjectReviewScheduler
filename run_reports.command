#!/bin/bash
cd ~/Documents/ProjectReviewScheduler
python3 scheduler.py generate_reports --type all
read -n 1 -s -r -p "Press any key to close..."
