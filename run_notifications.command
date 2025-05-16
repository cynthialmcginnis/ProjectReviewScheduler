#!/bin/bash
# A script to assign reviewers, send overdue notifications, and display logs.

# Navigate to the folder where the script is located
cd "$(dirname "$0")"

echo "🔁 Resetting and assigning reviewers..."
python3 reset_and_assign.py

echo "📧 Sending overdue notifications..."
python3 scheduler.py send_notifications --status Overdue

echo ""
echo "📂 Displaying first 10 reviewer assignments from reviewer_assignments.csv:"
echo "-------------------------------------"
head -n 10 reviewer_assignments.csv
echo "..."

echo ""
echo "📨 Displaying email log (simulated from sent_emails_log.csv):"
echo "-------------------------------------"

# Display each email log entry in a readable format
tail -n +2 sent_emails_log.csv | while IFS=, read -r timestamp recipient subject body
do
  echo ""
  echo "🕒 Timestamp: $timestamp"
  echo "👤 To: $recipient"
  echo "📌 Subject: $subject"
  echo "📝 Body: $body"
done

echo ""
read -n 1 -s -r -p "✅ Done! Press any key to close..."
