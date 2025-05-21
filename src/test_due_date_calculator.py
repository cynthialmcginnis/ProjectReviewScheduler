
import unittest
from unittest.mock import patch
from datetime import datetime
import scheduler

class TestDueDateCalculator(unittest.TestCase):

    @patch('scheduler.read_csv')
    @patch('scheduler.write_csv')
    def test_due_date_six_months(self, mock_write_csv, mock_read_csv):
        # Setup mock project data
        projects = [{
            "Project_ID": "P001",
            "Project_Name": "Security Review",
            "Start_Date": "2025-01-01",
            "Last_Review_Date": "2025-01-01",
            "Review_Frequency_Years": "0.5",
            "Department": "IT",
            "Status": "",
            "Next_Review_Date": ""
        }]

        # Mock return value for read_csv
        mock_read_csv.return_value = projects

        # Execute calculation with a fixed current date
        result = scheduler.calculate_all_reviews("Projects.csv", current_date="2025-06-01")

        # Extract updated projects written to CSV
        written_projects = mock_write_csv.call_args[0][1]
        updated = written_projects[0]

        # Validate the calculated date and status
        self.assertEqual(updated['Next_Review_Date'], '2025-07-01')
        self.assertEqual(updated['Status'], 'Due Soon')
        self.assertEqual(result['due_soon'], 1)
        self.assertEqual(result['total_projects'], 1)

if __name__ == '__main__':
    unittest.main()
