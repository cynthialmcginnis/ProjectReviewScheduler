#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Title of the app
st.title('Project Review Scheduler')

# Instructions
st.write('This app helps to automate project review scheduling and reviewer assignments.')

# File uploader for CSV files (ONLY Users and Projects needed)
users_file = st.file_uploader("Upload Users CSV", type=["csv"])
projects_file = st.file_uploader("Upload Projects CSV", type=["csv"])

def calculate_due_dates(projects_df, current_date=None):
    """
    Calculate the next review date based on the project's start date and review frequency.
    
    Args:
        projects_df (DataFrame): A dataframe containing project details
        current_date (datetime, optional): The current date to compare
    
    Returns:
        DataFrame: Updated project data with Next_Review_Date and Status fields
    """
    if current_date is None:
        current_date = datetime.now()
    
    # Make a copy to avoid modifying the original
    projects_df = projects_df.copy()
    
    # Ensure Start_Date is in datetime format
    projects_df['Start_Date'] = pd.to_datetime(projects_df['Start_Date'], errors='coerce')
    
    def calculate_for_project(row):
        # Last review date (Start Date of the project)
        last_review = row['Start_Date']
        
        # Frequency in years
        frequency_years = row['Review_Frequency_Years']
        
        # Convert frequency in years to months (12 months per year)
        frequency_months = int(frequency_years * 12)
        
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
            'Next_Review_Date': next_review,
            'Status': status,
            'Days_Until_Review': days_until_review
        })
    
    # Apply the function to each row in the DataFrame
    projects_df[['Next_Review_Date', 'Status', 'Days_Until_Review']] = projects_df.apply(calculate_for_project, axis=1)
    
    return projects_df

def create_enhanced_reviews_csv(projects_df, users_df):
    """
    Create an enhanced Reviews.csv with project names, due dates, and comprehensive reviewer information.
    
    Args:
        projects_df (DataFrame): Projects with calculated due dates and status
        users_df (DataFrame): Available reviewers
    
    Returns:
        DataFrame: Enhanced reviews data with all relevant information
    """
    reviews = []
    
    # Filter projects that need review
    projects_needing_review = projects_df[
        projects_df['Status'].isin(['Overdue', 'Due Soon'])
    ].copy()
    
    if len(projects_needing_review) == 0:
        return pd.DataFrame(columns=[
            'Review_ID', 'Project_ID', 'Project_Name', 'Project_Department', 
            'Next_Review_Date', 'Project_Status', 'Days_Until_Review',
            'Reviewer_ID', 'Reviewer_Name', 'Reviewer_Email', 'Reviewer_Department',
            'Scheduled_Date', 'Review_Status', 'Completion_Date'
        ])
    
    # Convert Current_Load to numeric, defaulting to 0 if missing
    users_df = users_df.copy()
    users_df['Current_Load'] = pd.to_numeric(users_df.get('Current_Load', 0), errors='coerce').fillna(0)
    
    for i, project in projects_needing_review.iterrows():
        project_dept = project.get('Department', '')
        
        # Try to find reviewers from different departments first
        other_dept_reviewers = users_df[users_df['Department'] != project_dept]
        
        if len(other_dept_reviewers) > 0:
            # Choose reviewer with lowest workload from other departments
            available_reviewer = other_dept_reviewers.loc[other_dept_reviewers['Current_Load'].idxmin()]
        else:
            # Fallback: choose reviewer with lowest workload from any department
            available_reviewer = users_df.loc[users_df['Current_Load'].idxmin()]
        
        # Update the workload for the next assignment
        users_df.loc[users_df['User_ID'] == available_reviewer['User_ID'], 'Current_Load'] += 1
        
        # Create enhanced review record with all relevant information
        review_id = f"R{datetime.now().strftime('%Y%m%d')}{i:03d}"
        scheduled_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')  # Schedule for next week
        
        reviews.append({
            # Review Information
            'Review_ID': review_id,
            'Scheduled_Date': scheduled_date,
            'Review_Status': 'Scheduled',
            'Completion_Date': '',
            
            # Project Information
            'Project_ID': project['Project_ID'],
            'Project_Name': project.get('Project_Name', 'Unknown'),
            'Project_Department': project.get('Department', 'Unknown'),
            'Next_Review_Date': project['Next_Review_Date'].strftime('%Y-%m-%d') if pd.notna(project['Next_Review_Date']) else '',
            'Project_Status': project['Status'],
            'Days_Until_Review': project.get('Days_Until_Review', 0),
            
            # Reviewer Information
            'Reviewer_ID': available_reviewer['User_ID'],
            'Reviewer_Name': available_reviewer['Name'],
            'Reviewer_Email': available_reviewer.get('Email', ''),
            'Reviewer_Department': available_reviewer.get('Department', 'Unknown'),
        })
    
    return pd.DataFrame(reviews)

def create_simple_reviews_csv(enhanced_reviews_df):
    """
    Create a simplified Reviews.csv with just the core fields for system processing.
    
    Args:
        enhanced_reviews_df (DataFrame): Enhanced reviews data
    
    Returns:
        DataFrame: Simplified reviews data
    """
    if len(enhanced_reviews_df) == 0:
        return pd.DataFrame(columns=['Review_ID', 'Project_ID', 'Reviewer_ID', 'Scheduled_Date', 'Status', 'Completion_Date'])
    
    simple_reviews = enhanced_reviews_df[[
        'Review_ID', 'Project_ID', 'Reviewer_ID', 'Scheduled_Date', 'Review_Status', 'Completion_Date'
    ]].copy()
    
    # Rename Review_Status to Status for compatibility
    simple_reviews = simple_reviews.rename(columns={'Review_Status': 'Status'})
    
    return simple_reviews

# Main app logic - ONLY requires Users and Projects CSV
if users_file and projects_file:
    try:
        # Load CSV files
        users_df = pd.read_csv(users_file)
        projects_df = pd.read_csv(projects_file)
        
        st.success("Data loaded successfully!")
        
        # Display loaded data for review
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("View Users Data"):
                st.dataframe(users_df)
                st.write(f"**Total Users:** {len(users_df)}")
        
        with col2:
            with st.expander("View Projects Data"):
                st.dataframe(projects_df)
                st.write(f"**Total Projects:** {len(projects_df)}")
        
        # Buttons for actions
        st.subheader("Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button('Calculate Review Due Dates', type="primary"):
                with st.spinner('Calculating due dates...'):
                    try:
                        updated_projects = calculate_due_dates(projects_df)
                        st.success('Review due dates calculated!')
                        
                        # Show summary statistics
                        st.subheader("Status Summary")
                        status_counts = updated_projects['Status'].value_counts()
                        
                        # Create columns for status display
                        status_cols = st.columns(len(status_counts))
                        for i, (status, count) in enumerate(status_counts.items()):
                            with status_cols[i]:
                                st.metric(label=status, value=count)
                        
                        # Show detailed results
                        st.subheader("Updated Projects")
                        display_cols = ['Project_ID', 'Project_Name', 'Department', 'Next_Review_Date', 'Status', 'Days_Until_Review']
                        available_cols = [col for col in display_cols if col in updated_projects.columns]
                        st.dataframe(updated_projects[available_cols])
                        
                        # Download option
                        csv = updated_projects.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Updated Projects CSV",
                            data=csv,
                            file_name=f"updated_projects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                        
                        # Store in session state for reviewer assignment
                        st.session_state['updated_projects'] = updated_projects
                        
                    except Exception as e:
                        st.error(f"Error calculating due dates: {str(e)}")
        
        with col2:
            if st.button('Assign Reviewers & Generate Reviews', type="secondary"):
                with st.spinner('Assigning reviewers and generating Reviews.csv...'):
                    try:
                        # Use updated projects if available, otherwise calculate first
                        if 'updated_projects' in st.session_state:
                            projects_for_assignment = st.session_state['updated_projects']
                        else:
                            projects_for_assignment = calculate_due_dates(projects_df)
                        
                        # Create Enhanced Reviews.csv with project names and due dates
                        enhanced_reviews_df = create_enhanced_reviews_csv(projects_for_assignment, users_df)
                        
                        if len(enhanced_reviews_df) > 0:
                            st.success(f'✅ Reviews generated with {len(enhanced_reviews_df)} assignments!')
                            
                            # Show assignment summary
                            st.subheader("Assignment Summary")
                            overdue_count = len(enhanced_reviews_df[enhanced_reviews_df['Project_Status'] == 'Overdue'])
                            due_soon_count = len(enhanced_reviews_df[enhanced_reviews_df['Project_Status'] == 'Due Soon'])
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Total Assignments", len(enhanced_reviews_df))
                            with col_b:
                                st.metric("Overdue Projects", overdue_count)
                            with col_c:
                                st.metric("Due Soon Projects", due_soon_count)
                            
                            # Show enhanced reviews with project names and due dates
                            st.subheader("Generated Reviews (with Project Names & Due Dates)")
                            
                            # Display key columns for easy viewing
                            display_columns = [
                                'Review_ID', 'Project_Name', 'Project_Status', 'Next_Review_Date',
                                'Reviewer_Name', 'Reviewer_Department', 'Scheduled_Date'
                            ]
                            available_display = [col for col in display_columns if col in enhanced_reviews_df.columns]
                            st.dataframe(enhanced_reviews_df[available_display])
                            
                            # Create simple Reviews.csv for system compatibility
                            simple_reviews_df = create_simple_reviews_csv(enhanced_reviews_df)
                            
                            # Download options
                            col_d1, col_d2 = st.columns(2)
                            
                            with col_d1:
                                # Download Enhanced Reviews.csv (with project names and due dates)
                                enhanced_csv = enhanced_reviews_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Enhanced Reviews.csv",
                                    data=enhanced_csv,
                                    file_name=f"Enhanced_Reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    help="Complete reviews file with project names, due dates, and reviewer details"
                                )
                            
                            with col_d2:
                                # Download Simple Reviews.csv (for system processing)
                                simple_csv = simple_reviews_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Simple Reviews.csv",
                                    data=simple_csv,
                                    file_name=f"Reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    help="Standard format for system processing"
                                )
                            
                            # Show what's included in each file
                            with st.expander("📋 What's included in each file"):
                                st.write("**Enhanced Reviews.csv includes:**")
                                st.write("- Project names and departments")
                                st.write("- Due dates and status")
                                st.write("- Complete reviewer information")
                                st.write("- Days until review")
                                
                                st.write("**Simple Reviews.csv includes:**")
                                st.write("- Core fields for system processing")
                                st.write("- Review_ID, Project_ID, Reviewer_ID")
                                st.write("- Scheduled_Date, Status, Completion_Date")
                            
                        else:
                            st.info("✅ No projects currently need review assignments. All projects are up to date!")
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"Error assigning reviewers: {str(e)}")
    
    except Exception as e:
        st.error(f"Error loading CSV files: {str(e)}")
        st.info("Please make sure your CSV files have the correct format and encoding.")

else:
    st.info("Please upload both Users and Projects CSV files to get started.")
    
    # Show expected file formats
    with st.expander(" Expected CSV File Formats"):
        st.subheader("Users CSV Format")
        st.code("""User_ID,Name,Email,Department,Current_Load
U001,John Doe,john@example.com,Engineering,0
U002,Jane Smith,jane@example.com,Marketing,1""", language="csv")
        
        st.subheader("Projects CSV Format")  
        st.code("""Project_ID,Project_Name,Start_Date,Review_Frequency_Years,Department
P001,Website Redesign,2023-01-15,1.0,Engineering
P002,Marketing Campaign,2023-03-20,0.5,Marketing""", language="csv")
        
        st.info("""
        **How it works:**
        1. Upload your Users.csv and Projects.csv files
        2. Click 'Calculate Review Due Dates' to see which projects need review
        3. Click 'Assign Reviewers & Generate Reviews' to create comprehensive Reviews.csv files
        4. Download either the Enhanced Reviews.csv (with project names & due dates) or Simple Reviews.csv
        """)

# Add footer information
st.markdown("---")
st.markdown("""
**Enhanced Features:**
-  **Enhanced Reviews.csv** includes project names, due dates, and complete reviewer information
-  **Simple Reviews.csv** provides standard format for system processing
-  **Smart assignment** balances workload and prefers cross-department reviews
""")


# In[ ]:




