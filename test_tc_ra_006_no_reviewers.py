"""
Test Case: TC_RA_006
Purpose: Ensure the reviewer assignment handles the scenario where no reviewers are available gracefully.
"""

import unittest
from unittest.mock import patch
from scheduler import assign_all_reviewers

class TestNoReviewersAvailable(unittest.TestCase):

    @patch('scheduler.read_csv')
    @patch('scheduler.write_csv')
    def test_graceful_handling_when_no_reviewers_exist(self, mock_write_csv, mock_read_csv):
        # Only one project needing review
        projects = [{
            "Project_ID": "P006",
            "Project_Name": "Compliance Audit",
            "Start_Date": "2025-01-01",
            "Last_Review_Date": "2025-01-01",
            "Review_Frequency_Years": "1",
            "Department": "Finance",
            "Status": "Overdue",
            "Next_Review_Date": "2025-05-01"
        }]

        # No reviewers exist
        users = []  # Intentionally empty

        # Simulate read_csv returning projects, then users twice (initial + update_user)
        mock_read_csv.side_effect = [projects, users, users]

        # Run the reviewer assignment
        result = assign_all_reviewers("Projects.csv", "Users.csv", "Reviews.csv")

        # Assertions
        self.assertEqual(result['total_assigned'], 0)
        self.assertEqual(len(result['assignments']), 0)
        self.assertIn('assignments', result)
        print(" TC_RA_006 passed: No reviewers available handled correctly.")

if __name__ == '__main__':
    unittest.main()
