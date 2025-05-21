
import unittest
from unittest.mock import patch
from scheduler import assign_reviewer

class TestReviewerAssignmentFallback(unittest.TestCase):
    @patch('scheduler.update_user')  # Mock update_user to avoid file write
    @patch('scheduler.add_review')   # Mock add_review to avoid writing reviews
    def test_fallback_same_department_and_load_balancing(self, mock_add_review, mock_update_user):
        project = {
            "Project_ID": "P1001",
            "Project_Name": "Fallback Logic Test",
            "Department": "IT",
            "Status": "Overdue"
        }

        reviewers = [
            {"User_ID": "U001", "Department": "IT", "Current_Load": "3"},
            {"User_ID": "U002", "Department": "IT", "Current_Load": "1"},
            {"User_ID": "U003", "Department": "IT", "Current_Load": "2"},
        ]

        assignment = assign_reviewer(project, reviewers)
        self.assertIsNotNone(assignment)
        self.assertEqual(assignment['Reviewer_ID'], 'U002')
        self.assertEqual(assignment['Project_ID'], 'P1001')
        self.assertEqual(assignment['Status'], 'Scheduled')

if __name__ == "__main__":
    unittest.main()
