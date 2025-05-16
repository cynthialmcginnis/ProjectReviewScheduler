#!/usr/bin/env python
# coding: utf-8

# In[2]:


from faker import Faker
import csv
import os
import random
from datetime import datetime, timedelta
from scheduler import calculate_all_reviews, assign_all_reviewers

fake = Faker()

departments = ['Engineering', 'QA', 'HR', 'Finance', 'IT']

def generate_fake_users(num=10):
    users = []
    for i in range(num):
        users.append({
            "User_ID": f"U{i+1:03}",
            "Name": fake.name(),
            "Email": fake.email(),
            "Department": random.choice(departments),
            "Current_Load": random.randint(0, 3)
        })
    return users

def generate_fake_projects(num=25):
    projects = []
    for i in range(num):
        start_date = fake.date_between(start_date='-2y', end_date='-1y')
        last_review = fake.date_between(start_date=start_date, end_date='-6m')
        frequency = random.choice([1, 2])
        next_review = datetime.strptime(str(last_review), "%Y-%m-%d") + timedelta(days=frequency * 365)
        status = "Overdue" if next_review < datetime.now() else "Due Soon"

        projects.append({
            "Project_ID": f"P{i+1:03}",
            "Project_Name": fake.bs().title(),
            "Start_Date": str(start_date),
            "Last_Review_Date": str(last_review),
            "Review_Frequency_Years": frequency,
            "Department": random.choice(departments),
            "Status": status,
            "Next_Review_Date": str(next_review.date())
        })
    return projects

def write_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def reset_all():
    print("🔁 Resetting CSV files...")

    users = generate_fake_users()
    projects = generate_fake_projects()

    write_csv("Users.csv", users, ["User_ID", "Name", "Email", "Department", "Current_Load"])
    write_csv("Projects.csv", projects, [
        "Project_ID", "Project_Name", "Start_Date", "Last_Review_Date",
        "Review_Frequency_Years", "Department", "Status", "Next_Review_Date"
    ])
    write_csv("Reviews.csv", [], ["Review_ID", "Project_ID", "Reviewer_ID", "Scheduled_Date", "Status", "Completion_Date"])

    print("✅ Fake data created.")
    calculate_all_reviews("Projects.csv")
    assign_all_reviewers("Projects.csv", "Users.csv", "Reviews.csv")
    print("🎯 Review assignments complete.")

if __name__ == "__main__":
    reset_all()


# In[ ]:




