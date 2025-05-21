# test_reporting_module.py
# Test Case: TC_RP_004 - Validate generation of review schedule with correct formatting and sorting

import unittest
from unittest.mock import patch
from scheduler import generate_monthly_schedule

class TestReportingModule(unittest.TestCase):

    @patch("scheduler.get_all_projects")
    @patch("scheduler.get_all_reviews")
    @patch("scheduler.get_reviewer")
    @patch("scheduler.write_csv")
    def test_generate_monthly_review_schedule(self, mock_write_csv, mock_get_reviewer, mock_get_all_reviews, mock_get_all_projects):
        # Sample data for May 2025
        mock_get_all_reviews.return_value = [
            {"Review_ID": "R001", "Project_ID": "P001", "Reviewer_ID": "U001", "Scheduled_Date": "2025-05-10", "Status": "Scheduled"},
            {"Review_ID": "R002", "Project_ID": "P002", "Reviewer_ID": "U002", "Scheduled_Date": "2025-05-05", "Status": "In Progress"},
            {"Review_ID": "R003", "Project_ID": "P003", "Reviewer_ID": "U003", "Scheduled_Date": "2025-06-01", "Status": "Scheduled"},
            {"Review_ID": "R004", "Project_ID": "P004", "Reviewer_ID": "U004", "Scheduled_Date": "2025-05-20", "Status": "Completed"}
        ]

        mock_get_all_projects.return_value = [
            {"Project_ID": "P001", "Project_Name": "AI Audit"},
            {"Project_ID": "P002", "Project_Name": "Cyber Compliance"},
            {"Project_ID": "P003", "Project_Name": "Cloud Update"},
            {"Project_ID": "P004", "Project_Name": "DevOps Review"},
        ]

        mock_get_reviewer.side_effect = lambda uid: {"U001": {"Name": "Alice"},
                                                     "U002": {"Name": "Bob"},
                                                     "U003": {"Name": "Carol"},
                                                     "U004": {"Name": "Dana"}}.get(uid, {"Name": "Unknown"})

        # Call the function
        result = generate_monthly_schedule(month="05", year="2025", output_file="test_monthly_schedule.csv")

        # Ensure only two reviews included
        self.assertEqual(result["review_count"], 2)
        mock_write_csv.assert_called_once()

        # Capture the written data
        _, written_data, fieldnames = mock_write_csv.call_args[0]
        dates = [row["Scheduled_Date"] for row in written_data]
        self.assertEqual(dates, sorted(dates))  # Ensure sorted
        self.assertEqual(fieldnames, ['Project_ID', 'Project_Name', 'Reviewer_Name', 'Scheduled_Date', 'Status'])

if __name__ == '__main__':
    unittest.main()
