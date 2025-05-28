#!/usr/bin/env python
# coding: utf-8

# In[26]:


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# In[28]:


"""
Project Review Scheduler - Main Implementation Module

This module implements the core functionality for the Project Review Scheduler system,
including due date calculation, reviewer assignment, notification, and reporting.
"""


import sys
import os

from pathlib import Path

# Add your project directory to sys.path
project_dir = Path.home() / "Documents" / "ProjectReviewScheduler"
sys.path.append(str(project_dir))

import os
import csv
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

#from faker import Faker
#import random
#fake = Faker()

#from utils import safe_parse_date
from dateutil.relativedelta import relativedelta

   


# In[30]:


def parse_args(args):
    parsed = {}

    if not args:
        parsed["command"] = "help"
        return parsed

    parsed["command"] = args[0]

    for i in range(1, len(args)):
        if args[i].startswith("--"):
            key = args[i][2:].replace("-", "_")  # allow both --csv-file and --csv_file
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                parsed[key] = args[i + 1]
            else:
                parsed[key] = True

    return parsed


# In[32]:


# ===============================================================================
# Data Access Functions
# ===============================================================================

import os
import csv
from datetime import datetime

def read_csv(file_path):
    """
    Read data from a CSV file. If missing, create a new one with the default schema.

    Args:
        file_path (str): Full or relative path to the CSV file.

    Returns:
        list: List of rows as dictionaries.
    """
    if not os.path.exists(file_path):
        print(f"⚠️ {file_path} not found. Creating with headers...")
        create_csv_if_missing(file_path)
        return []

    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def write_csv(file_path, data, fieldnames=None):
    """
    Write data to a CSV file. Backs up old file if it exists.

    Args:
        file_path (str): Path to the CSV file
        data (list): List of dictionaries to write
        fieldnames (list): Optional list of field names. Uses keys from first row if omitted.
    """
    if not data:
        print(f"⚠️ No data to write to {file_path}")
        return

    if fieldnames is None:
        fieldnames = data[0].keys()

    # Backup existing file
    if os.path.exists(file_path):
        backup_file(file_path)

    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def backup_file(file_path):
    """
    Create a backup copy of a file with a timestamp.

    Args:
        file_path (str): Path to the file to backup
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.{timestamp}.bak"
    with open(file_path, 'r') as src, open(backup_path, 'w') as dst:
        dst.write(src.read())
    print(f"🗂️  Backed up {file_path} → {backup_path}")

def create_csv_if_missing(file_path, schema=None):
    """
    Create a CSV file with headers based on filename patterns if it doesn't exist.

    Args:
        file_path (str): Path to the file

    Returns:
        bool: True if file was created, False if it already existed
    """
    if os.path.exists(file_path):
        return False

    filename = os.path.basename(file_path)
    headers = []

    if "Projects" in filename:
        headers = ["Project_ID", "Project_Name", "Start_Date", "Last_Review_Date",
                   "Review_Frequency_Years", "Department", "Status", "Next_Review_Date"]
    elif "Users" in filename:
        headers = ["User_ID", "Name", "Email", "Department", "Current_Load"]
    elif "Reviews" in filename:
        headers = ["Review_ID", "Project_ID", "Reviewer_ID", "Scheduled_Date",
                   "Status", "Completion_Date"]
    else:
        headers = ["ID"]  # fallback

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

    print(f"✅ Created new CSV: {file_path} with headers: {headers}")
    return True

# Convenience shortcuts
def get_all_projects(file_path='Projects.csv'):
    return read_csv(file_path)

def get_all_users(file_path='Users.csv'):
    return read_csv(file_path)

def get_all_reviews(file_path='Reviews.csv'):
    return read_csv(file_path)

def get_projects_by_status(status, file_path='Projects.csv'):
    return [p for p in read_csv(file_path) if p.get('Status') == status]

def get_reviews_by_project(project_id, file_path='Reviews.csv'):
    return [r for r in read_csv(file_path) if r.get('Project_ID') == project_id]

def get_reviewer(reviewer_id, file_path='Users.csv'):
    for user in read_csv(file_path):
        if user.get('User_ID') == reviewer_id:
            return user
    return None

def update_project(project, file_path='Projects.csv'):
    projects = read_csv(file_path)
    for i, p in enumerate(projects):
        if p.get('Project_ID') == project.get('Project_ID'):
            projects[i] = project
            break
    write_csv(file_path, projects)

def update_user(user, file_path='Users.csv'):
    users = read_csv(file_path)
    for i, u in enumerate(users):
        if u.get('User_ID') == user.get('User_ID'):
            users[i] = user
            break
    write_csv(file_path, users)

def add_review(review, file_path='Reviews.csv'):
    reviews = read_csv(file_path)
    reviews.append(review)
    write_csv(file_path, reviews)

def update_review(review, file_path='Reviews.csv'):
    reviews = read_csv(file_path)
    for i, r in enumerate(reviews):
        if r.get('Review_ID') == review.get('Review_ID'):
            reviews[i] = review
            break
    write_csv(file_path, reviews)


# In[34]:


# ===============================================================================
# Data Validation Functions
# ===============================================================================

def validate_csv_data(file_path, schema=None):
    """
    Validate the data in a CSV file against a schema.
    
    Args:
        file_path (str): Path to the CSV file
        schema (dict, optional): Dictionary defining the validation rules
        
    Returns:
        dict: Validation result with 'valid' flag and list of 'errors'
    """
    # Create file if it doesn't exist
    if not os.path.exists(file_path):
        create_csv_if_missing(file_path, schema)
        return {'valid': True, 'errors': []}
    
    # Determine schema based on filename if not provided
    if schema is None:
        filename = os.path.basename(file_path)
        if 'Projects' in filename:
            schema = {
                'Project_ID': {'type': 'string', 'required': True},
                'Project_Name': {'type': 'string', 'required': True},
                'Start_Date': {'type': 'date', 'required': True},
                'Last_Review_Date': {'type': 'date', 'required': True},
                'Review_Frequency_Years': {'type': 'decimal', 'required': True},
                'Department': {'type': 'string', 'required': True}
            }
        elif 'Users' in filename:
            schema = {
                'User_ID': {'type': 'string', 'required': True},
                'Name': {'type': 'string', 'required': True},
                'Email': {'type': 'string', 'required': True},
                'Department': {'type': 'string', 'required': True}
            }
        elif 'Reviews' in filename:
            schema = {
                'Review_ID': {'type': 'string', 'required': True},
                'Project_ID': {'type': 'string', 'required': True},
                'Reviewer_ID': {'type': 'string', 'required': True},
                'Scheduled_Date': {'type': 'date', 'required': True},
                'Status': {'type': 'string', 'required': True}
            }
    
    data = read_csv(file_path)
    errors = []
    
    # Check each row against the schema
    for i, row in enumerate(data, start=2):  # Start from 2 to account for header row
        for field, rules in schema.items():
            # Check required fields
            if rules.get('required', False) and (field not in row or not row[field]):
                errors.append({
                    'row': i,
                    'field': field,
                    'message': f"Required field '{field}' is missing or empty in row {i}"
                })
                continue
            
            # Skip validation if field is not present
            if field not in row or not row[field]:
                continue
            
            # Validate data types
            value = row[field]
            if rules.get('type') == 'date':
                try:
                    datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    errors.append({
                        'row': i,
                        'field': field,
                        'message': f"Field '{field}' with value '{value}' is not a valid date (YYYY-MM-DD) in row {i}"
                    })
            elif rules.get('type') == 'decimal' or rules.get('type') == 'integer':
                try:
                    float(value)
                    if rules.get('type') == 'integer' and '.' in value:
                        errors.append({
                            'row': i,
                            'field': field,
                            'message': f"Field '{field}' with value '{value}' should be an integer in row {i}"
                        })
                except ValueError:
                    errors.append({
                        'row': i,
                        'field': field,
                        'message': f"Field '{field}' with value '{value}' is not a valid number in row {i}"
                    })
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_referential_integrity():
    """
    Validate referential integrity between CSV files.
    
    Returns:
        dict: Validation result with 'valid' flag and list of 'errors'
    """
    projects = get_all_projects()
    users = get_all_users()
    reviews = get_all_reviews()
    
    errors = []
    
    # Create sets of IDs for faster lookup
    project_ids = {p.get('Project_ID') for p in projects}
    user_ids = {u.get('User_ID') for u in users}
    
    # Check Reviews reference valid Projects and Users
    for i, review in enumerate(reviews, start=2):  # Start from 2 to account for header row
        project_id = review.get('Project_ID')
        if project_id not in project_ids:
            errors.append({
                'row': i,
                'field': 'Project_ID',
                'message': f"Review references Project_ID: {project_id} which does not exist"
            })
        
        reviewer_id = review.get('Reviewer_ID')
        if reviewer_id not in user_ids:
            errors.append({
                'row': i,
                'field': 'Reviewer_ID',
                'message': f"Review references Reviewer_ID: {reviewer_id} which does not exist"
            })
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


# In[96]:


# ===============================================================================
# Due Date Calculator
# ===============================================================================

from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def calculate_due_dates(projects_df, current_date=None):
    """
    Calculate the next review date based on the project’s last review date and review frequency in years.
    
    Args:
        projects_df (DataFrame): A dataframe containing project details including 'Start_Date' and 'Review_Frequency_Years'.
        current_date (datetime, optional): The current date to compare. Defaults to None, in which case the current system date is used.

    Returns:
        DataFrame: Updated project data with Next_Review_Date and Status fields
    """
    if current_date is None:
        current_date = datetime.now()
    
    # Ensure Start_Date is in datetime format
    projects_df['Start_Date'] = pd.to_datetime(projects_df['Start_Date'], errors='coerce')

    # Function to calculate next review date
    def calculate_for_project(row):
        # Last review date (Start Date of the project)
        last_review = row['Start_Date']

        # Frequency in years
        frequency_years = row['Review_Frequency_Years']
        
        # Convert frequency in years to months (12 months per year)
        frequency_months = int(frequency_years * 12)  # Convert years to months
        
        # Add the calculated months to the last review date
        next_review = last_review + relativedelta(months=frequency_months)
        
        # Calculate the number of days until the next review date
        days_until_review = (next_review - current_date).days
        
        # Assign status based on how many days until the review
        if days_until_review < 0:
            status = 'Overdue'
        elif days_until_review <= 30:
            status = 'Due Soon'
        else:
            status = 'Up to Date'
        
        # Return updated values
        return pd.Series({
            'Next_Review_Date': next_review,  # Store as datetime, not string
            'Status': status
        })

    # Apply the function to each row in the DataFrame
    projects_df[['Next_Review_Date', 'Status']] = projects_df.apply(calculate_for_project, axis=1)

    return projects_df


    # Function to calculate next review date
    def calculate_for_project(row):
        # Last review date (Start Date of the project)
        last_review = row['Start_Date']

        # Frequency in years
        frequency_years = row['Review_Frequency_Years']
        
        # Convert frequency in years to months (12 months per year)
        frequency_months = int(frequency_years * 12)  # Convert years to months
        
        # Add the calculated months to the last review date
        next_review = last_review + relativedelta(months=frequency_months)
        
        # Calculate the number of days until the next review date
        days_until_review = (next_review - current_date).days
        
        # Assign status based on how many days until the review
        if days_until_review < 0:
            status = 'Overdue'
        elif days_until_review <= 30:
            status = 'Due Soon'
        else:
            status = 'Up to Date'
        
        # Return updated values
        return pd.Series({
            'Next_Review_Date': next_review.strftime('%Y-%m-%d'),
            'Status': status
        })

    # Apply the function to each row in the DataFrame
    projects_df[['Next_Review_Date', 'Status']] = projects_df.apply(calculate_for_project, axis=1)

    return projects_df


    # Function to calculate next review date
    def calculate_for_project(row):
        # Last review date (Start Date of the project)
        last_review = row['Start_Date']

        # Frequency in years, convert to months
        frequency_years = row['Review_Frequency_Years']
        frequency_months = int(frequency_years * 12)  # Convert years to months
        
        # Add the months to the last review date
        next_review = last_review + relativedelta(months=frequency_months)
        
        # Calculate the number of days until the next review date
        days_until_review = (next_review - current_date).days
        
        # Assign status based on how many days until the review
        if days_until_review < 0:
            status = 'Overdue'
        elif days_until_review <= 30:
            status = 'Due Soon'
        else:
            status = 'Up to Date'
        
        # Return updated values
        return pd.Series({
            'Next_Review_Date': next_review.strftime('%Y-%m-%d'),
            'Status': status
        })

    # Apply the function to each row in the DataFrame
    projects_df[['Next_Review_Date', 'Status']] = projects_df.apply(calculate_for_project, axis=1)

    return projects_df

    

    

def calculate_all_reviews(projects_file='Projects.csv', current_date=None):
    """
    Calculate review dates for all projects and update the Projects CSV file.
    
    Args:
        projects_file (str): Path to the Projects CSV file
        current_date (datetime or str, optional): Current date for comparison. Defaults to today.
        
    Returns:
        dict: Summary of calculation results
    """
    if current_date is None:
        current_date = datetime.now()
    elif isinstance(current_date, str):
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
    
    # Read projects data
    projects = read_csv(projects_file)
    
    # Calculate due dates and update status
    for project in projects:
        updated_project = calculate_due_date(project, current_date)
        project.update(updated_project)
    
    # Write updated data back to CSV
    write_csv(projects_file, projects)
    
    # Generate summary
    status_counts = {
        'overdue': len([p for p in projects if p['Status'] == 'Overdue']),
        'due_soon': len([p for p in projects if p['Status'] == 'Due Soon']),
        'up_to_date': len([p for p in projects if p['Status'] == 'Up to Date']),
        'total_projects': len(projects)
    }
    
    return status_counts


# In[80]:


# ===============================================================================
# Reviewer Assignment
# ===============================================================================
def assign_reviewer(project, reviewers=None):
    """
    Assign a reviewer to a project based on workload balance and department.
    Returns None if no reviewers are available.
    """
    if reviewers is None:
        reviewers = get_all_users()
    
    if not reviewers:
        return None  # 🚨 No reviewers at all
    
    # Convert Current_Load to int
    for reviewer in reviewers:
        try:
            reviewer['Current_Load'] = int(reviewer.get('Current_Load', 0))
        except ValueError:
            reviewer['Current_Load'] = 0

    # Sort reviewers by load
    reviewers_sorted = sorted(reviewers, key=lambda r: r['Current_Load'])
    
    # Try to select from a different department
    project_dept = project.get('Department', '')
    other_dept_reviewers = [r for r in reviewers_sorted if r.get('Department') != project_dept]
    
    # Assign reviewer
    if other_dept_reviewers:
        assigned_reviewer = other_dept_reviewers[0]
    else:
        # ❗ Fallback: same department
        if not reviewers_sorted:
            return None  # 🛑 Still no one to assign
        assigned_reviewer = reviewers_sorted[0]
    
    # Update workload and persist
    assigned_reviewer['Current_Load'] += 1
    update_user(assigned_reviewer)
    
    # Build review object
    review = {
        'Review_ID': f"R{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'Project_ID': project['Project_ID'],
        'Reviewer_ID': assigned_reviewer['User_ID'],
        'Scheduled_Date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'Status': 'Scheduled',
        'Completion_Date': ''
    }

    add_review(review)
    return review

def assign_all_reviewers(projects_file='Projects.csv', users_file='Users.csv', reviews_file='Reviews.csv'):
    """
    Assign reviewers to all projects needing review (Overdue or Due Soon).
    
    Returns:
        dict: Summary of assignment results
    """
    # Read data
    projects = read_csv(projects_file)
    users = read_csv(users_file)
    existing_reviews = read_csv(reviews_file)
    
    # Projects needing review
    projects_needing_review = [p for p in projects 
                               if p.get('Status') in ['Overdue', 'Due Soon']]
    
    # Exclude projects with active reviews
    active_project_ids = {r['Project_ID'] for r in existing_reviews 
                          if r['Status'] in ['Scheduled', 'In Progress']}
    
    projects_to_assign = [p for p in projects_needing_review 
                          if p['Project_ID'] not in active_project_ids]
    
    # Assign reviewers
    new_assignments = []
    for project in projects_to_assign:
        review = assign_reviewer(project, users)
        if review:  # ✅ Only if a reviewer was successfully assigned
            new_assignments.append(review)
    
    return {
        'total_assigned': len(new_assignments),
        'total_needing_review': len(projects_needing_review),
        'already_assigned': len(projects_needing_review) - len(projects_to_assign),
        'assignments': new_assignments
    }
    
    


# In[82]:


# ===============================================================================
# Notification System
# ===============================================================================

def send_notifications(status_filter=None, smtp_server='localhost', smtp_port=587, 
                      smtp_user=None, smtp_password=None, sender_email='scheduler@example.com'):
    """
    Send email notifications to reviewers for their assigned reviews.
    
    Args:
        status_filter (str, optional): Filter projects by status ('Overdue', 'Due Soon')
        smtp_server (str): SMTP server address
        smtp_port (int): SMTP server port
        smtp_user (str, optional): SMTP username
        smtp_password (str, optional): SMTP password
        sender_email (str): Sender email address
        
    Returns:
        dict: Summary of notification results
    """
    # Read necessary data
    projects = get_all_projects()
    
    # Filter projects if needed
    if status_filter:
        projects = [p for p in projects if p.get('Status') == status_filter]
    
    sent_count = 0
    failed_count = 0
    notification_log = []
    
    # Process each project
    for project in projects:
        # Get associated reviews
        reviews = get_reviews_by_project(project['Project_ID'])
        
        # Filter reviews that are scheduled or in progress
        active_reviews = [r for r in reviews if r['Status'] in ['Scheduled', 'In Progress']]
        
        for review in active_reviews:
            # Get reviewer information
            reviewer = get_reviewer(review['Reviewer_ID'])
            
            if not reviewer or not reviewer.get('Email'):
                notification_log.append({
                    'project_id': project['Project_ID'],
                    'review_id': review['Review_ID'],
                    'status': 'Failed',
                    'reason': 'Missing reviewer or email'
                })
                failed_count += 1
                continue
            
            try:
                # Prepare email content
                msg = EmailMessage()
                
                # Set subject with urgency prefix if overdue
                subject = project['Project_Name'] + ' - Review Required'
                if project.get('Status') == 'Overdue':
                    subject = '[URGENT] ' + subject
                
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = reviewer['Email']
                
                # Create email body
                body = f"""
                Dear {reviewer['Name']},
                
                You have been assigned to review the following project:
                
                Project: {project['Project_Name']}
                Project ID: {project['Project_ID']}
                Scheduled Date: {review['Scheduled_Date']}
                Status: {project.get('Status', '')}
                
                """
                
                if project.get('Status') == 'Overdue':
                    body += "This review is OVERDUE and requires immediate attention.\n"
                elif project.get('Status') == 'Due Soon':
                    body += "This review is due soon. Please prioritize accordingly.\n"
                
                body += """
                Please complete your review by the scheduled date.
                
                Thank you,
                Project Review Scheduler
                """
                
                msg.set_content(body)
                
                # In a production environment, we would send the email here
                # For testing/development, we'll simulate this
                if smtp_server == 'localhost':
                    # Simulate email sending for testing
                    print(f"Email would be sent to {reviewer['Email']}")
                else:
                    # Actually send the email
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        if smtp_user and smtp_password:
                            server.login(smtp_user, smtp_password)
                        server.send_message(msg)
                
                notification_log.append({
                    'project_id': project['Project_ID'],
                    'review_id': review['Review_ID'],
                    'reviewer_email': reviewer['Email'],
                    'status': 'Sent',
                    'subject': subject
                })
                sent_count += 1
                
            except Exception as e:
                notification_log.append({
                    'project_id': project['Project_ID'],
                    'review_id': review['Review_ID'],
                    'status': 'Failed',
                    'reason': str(e)
                })
                failed_count += 1
    
    return {
        'sent': sent_count,
        'failed': failed_count,
        'total': sent_count + failed_count,
        'log': notification_log
    }


# In[84]:


# ===============================================================================
# Reporting Module
# ===============================================================================

def generate_monthly_schedule(month, year, output_file=None):
    """
    Generate a monthly schedule of upcoming reviews.
    
    Args:
        month (str): Month to generate schedule for (format: MM)
        year (str): Year to generate schedule for (format: YYYY)
        output_file (str, optional): Path to output file. If None, uses default naming.
        
    Returns:
        dict: Report generation results
    """
    # Read data
    reviews = get_all_reviews()
    
    # Build full review data with project and reviewer info
    enriched_reviews = []
    for review in reviews:
        # Only include scheduled and in-progress reviews
        if review['Status'] not in ['Scheduled', 'In Progress']:
            continue
        
        # Check if the review is in the specified month/year
        review_date = datetime.strptime(review['Scheduled_Date'], '%Y-%m-%d')
        if review_date.strftime('%m') != month or review_date.strftime('%Y') != year:
            continue
        
        # Get project and reviewer info
        project = next((p for p in get_all_projects() if p['Project_ID'] == review['Project_ID']), {})
        reviewer = get_reviewer(review['Reviewer_ID'])
        
        # Create enriched review record
        enriched_review = {
            'Review_ID': review['Review_ID'],
            'Project_ID': review['Project_ID'],
            'Project_Name': project.get('Project_Name', 'Unknown'),
            'Reviewer_ID': review['Reviewer_ID'],
            'Reviewer_Name': reviewer.get('Name', 'Unknown') if reviewer else 'Unknown',
            'Scheduled_Date': review['Scheduled_Date'],
            'Status': review['Status']
        }
        
        enriched_reviews.append(enriched_review)
    
    # Sort by scheduled date
    enriched_reviews.sort(key=lambda r: r['Scheduled_Date'])
    
    # Define output file name if not specified
    if output_file is None:
        output_file = f"monthly_schedule_{month}-{year}.csv"
    
    # Define fields for the report
    fieldnames = [
        'Project_ID', 'Project_Name', 'Reviewer_Name', 'Scheduled_Date', 'Status'
    ]
    
    # Write report to CSV
    if enriched_reviews:
        write_csv(output_file, enriched_reviews, fieldnames)
    
    return {
        'file': output_file,
        'month': month,
        'year': year,
        'review_count': len(enriched_reviews)
    }

def generate_workload_report(output_file=None):
    """
    Generate a report showing workload distribution among reviewers.
    
    Args:
        output_file (str, optional): Path to output file. If None, uses default naming.
        
    Returns:
        dict: Report generation results
    """
    # Read data
    users = get_all_users()
    reviews = get_all_reviews()
    
    # Count active reviews per reviewer
    workloads = {}
    for user in users:
        user_id = user['User_ID']
        active_reviews = [r for r in reviews 
                          if r['Reviewer_ID'] == user_id and 
                          r['Status'] in ['Scheduled', 'In Progress']]
        workloads[user_id] = {
            'User_ID': user_id,
            'Name': user['Name'],
            'Department': user.get('Department', 'Unknown'),
            'Current_Load': len(active_reviews),
            'Active_Reviews': [r['Review_ID'] for r in active_reviews]
        }
    
    # Sort by current load (descending)
    sorted_workloads = sorted(workloads.values(), key=lambda w: w['Current_Load'], reverse=True)
    
    # Define output file name if not specified
    if output_file is None:
        output_file = f"workload_report_{datetime.now().strftime('%Y%m%d')}.csv"
    
    # Define fields for the report
    fieldnames = ['User_ID', 'Name', 'Department', 'Current_Load', "Current_Load", "Active_Reviews"]
    
    # Write report to CSV
    write_csv(output_file, sorted_workloads, fieldnames)
    
    # Generate visualization
    plt.figure(figsize=(10, 6))
    plt.bar([w['Name'] for w in sorted_workloads], [w['Current_Load'] for w in sorted_workloads])
    plt.xlabel('Reviewer')
    plt.ylabel('Active Reviews')
    plt.title('Reviewer Workload Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save chart
    chart_file = output_file.replace('.csv', '.png')
    plt.savefig(chart_file)
    
    return {
        'file': output_file,
        'chart': chart_file,
        'reviewer_count': len(sorted_workloads),
        'total_reviews': sum(w['Current_Load'] for w in sorted_workloads)
    }

def generate_overdue_alerts(output_file=None):
    """
    Generate alerts for overdue reviews.
    
    Args:
        output_file (str, optional): Path to output file. If None, uses default naming.
        
    Returns:
        dict: Report generation results
    """
    # Read data
    projects = get_all_projects()
    
    # Filter overdue projects
    overdue_projects = [p for p in projects if p.get('Status') == 'Overdue']
    
    # Sort by next review date (oldest first)
    overdue_projects.sort(key=lambda p: p.get('Next_Review_Date', ''))
    
    # Enrich with reviewer information
    enriched_overdue = []
    for project in overdue_projects:
        reviews = get_reviews_by_project(project['Project_ID'])
        active_reviews = [r for r in reviews if r['Status'] in ['Scheduled', 'In Progress']]
        
        if active_reviews:
            review = active_reviews[0]  # Take the first active review
            reviewer = get_reviewer(review['Reviewer_ID'])
            reviewer_name = reviewer.get('Name', 'Unknown') if reviewer else 'Unknown'
            next_review = datetime.strptime(project['Next_Review_Date'], '%Y-%m-%d')
            days_overdue = (datetime.now() - next_review).days

        else:
            reviewer_name = 'No reviewer assigned'
            days_overdue = 0
        
        enriched_project = {
            'Project_ID': project['Project_ID'],
            'Project_Name': project['Project_Name'],
            'Department': project.get('Department', 'Unknown'),
            'Next_Review_Date': project.get('Next_Review_Date', ''),
            'Days_Overdue': days_overdue,
            'Reviewer_Name': reviewer_name
        }
        
        enriched_overdue.append(enriched_project)
           # Define output file name if not specified
    if output_file is None:
        output_file = f"overdue_alerts_{datetime.now().strftime('%Y%m%d')}.csv"
    
    # Define fields for the report
    fieldnames = ['Project_ID', 'Project_Name', 'Department', 'Next_Review_Date', 'Days_Overdue', 'Reviewer_Name']
    
    # Write report to CSV
    if enriched_overdue:
        write_csv(output_file, enriched_overdue, fieldnames)
    
    return {
        'file': output_file,
        'overdue_count': len(enriched_overdue),
        'projects': [p['Project_ID'] for p in enriched_overdue]
    }

def generate_all_reports():
    """
    Generate all standard reports.
    
    Returns:
        dict: Summary of all report generation results
    """
    # Current date for filenames and monthly report
    current_date = datetime.now()
    current_month = current_date.strftime('%m')
    current_year = current_date.strftime('%Y')
    
    # Generate reports
    monthly_result = generate_monthly_schedule(current_month, current_year)
    workload_result = generate_workload_report()
    overdue_result = generate_overdue_alerts()
    
    return {
        'monthly_schedule': monthly_result,
        'workload_report': workload_result,
        'overdue_alerts': overdue_result,
        'timestamp': current_date.strftime('%Y-%m-%d %H:%M:%S')
    }


# In[86]:


# ===============================================================================
# Command Line Interface
# ===============================================================================

def parse_args(args):
    """
    Parse command line arguments.
    
    Args:
        args (list): List of command line arguments
        
    Returns:
        dict: Parsed arguments
    """
    if not args or len(args) < 1:
        return {'command': 'help'}
    
    command = args[0]
    parsed = {'command': command}
    
    # Parse command-specific arguments
    if command == 'calculate_reviews':
        for i in range(1, len(args)):
            if args[i] == '--csv' and i + 1 < len(args):
                parsed['csv_file'] = args[i + 1]
    
    elif command == 'assign_reviewers':
        for i in range(1, len(args)):
            if args[i] == '--projects' and i + 1 < len(args):
                parsed['projects_file'] = args[i + 1]
            elif args[i] == '--users' and i + 1 < len(args):
                parsed['users_file'] = args[i + 1]
            elif args[i] == '--reviews' and i + 1 < len(args):
                parsed['reviews_file'] = args[i + 1]
    
    elif command == 'send_notifications':
        for i in range(1, len(args)):
            if args[i] == '--status' and i + 1 < len(args):
                parsed['status'] = args[i + 1]
            elif args[i] == '--smtp-server' and i + 1 < len(args):
                parsed['smtp_server'] = args[i + 1]
            elif args[i] == '--smtp-port' and i + 1 < len(args):
                parsed['smtp_port'] = int(args[i + 1])


    elif command == 'generate_reports':
        for i in range(1, len(args)):
            if args[i] == '--type' and i + 1 < len(args):
                parsed['report_type'] = args[i + 1]
            elif args[i] == '--month' and i + 1 < len(args):
                parsed['month'] = args[i + 1]
            elif args[i] == '--year' and i + 1 < len(args):
                parsed['year'] = args[i + 1]
            elif args[i] == '--output' and i + 1 < len(args):
                parsed['output_file'] = args[i + 1]
    
    return parsed
    
def parse_args(args):
    parsed = {}

    if not args:
        parsed["command"] = "help"
        return parsed

    parsed["command"] = args[0]

    for i in range(1, len(args)):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                parsed[key] = args[i + 1]
            else:
                parsed[key] = True  # flag-style

    return parsed

def execute_command(args):
    """
    Execute a command based on parsed arguments.

    Args:
        args (list): List of command line arguments

    Returns:
        dict: Command execution results
    """
    parsed_args = parse_args(args)
    print(f"DEBUG: parsed_args = {parsed_args}")
    command = parsed_args.get('command')
    print("DEBUG: command =", command)  

    if command == 'help':
        print("Project Review Scheduler - Command Line Interface\n")
        print("Available commands:")
        print("  calculate_reviews [--csv PROJECTS_FILE]")
        print("      Calculate review due dates for all projects")
        print("  assign_reviewers [--projects PROJECTS_FILE] [--users USERS_FILE] [--reviews REVIEWS_FILE]")
        print("      Assign reviewers to projects needing review")
        print("  send_notifications [--status STATUS] [--smtp-server SERVER] [--smtp-port PORT]")
        print("      Send email notifications to reviewers")
        print("  generate_reports [--type REPORT_TYPE] [--month MONTH] [--year YEAR] [--output OUTPUT_FILE]")
        print("      Generate reports. REPORT_TYPE can be 'monthly', 'workload', 'overdue', or 'all'")
        return {'success': True, 'command': 'help'}

    elif command == 'calculate_reviews':
        csv_file = parsed_args.get('csv_file', 'Projects.csv')

        result = calculate_all_reviews(csv_file)

        print(f"Review calculations completed successfully")
        print(f"Total projects: {result['total_projects']}")
        print(f"Overdue: {result['overdue']}")
        print(f"Due Soon: {result['due_soon']}")
        print(f"Up to Date: {result['up_to_date']}")

        return {'success': True, 'command': 'calculate_reviews', 'result': result}

    elif command == 'assign_reviewers':
        projects_file = parsed_args.get('projects_file', 'Projects.csv')
        users_file = parsed_args.get('users_file', 'Users.csv')
        reviews_file = parsed_args.get('reviews_file', 'Reviews.csv')

        result = assign_all_reviewers(projects_file, users_file, reviews_file)

        print(f"Reviewer assignments completed successfully")
        print(f"Projects needing review: {result['total_needing_review']}")
        print(f"Projects already assigned: {result['already_assigned']}")
        print(f"New assignments created: {result['total_assigned']}")

        return {'success': True, 'command': 'assign_reviewers', 'result': result}

    elif command == 'send_notifications':
        status = parsed_args.get('status')
        smtp_server = parsed_args.get('smtp_server', 'localhost')
        smtp_port = parsed_args.get('smtp_port', 587)

        result = send_notifications(status, smtp_server, smtp_port)

        print(f"Notification process completed")
        print(f"Total notifications: {result['total']}")
        print(f"Successfully sent: {result['sent']}")
        print(f"Failed: {result['failed']}")
        if result["sent"] > 0:
           print("\nEmails Sent:")
           for log in result["log"]:
              print(f"- To: {log['reviewer_email']} | Subject: {log['subject']} | Status: {log['status']}")
        else:
           print("No emails were sent.")
           return {'success': True, 'command': 'send_notifications', 'result': result}

    elif command == 'generate_reports':
        report_type = parsed_args.get('report_type', 'all')

        if report_type == 'all':
            result = generate_all_reports()

            print(f"All reports generated successfully")
            print(f"Monthly schedule: {result['monthly_schedule']['file']} ({result['monthly_schedule']['review_count']} reviews)")
            print(f"Workload report: {result['workload_report']['file']} ({result['workload_report']['reviewer_count']} reviewers)")
            print(f"Overdue alerts: {result['overdue_alerts']['file']} ({result['overdue_alerts']['overdue_count']} overdue projects)")

            return {'success': True, 'command': 'generate_reports', 'result': result}

        elif report_type == 'monthly':
            month = parsed_args.get('month', datetime.now().strftime('%m'))
            year = parsed_args.get('year', datetime.now().strftime('%Y'))
            output_file = parsed_args.get('output_file')

            result = generate_monthly_schedule(month, year, output_file)

            print(f"Monthly schedule generated successfully")
            print(f"File: {result['file']}")
            print(f"Reviews: {result['review_count']}")

            return {'success': True, 'command': 'generate_reports', 'report_type': 'monthly', 'result': result}

        elif report_type == 'workload':
            output_file = parsed_args.get('output_file')

            result = generate_workload_report(output_file)

            print(f"Workload report generated successfully")
            print(f"File: {result['file']}")
            print(f"Chart: {result['chart']}")
            print(f"Reviewers: {result['reviewer_count']}")
            print(f"Total active reviews: {result['total_reviews']}")

            return {'success': True, 'command': 'generate_reports', 'report_type': 'workload', 'result': result}

        elif report_type == 'overdue':
            output_file = parsed_args.get('output_file')

            result = generate_overdue_alerts(output_file)

            print(f"Overdue alerts generated successfully")
            print(f"File: {result['file']}")
            print(f"Overdue projects: {result['overdue_count']}")

            return {'success': True, 'command': 'generate_reports', 'report_type': 'overdue', 'result': result}

        else:
            print(f"Error: Unknown report type '{report_type}'")
            return {'success': False, 'command': 'generate_reports', 'error': f"Unknown report type '{report_type}'"}

    else:
        print(f"Error: Unknown command '{command}'")
        return {'success': False, 'command': 'unknown', 'error': f"Unknown command '{command}'"}






# In[88]:


# ===============================================================================
# Main Entry Point
# ===============================================================================

def main():
    """
    Main entry point for the command line interface.
    Filters out Jupyter and IDE internal arguments.
    """
    import sys

    print("RAW sys.argv =", sys.argv)  

    # Filter out known unwanted args like '-f' or kernel specs
    filtered_args = [
        arg for arg in sys.argv[1:]
        if not arg.endswith(".json") and not arg.startswith("-f") and not arg.startswith('--Application')
    ]

    print("Project Review Scheduler module loaded successfully")
    execute_command(filtered_args)


if __name__ == '__main__':
    main()



# In[98]:


from dateutil.relativedelta import relativedelta
import pandas as pd

def calculate_due_dates(projects_df):
    # Ensure 'Start_Date' is in datetime format
    projects_df['Start_Date'] = pd.to_datetime(projects_df['Start_Date'], errors='coerce')

    # Convert frequency from years to months
    def calculate_for_project(row):
        # Last review date (Start Date of the project)
        last_review = row['Start_Date']
        
        # Frequency in years (convert it to months)
        frequency_years = row['Review_Frequency_Years']
        frequency_months = int(frequency_years * 12)  # Convert years to months
        
        # Add the calculated months to the last review date using relativedelta
        next_review = last_review + relativedelta(months=frequency_months)
        
        # Return updated values
        return pd.Series({
            'Next_Review_Date': next_review,  # Store as datetime
        })
    
    # Apply the function to each row in the DataFrame
    projects_df[['Next_Review_Date']] = projects_df.apply(calculate_for_project, axis=1)

    return projects_df


def assign_reviewers(projects_df, users_df):
    # Example function to assign reviewers based on department or load
    assignments = []
    for i, project in projects_df.iterrows():
        # Simple logic to assign the first available reviewer
        available_reviewer = users_df.sample(1).iloc[0]  # Randomly choose a reviewer
        assignments.append({
            "Project_ID": project["Project_ID"],
            "Reviewer_ID": available_reviewer["User_ID"],
            "Reviewer_Name": available_reviewer["Name"]
        })
    return pd.DataFrame(assignments)

# --------------- Streamlit App UI ---------------
# Title of the app
st.title('Project Review Scheduler')

# Instructions
st.write('This app helps to automate project review scheduling and reviewer assignments.')

# File uploader for CSV files
users_file = st.file_uploader("Upload Users CSV", type=["csv"])
projects_file = st.file_uploader("Upload Projects CSV", type=["csv"])
reviews_file = st.file_uploader("Upload Reviews CSV", type=["csv"])

if users_file and projects_file and reviews_file:
    # Load CSV files
    users_df = pd.read_csv(users_file)
    projects_df = pd.read_csv(projects_file)
    reviews_df = pd.read_csv(reviews_file)

    st.write("Data loaded successfully!")

    # Display loaded data for review
    st.write("Users Data:")
    st.write(users_df.head())

    st.write("Projects Data:")
    st.write(projects_df.head())

    st.write("Reviews Data:")
    st.write(reviews_df.head())

    # Trigger functions via buttons
    if st.button('Calculate Review Due Dates'):
        projects_df = calculate_due_dates(projects_df)
        st.write('Review due dates calculated:')
        st.write(projects_df[['Project_ID', 'Next_Review_Date']])

    if st.button('Assign Reviewers'):
        assignments_df = assign_reviewers(projects_df, users_df)
        st.write('Reviewers assigned:')
        st.write(assignments_df)

else:
    st.write("Please upload the CSV files to proceed.")


# In[ ]:




