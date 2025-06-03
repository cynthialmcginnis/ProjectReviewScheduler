#!/usr/bin/env python
# coding: utf-8

"""
Universal Project Review Analytics Dashboard
Can be used by anyone with CSV files or auto-detect files in current directory
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import glob

# Configure Streamlit page
st.set_page_config(
    page_title="Project Review Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'regenerate_reviews' not in st.session_state:
    st.session_state.regenerate_reviews = False

# Custom CSS for better styling
st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Project Review Analytics Dashboard</h1>
    <p>Universal dashboard for project review analytics - works with any CSV files!</p>
</div>
""", unsafe_allow_html=True)

def auto_detect_csv_files():
    """Auto-detect CSV files in current directory"""
    csv_files = glob.glob("*.csv")
    detected_files = {}
    
    for file in csv_files:
        filename_lower = file.lower()
        if 'user' in filename_lower:
            detected_files['users'] = file
        elif 'project' in filename_lower:
            detected_files['projects'] = file
        elif 'review' in filename_lower:
            detected_files['reviews'] = file
    
    return detected_files

def validate_csv_structure(df, expected_columns, file_type):
    """Validate that CSV has expected columns"""
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        st.error(f"❌ {file_type} file is missing required columns: {missing_columns}")
        st.info(f"Required columns for {file_type}: {expected_columns}")
        return False
    return True

def generate_realistic_reviews(users_df, projects_df):
    """Generate realistic review data based on users and projects"""
    import random
    from datetime import datetime, timedelta
    
    reviews = []
    
    # Create multiple reviews per project for realism
    for _, project in projects_df.iterrows():
        # Determine number of reviews based on project status
        if project['Status'] == 'Overdue':
            num_reviews = random.randint(1, 3)  # Overdue projects might have multiple reviews
        elif project['Status'] == 'Due Soon':
            num_reviews = random.randint(1, 2)
        else:
            num_reviews = 1
        
        for review_num in range(num_reviews):
            # Smart reviewer assignment
            # Try to assign reviewers from different departments for cross-departmental review
            other_dept_reviewers = users_df[users_df['Department'] != project['Department']]
            
            if not other_dept_reviewers.empty and random.random() > 0.3:  # 70% chance of cross-dept assignment
                reviewer = other_dept_reviewers.sample(1).iloc[0]
            else:
                reviewer = users_df.sample(1).iloc[0]
            
            # Generate realistic dates and statuses
            base_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            # Status distribution based on project status
            if project['Status'] == 'Overdue':
                status_options = ['Overdue', 'In Progress', 'Scheduled']
                weights = [0.5, 0.3, 0.2]
            elif project['Status'] == 'Due Soon':
                status_options = ['In Progress', 'Scheduled', 'Completed']
                weights = [0.4, 0.4, 0.2]
            else:  # Up to Date
                status_options = ['Completed', 'In Progress', 'Scheduled']
                weights = [0.6, 0.2, 0.2]
            
            status = random.choices(status_options, weights=weights)[0]
            
            # Generate dates based on status
            if status == 'Completed':
                scheduled_date = base_date
                completion_date = scheduled_date + timedelta(days=random.randint(1, 14))
            elif status == 'Overdue':
                scheduled_date = base_date - timedelta(days=random.randint(1, 30))
                completion_date = None
            else:  # In Progress or Scheduled
                scheduled_date = base_date + timedelta(days=random.randint(-5, 15))
                completion_date = None
            
            review_id = f"R{len(reviews) + 1:03d}"
            
            reviews.append({
                'Review_ID': review_id,
                'Project_ID': project['Project_ID'],
                'Reviewer_ID': reviewer['User_ID'],
                'Status': status,
                'Scheduled_Date': scheduled_date.strftime('%Y-%m-%d'),
                'Completion_Date': completion_date.strftime('%Y-%m-%d') if completion_date else ''
            })
    
    # Update user workloads based on active reviews
    active_reviews = [r for r in reviews if r['Status'] in ['Scheduled', 'In Progress']]
    reviewer_counts = {}
    for review in active_reviews:
        reviewer_id = review['Reviewer_ID']
        reviewer_counts[reviewer_id] = reviewer_counts.get(reviewer_id, 0) + 1
    
    # Update Current_Load in users_df
    for i, user in users_df.iterrows():
        users_df.at[i, 'Current_Load'] = reviewer_counts.get(user['User_ID'], 0)
    
    return pd.DataFrame(reviews)

@st.cache_data
def load_and_validate_data(users_file, projects_file, reviews_file=None, source_type="upload"):
    """Load and validate data from various sources, auto-generate reviews if needed"""
    try:
        # Load users and projects data
        if source_type == "upload":
            users_df = pd.read_csv(users_file)
            projects_df = pd.read_csv(projects_file)
            if reviews_file is not None:
                reviews_df = pd.read_csv(reviews_file)
            else:
                reviews_df = None
        else:  # file paths
            users_df = pd.read_csv(users_file)
            projects_df = pd.read_csv(projects_file)
            if reviews_file and os.path.exists(reviews_file):
                reviews_df = pd.read_csv(reviews_file)
            else:
                reviews_df = None
        
        # Validate required columns for users and projects
        users_required = ['User_ID', 'Name', 'Department']
        projects_required = ['Project_ID', 'Project_Name', 'Department', 'Status']
        
        if not validate_csv_structure(users_df, users_required, "Users"):
            return None, None, None
        if not validate_csv_structure(projects_df, projects_required, "Projects"):
            return None, None, None
        
        # Auto-generate reviews if not provided
        if reviews_df is None or reviews_df.empty:
            st.info("🔄 No reviews data provided. Auto-generating realistic review data...")
            with st.expander("ℹ️ What's included in auto-generated reviews?"):
                st.markdown("""
                **Smart Review Generation:**
                - 🎯 Cross-departmental reviewer assignments for better oversight
                - 📅 Realistic date distributions based on project status
                - 📊 Balanced review status distribution (Completed, In Progress, Overdue, Scheduled)
                - ⚖️ Automatic workload balancing across reviewers
                - 🔄 Multiple reviews per project when appropriate (especially for overdue projects)
                """)
            reviews_df = generate_realistic_reviews(users_df, projects_df)
            st.success("✅ Auto-generated realistic review assignments!")
        else:
            # Validate reviews if provided
            reviews_required = ['Review_ID', 'Project_ID', 'Reviewer_ID', 'Status']
            if not validate_csv_structure(reviews_df, reviews_required, "Reviews"):
                st.warning("⚠️ Reviews file has issues. Auto-generating instead...")
                reviews_df = generate_realistic_reviews(users_df, projects_df)
        
        # Data preprocessing with error handling
        if 'Start_Date' in projects_df.columns:
            projects_df['Start_Date'] = pd.to_datetime(projects_df['Start_Date'], errors='coerce')
        if 'Next_Review_Date' in projects_df.columns:
            projects_df['Next_Review_Date'] = pd.to_datetime(projects_df['Next_Review_Date'], errors='coerce')
        if 'Scheduled_Date' in reviews_df.columns:
            reviews_df['Scheduled_Date'] = pd.to_datetime(reviews_df['Scheduled_Date'], errors='coerce')
        if 'Completion_Date' in reviews_df.columns:
            reviews_df['Completion_Date'] = pd.to_datetime(reviews_df['Completion_Date'], errors='coerce')
        
        # Add missing columns with defaults if needed
        if 'Current_Load' not in users_df.columns:
            users_df['Current_Load'] = 0
        if 'Email' not in users_df.columns:
            users_df['Email'] = users_df['User_ID'].apply(lambda x: f"{x}@company.com")
        
        st.success(f"✅ Data loaded and validated successfully!")
        st.info(f"📊 Loaded: {len(users_df)} users, {len(projects_df)} projects, {len(reviews_df)} reviews")
        
        return users_df, projects_df, reviews_df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None, None, None

def calculate_reviewer_performance(users_df, reviews_df):
    """Calculate comprehensive reviewer performance metrics"""
    performance_data = []
    
    for _, user in users_df.iterrows():
        user_reviews = reviews_df[reviews_df['Reviewer_ID'] == user['User_ID']]
        
        # Calculate metrics
        total_reviews = len(user_reviews)
        completed_reviews = len(user_reviews[user_reviews['Status'] == 'Completed'])
        overdue_reviews = len(user_reviews[user_reviews['Status'] == 'Overdue'])
        in_progress_reviews = len(user_reviews[user_reviews['Status'] == 'In Progress'])
        
        # Calculate completion rate
        completion_rate = (completed_reviews / total_reviews * 100) if total_reviews > 0 else 0
        
        # Calculate average review time for completed reviews
        if 'Completion_Date' in reviews_df.columns and 'Scheduled_Date' in reviews_df.columns:
            completed_with_dates = user_reviews[
                (user_reviews['Status'] == 'Completed') & 
                (user_reviews['Completion_Date'].notna()) & 
                (user_reviews['Scheduled_Date'].notna())
            ]
            
            if len(completed_with_dates) > 0:
                avg_review_time = (completed_with_dates['Completion_Date'] - 
                                 completed_with_dates['Scheduled_Date']).dt.days.mean()
            else:
                avg_review_time = 0
        else:
            avg_review_time = 0
        
        performance_data.append({
            'Reviewer_ID': user['User_ID'],
            'Reviewer_Name': user['Name'],
            'Department': user.get('Department', 'Unknown'),
            'Total_Reviews': total_reviews,
            'Completed_Reviews': completed_reviews,
            'Overdue_Reviews': overdue_reviews,
            'In_Progress_Reviews': in_progress_reviews,
            'Completion_Rate': completion_rate,
            'Avg_Review_Days': avg_review_time,
            'Current_Load': int(user.get('Current_Load', 0))
        })
    
    return pd.DataFrame(performance_data)

def calculate_project_metrics(projects_df):
    """Calculate project completion and status metrics"""
    total_projects = len(projects_df)
    
    # Handle different possible status values
    status_counts = projects_df['Status'].value_counts()
    overdue_projects = status_counts.get('Overdue', 0)
    due_soon_projects = status_counts.get('Due Soon', 0)
    up_to_date_projects = status_counts.get('Up to Date', 0) + status_counts.get('Current', 0)
    
    return {
        'total_projects': total_projects,
        'overdue_projects': overdue_projects,
        'due_soon_projects': due_soon_projects,
        'up_to_date_projects': up_to_date_projects,
        'status_counts': status_counts
    }

def create_workload_chart(performance_df):
    """Create workload distribution chart"""
    if performance_df.empty:
        return None
        
    fig = px.bar(
        performance_df,
        x='Reviewer_Name',
        y='Current_Load',
        color='Department',
        title='Current Workload Distribution by Reviewer',
        labels={'Current_Load': 'Active Reviews', 'Reviewer_Name': 'Reviewer'},
        text='Current_Load'
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=True
    )
    
    return fig

def create_status_pie_chart(project_metrics):
    """Create project status pie chart"""
    status_counts = project_metrics['status_counts']
    if status_counts.empty:
        return None
        
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        textinfo='label+percent+value',
        hole=0.4
    )])
    
    fig.update_layout(
        title='Project Status Distribution',
        height=400
    )
    
    return fig

# Sidebar for data input methods
st.sidebar.header("📁 Data Input Methods")

# Auto-detect files in current directory
detected_files = auto_detect_csv_files()

input_method = st.sidebar.radio(
    "Choose how to load your data:",
    ["Upload CSV Files", "Auto-detect Files", "Manual File Paths"]
)

users_df, projects_df, reviews_df = None, None, None

if input_method == "Upload CSV Files":
    st.sidebar.subheader("📤 Upload Your CSV Files")
    
    st.markdown("""
    <div class="upload-info">
        <h4>📋 Required File Format</h4>
        <p><strong>Users.csv:</strong> User_ID, Name, Department (Current_Load optional)</p>
        <p><strong>Projects.csv:</strong> Project_ID, Project_Name, Department, Status</p>
        <p><strong>Reviews.csv:</strong> <em>Optional!</em> Will auto-generate if not provided</p>
    </div>
    """, unsafe_allow_html=True)
    
    users_file = st.sidebar.file_uploader("Upload Users CSV", type=["csv"], key="users_upload")
    projects_file = st.sidebar.file_uploader("Upload Projects CSV", type=["csv"], key="projects_upload")
    reviews_file = st.sidebar.file_uploader("Upload Reviews CSV (Optional)", type=["csv"], key="reviews_upload")
    
    if users_file and projects_file:
        users_df, projects_df, reviews_df = load_and_validate_data(
            users_file, projects_file, reviews_file, "upload"
        )

elif input_method == "Auto-detect Files":
    st.sidebar.subheader("🔍 Auto-detected Files")
    
    if detected_files:
        st.sidebar.success("✅ Found CSV files:")
        for file_type, filename in detected_files.items():
            st.sidebar.write(f"• {file_type.title()}: {filename}")
        
        if len(detected_files) >= 2:  # Only need users and projects
            try:
                reviews_file = detected_files.get('reviews', None)
                users_df, projects_df, reviews_df = load_and_validate_data(
                    detected_files['users'], 
                    detected_files['projects'], 
                    reviews_file, 
                    "files"
                )
            except KeyError as e:
                st.sidebar.error(f"Missing required file type: {e}")
        else:
            st.sidebar.warning("⚠️ Need at least Users and Projects CSV files")
    else:
        st.sidebar.warning("⚠️ No CSV files found in current directory")
        st.sidebar.info("Make sure your CSV files contain 'user' and 'project' in their names")

elif input_method == "Manual File Paths":
    st.sidebar.subheader("📂 Manual File Paths")
    
    users_path = st.sidebar.text_input("Users CSV Path:", value="Users.csv")
    projects_path = st.sidebar.text_input("Projects CSV Path:", value="Projects.csv")
    reviews_path = st.sidebar.text_input("Reviews CSV Path (Optional):", value="Reviews.csv")
    
    if st.sidebar.button("Load Files"):
        if os.path.exists(users_path) and os.path.exists(projects_path):
            reviews_file = reviews_path if os.path.exists(reviews_path) else None
            users_df, projects_df, reviews_df = load_and_validate_data(
                users_path, projects_path, reviews_file, "files"
            )
        else:
            st.sidebar.error("❌ Users.csv and Projects.csv are required")

# Main dashboard logic
if users_df is not None and projects_df is not None and reviews_df is not None:
    
    # Add option to regenerate reviews
    with st.sidebar.expander("🔄 Review Generation Options"):
        if st.button("🎲 Regenerate Reviews", help="Create new random review assignments"):
            st.session_state.regenerate_reviews = True
    
    # Regenerate reviews if requested
    if st.session_state.get('regenerate_reviews', False):
        with st.spinner("Regenerating reviews..."):
            reviews_df = generate_realistic_reviews(users_df, projects_df)
        st.success("✅ Reviews regenerated with new assignments!")
        st.session_state.regenerate_reviews = False
    
    # Calculate metrics
    performance_df = calculate_reviewer_performance(users_df, reviews_df)
    project_metrics = calculate_project_metrics(projects_df)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    departments = ['All'] + list(users_df['Department'].unique())
    selected_dept = st.sidebar.selectbox("Filter by Department", departments)
    
    # Apply department filter
    if selected_dept != 'All':
        performance_df = performance_df[performance_df['Department'] == selected_dept]
        projects_df_filtered = projects_df[projects_df['Department'] == selected_dept]
        project_metrics = calculate_project_metrics(projects_df_filtered)
    
    # Key Performance Indicators (KPIs)
    st.header("🎯 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Projects",
            value=project_metrics['total_projects'],
            delta=f"{project_metrics['up_to_date_projects']} up to date"
        )
    
    with col2:
        if not performance_df.empty:
            avg_completion_rate = performance_df['Completion_Rate'].mean()
            high_performers = len(performance_df[performance_df['Completion_Rate'] > 80])
        else:
            avg_completion_rate = 0
            high_performers = 0
            
        st.metric(
            label="Avg Completion Rate",
            value=f"{avg_completion_rate:.1f}%",
            delta=f"{high_performers} high performers"
        )
    
    with col3:
        overdue_pct = (project_metrics['overdue_projects']/project_metrics['total_projects']*100) if project_metrics['total_projects'] > 0 else 0
        st.metric(
            label="Overdue Projects",
            value=project_metrics['overdue_projects'],
            delta=f"{overdue_pct:.1f}% of total",
            delta_color="inverse"
        )
    
    with col4:
        total_active_reviews = performance_df['Current_Load'].sum() if not performance_df.empty else 0
        in_progress = performance_df['In_Progress_Reviews'].sum() if not performance_df.empty else 0
        st.metric(
            label="Active Reviews",
            value=total_active_reviews,
            delta=f"{in_progress} in progress"
        )
    
    # Main dashboard content
    st.header("📈 Analytics Dashboard")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        workload_chart = create_workload_chart(performance_df)
        if workload_chart:
            st.plotly_chart(workload_chart, use_container_width=True)
        else:
            st.info("No reviewer data available for workload chart")
    
    with col2:
        status_pie = create_status_pie_chart(project_metrics)
        if status_pie:
            st.plotly_chart(status_pie, use_container_width=True)
        else:
            st.info("No project status data available")
    
    # Detailed Tables
    st.header("📊 Detailed Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Reviewer Performance", "Project Details", "Data Summary"])
    
    with tab1:
        st.subheader("Reviewer Performance Metrics")
        if not performance_df.empty:
            st.dataframe(
                performance_df.sort_values('Completion_Rate', ascending=False),
                use_container_width=True
            )
            
            # Download button
            csv_performance = performance_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Performance Report",
                data=csv_performance,
                file_name=f"reviewer_performance_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No performance data available")
    
    with tab2:
        st.subheader("Project Status Overview")
        display_columns = ['Project_ID', 'Project_Name', 'Department', 'Status']
        if 'Next_Review_Date' in projects_df.columns:
            display_columns.append('Next_Review_Date')
            
        st.dataframe(
            projects_df[display_columns],
            use_container_width=True
        )
    
    with tab3:
        st.subheader("Data Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Users Data Columns:**")
            st.write(list(users_df.columns))
        
        with col2:
            st.write("**Projects Data Columns:**")
            st.write(list(projects_df.columns))
        
        with col3:
            st.write("**Reviews Data Columns:**")
            st.write(list(reviews_df.columns))

else:
    # Instructions for users
    st.info("👆 Please select a data input method from the sidebar to get started!")
    
    # Sample data format guide
    st.header("📋 Sample Data Format")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Users.csv (Required)")
        st.code("""User_ID,Name,Email,Department,Current_Load
U001,John Doe,john@email.com,IT,3
U002,Jane Smith,jane@email.com,HR,2
U003,Bob Wilson,bob@email.com,Finance,1""")
    
    with col2:
        st.subheader("Projects.csv (Required)")
        st.code("""Project_ID,Project_Name,Department,Status,Next_Review_Date
P001,System Upgrade,IT,Due Soon,2025-06-15
P002,Policy Review,HR,Up to Date,2025-07-01
P003,Budget Analysis,Finance,Overdue,2025-05-30""")
    
    with col3:
        st.subheader("Reviews.csv (Optional)")
        st.code("""Review_ID,Project_ID,Reviewer_ID,Status,Scheduled_Date
R001,P001,U001,In Progress,2025-06-10
R002,P002,U002,Completed,2025-05-15
R003,P003,U003,Overdue,2025-05-25""")
        st.info("💡 If not provided, reviews will be auto-generated!")
    
    st.header("🚀 Getting Started")
    st.markdown("""
    **Option 1 - Upload Files:** Use the sidebar to upload your CSV files directly (only Users and Projects required!)
    
    **Option 2 - Auto-detect:** Place your CSV files in the same directory as this dashboard and ensure filenames contain 'user' and 'project'
    
    **Option 3 - File Paths:** Enter the full paths to your CSV files in the sidebar
    
    **✨ Smart Features:**
    - Reviews are **automatically generated** if not provided
    - Missing columns are added with sensible defaults
    - Cross-departmental reviewer assignments for better oversight
    - Realistic review status distributions based on project status
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Universal Project Review Analytics Dashboard | Auto-generates missing data for instant insights!"
    "</div>", 
    unsafe_allow_html=True
)
