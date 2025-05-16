"""
Test Case: TC_RA_003 – Reviewer Department Separation

This unit test verifies that the reviewer assignment algorithm avoids selecting
a reviewer from the same department as the project when reviewers from other departments are available.
"""

import unittest
from unittest.mock import patch
from scheduler import assign_reviewer

class TestReviewerDepartmentSeparation(unittest.TestCase):

    @patch('scheduler.update_user')
    @patch('scheduler.add_review')
    def test_avoid_same_department_reviewer(self, mock_add_review, mock_update_user):
        # Project is from IT department
        project = {
            "Project_ID": "P001",
            "Department": "IT"
        }

        # Reviewers with different departments
        reviewers = [
            {"User_ID": "U001", "Name": "Alice", "Department": "IT", "Current_Load": 1},
            {"User_ID": "U002", "Name": "Bob", "Department": "HR", "Current_Load": 2},
            {"User_ID": "U003", "Name": "Charlie", "Department": "Finance", "Current_Load": 1}
        ]

        review = assign_reviewer(project, reviewers)
        assigned_id = review['Reviewer_ID']

        # U001 is from same department (IT) and should NOT be selected if others exist
        self.assertIn(assigned_id, ["U002", "U003"], "Reviewer from different department should be assigned")

if __name__ == '__main__':
    unittest.main()
