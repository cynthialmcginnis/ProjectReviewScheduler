# Project Review Scheduler

## Overview

Project Review Scheduler is a comprehensive system designed to automate and streamline the process of scheduling and managing project reviews. It helps organizations maintain compliance with review requirements, ensure appropriate reviewer assignments, and track the status of reviews across the organization.

## Key Features

- **Due Date Calculation**: Automatically calculates project review due dates based on configurable frequency parameters
- **Reviewer Assignment**: Intelligently assigns reviewers based on workload balance and department separation
- **Notification System**: Sends email notifications to reviewers about pending and overdue reviews
- **Reporting Module**: Generates comprehensive reports including monthly schedules, workload distribution, and overdue alerts
- **Multiple Interfaces**: Command-line interface for automation and Streamlit web interface for user-friendly access

## Deployment Strategies

This project implements several deployment strategies to ensure reliability and maintainability:

- **Phased Deployment**: Both command-line and web-based interfaces allow for incremental adoption
- **Safe Deployment with Backups**: Automatic timestamped backups created before any data modifications
- **Adaptive File Creation**: System checks for necessary files and creates them with appropriate headers if missing
- **Data Validation**: Comprehensive validation ensures data integrity and prevents corrupted data from being deployed

## Maintenance Techniques

The codebase is designed with maintainability in mind:

- **Comprehensive Documentation**: Detailed docstrings and comments throughout the code
- **Modular Design**: Code organized into distinct functional modules for easier maintenance
- **Error Handling**: Try/except blocks in critical sections to gracefully handle failures
- **Configuration Management**: Command-line arguments allow flexible configuration without code changes
- **Referential Integrity Checks**: Validation for relationships between data entities

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/cynthialmcginnis/ProjectReviewScheduler.git
   cd ProjectReviewScheduler
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

The scheduler.py file provides a command-line interface with several commands:

```
python scheduler.py calculate_reviews
python scheduler.py assign_reviewers
python scheduler.py send_notifications
python scheduler.py generate_reports
```

### Web Interface

The Streamlit app provides a user-friendly interface:

```
streamlit run streamlit_app.py
```

## Data Files

- **Projects.csv**: Contains project information including review frequency and status
- **Users.csv**: Contains reviewer information including department and workload
- **Reviews.csv**: Contains review assignments and status information

## Testing

The project includes comprehensive test cases covering all major functionality:

- Due date calculation tests
- Reviewer assignment tests
- Notification system tests
- Reporting module tests

Run all tests with:

```
python run_all_tests.py
```

## Project Structure

- `scheduler.py`: Main implementation module
- `streamlit_app.py`: Web interface using Streamlit
- `utils.py`: Utility functions
- `test_*.py`: Test files for different modules
- `*.csv`: Data files
- `TestCases/`: Test case documentation

## Dependencies

- pandas
- streamlit
- matplotlib
- dateutil
- faker (for test data generation)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
