"""
Test Case: TC_NT_002 – Notification System
Verify overdue review notifications include correct urgency indicators and are sent to the right reviewer.
"""

import unittest
from unittest.mock import patch, MagicMock
from scheduler import send_notifications

class TestNotificationSystem(unittest.TestCase):

    @patch("scheduler.read_csv")
    @patch("scheduler.smtplib.SMTP")
    def test_overdue_email_notification(self, mock_smtp, mock_read_csv):
        # Mocked data setup
        projects = [{
            "Project_ID": "P002",
            "Project_Name": "Critical Security Review",
            "Status": "Overdue",
            "Next_Review_Date": "2025-04-15",
            "Department": "IT"
        }]
        reviews = [{
            "Review_ID": "R001",
            "Project_ID": "P002",
            "Reviewer_ID": "U002",
            "Scheduled_Date": "2025-04-15",
            "Status": "Scheduled",
            "Completion_Date": ""
        }]
        users = [{
            "User_ID": "U002",
            "Name": "Jane Doe",
            "Email": "reviewer@example.com",
            "Department": "IT",
            "Current_Load": "1"
        }]

        # Ensure correct read_csv call order
        mock_read_csv.side_effect = [projects, reviews, users]

        # Mock SMTP server behavior
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Run the function
        result = send_notifications(status_filter="Overdue", smtp_server="localhost", smtp_port=587)

        print("DEBUG result:", result)

        # Assertions
        self.assertEqual(result["sent"], 1)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(result["total"], 1)
        self.assertIn("reviewer@example.com", result["log"][0]["reviewer_email"])
        self.assertIn("URGENT", result["log"][0]["subject"].upper())
        self.assertIn("REVIEW REQUIRED", result["log"][0]["subject"].upper())


if __name__ == "__main__":
    unittest.main()
