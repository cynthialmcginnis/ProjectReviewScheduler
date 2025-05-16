
import unittest
from unittest.mock import patch
from scheduler import assign_all_reviewers

class TestReviewerAssignment(unittest.TestCase):

    @patch('scheduler.read_csv')
    @patch('scheduler.write_csv')
    def test_department_conflict_and_load_balancing(self, mock_write_csv, mock_read_csv):
        # Projects needing assignment
        projects = [{
            "Project_ID": "P001",
            "Project_Name": "Test Project",
            "Start_Date": "2025-01-01",
            "Last_Review_Date": "2025-01-01",
            "Review_Frequency_Years": "1",
            "Department": "IT",
            "Status": "Overdue",
            "Next_Review_Date": "2025-05-01"
        }]
        
        # Users (all different departments with varying loads)
        users = [
            {"User_ID": "U001", "Name": "Alice", "Email": "a@example.com", "Department": "IT", "Current_Load": "2"},
            {"User_ID": "U002", "Name": "Bob", "Email": "b@example.com", "Department": "HR", "Current_Load": "1"},
            {"User_ID": "U003", "Name": "Carol", "Email": "c@example.com", "Department": "Finance", "Current_Load": "0"}
        ]

        reviews = []
        
        # Load balancing test
        mock_read_csv.side_effect = [projects, users, reviews]
        result = assign_all_reviewers("Projects.csv", "Users.csv", "Reviews.csv")
        written_reviews = mock_write_csv.call_args[0][1]
        assigned_reviewer_id = written_reviews[0]['Reviewer_ID']
        self.assertEqual(assigned_reviewer_id, "U003")  # Should choose lowest load

    @patch('scheduler.read_csv')
    @patch('scheduler.write_csv')
    def test_all_reviewers_same_department(self, mock_write_csv, mock_read_csv):
        projects = [{
            "Project_ID": "P002",
            "Project_Name": "Same Department Project",
            "Start_Date": "2025-01-01",
            "Last_Review_Date": "2025-01-01",
            "Review_Frequency_Years": "1",
            "Department": "Finance",
            "Status": "Overdue",
            "Next_Review_Date": "2025-05-01"
        }]
        
        users = [
            {"User_ID": "U004", "Name": "Dave", "Email": "d@example.com", "Department": "Finance", "Current_Load": "1"},
            {"User_ID": "U005", "Name": "Eve", "Email": "e@example.com", "Department": "Finance", "Current_Load": "2"}
        ]

        reviews = []

        mock_read_csv.side_effect = [projects, users, reviews]
        result = assign_all_reviewers("Projects.csv", "Users.csv", "Reviews.csv")
        written_reviews = mock_write_csv.call_args[0][1]
        assigned_reviewer_id = written_reviews[0]['Reviewer_ID']
        self.assertIn(assigned_reviewer_id, ["U004", "U005"])  # Must fall back to same department

    @patch('scheduler.read_csv')
    @patch('scheduler.write_csv')
    def test_no_reviewers_available(self, mock_write_csv, mock_read_csv):
        projects = [{
            "Project_ID": "P003",
            "Project_Name": "No Reviewer Project",
            "Start_Date": "2025-01-01",
            "Last_Review_Date": "2025-01-01",
            "Review_Frequency_Years": "1",
            "Department": "QA",
            "Status": "Overdue",
            "Next_Review_Date": "2025-05-01"
        }]
        
        users = []  # No reviewers
        reviews = []

        mock_read_csv.side_effect = [projects, users, reviews]
        result = assign_all_reviewers("Projects.csv", "Users.csv", "Reviews.csv")
        self.assertEqual(result['total_assigned'], 0)

if __name__ == '__main__':
    unittest.main()

