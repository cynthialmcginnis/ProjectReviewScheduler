%%html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Software Design Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }
        h1 {
            color: #0000CD;
            border-bottom: 2px solid #0000CD;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 28px;
        }
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Software Design Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }
        h1 {
            color: #0000CD;
            border-bottom: 2px solid #0000CD;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 28px;
        }
        h2 {
            color: #0000CD;
            border-bottom: 2px solid #0000CD;
            padding-bottom: 5px;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 24px;
        }
        h3 {
            color: #0000CD;
            border-bottom: 1px solid #0000CD;
            padding-bottom: 3px;
            margin-top: 25px;
            font-size: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:nth-child(odd) {
            background-color: #e6e9ff;
        }
        th {
            background-color: #b3b9ff;
            color: #0000CD;
        }
        .header-table td:first-child {
            background-color: #b3b9ff;
            font-weight: bold;
            width: 30%;
        }
        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 3px;
            overflow-x: auto;
        }
        ul, ol {
            margin-left: 20px;
        }
    </style>
</head>
<body>

<h1>Software Design Documentation</h1>

<table class="header-table">
    <tr>
        <td>Product Name</td>
        <td>Project Review Scheduler</td>
    </tr>
    <tr>
        <td>Date Updated</td>
        <td>May 6, 2025</td>
    </tr>
    <tr>
        <td>Written By</td>
        <td>C. McGinnis</td>
    </tr>
</table>

<h2>Introduction</h2>
<p>
The purpose of this document is to provide a comprehensive overview of the software design for the Project Review Scheduler application. This includes the system overview, design considerations, specifications, detailed design, implementation plan, testing plan, and maintenance plan.
</p>

<h2>System Overview</h2>

<h3>2.1 System Description</h3>
<p>
The Project Review Scheduler is an automated system designed to replace the current manual Excel-based process for managing project reviews. It systematically tracks projects requiring review, calculates due dates based on configured frequencies, assigns reviewers based on workload balance, sends notifications, and generates reports. The system uses a lightweight architecture with CSV files for data storage and Python for processing, making it easily deployable with minimal infrastructure requirements.
</p>

<h3>2.2 System Context</h3>
<p>
The Project Review Scheduler operates within the organization's project management environment, interfacing with multiple stakeholders:
</p>
<ul>
    <li>Project managers initiate projects and prepare materials for reviews</li>
    <li>Reviewers conduct evaluations based on assigned schedules</li>
    <li>Administrative staff manage the review process and monitor compliance</li>
    <li>Leadership oversees the entire process and uses reports for decision-making</li>
</ul>
<p>
The system automates previously manual tasks including due date calculation, reviewer assignment, notification, and reporting, eliminating the 15% oversight rate and 22% error rate identified in the current process.
</p>

<h3>2.3 System Architecture</h3>
<p>
The system follows a modular architecture with five primary components:
</p>
<ol>
    <li>Data Storage Layer: Three interconnected CSV files (Projects.csv, Users.csv, Reviews.csv) maintain all system data</li>
    <li>Processing Engine: Python-based components that implement the core business logic</li>
    <li>Calculation Module: Determines which projects need review and when</li>
    <li>Assignment Module: Distributes reviews fairly among available reviewers</li>
    <li>Communication Module: Sends notifications to relevant stakeholders</li>
    <li>Reporting Module: Generates visualizations and reports for management</li>
</ol>
<p>
The architecture prioritizes simplicity and maintainability while providing all required functionality. Components are loosely coupled, allowing for independent testing and future enhancements. The command-line interface provides a straightforward mechanism for administrative staff to trigger key system functions without requiring technical expertise.
</p>
<p>
This design delivers a complete solution to the project review challenges while balancing technical constraints and business requirements. The system can be deployed quickly with minimal infrastructure while providing immediate efficiency improvements.
</p>

<h2>Design Considerations</h2>

<h3>3.1 Design Assumptions</h3>
<p>
The Project Review Scheduler design is based on the following assumptions:
</p>
<ul>
    <li>All users have basic computer literacy and can interact with command-line interfaces</li>
    <li>The system will operate on Python 3.x, which is already available in the organization</li>
    <li>CSV files will be accessible in a shared directory for reading and writing</li>
    <li>Email notifications will use standard SMTP libraries available in Python</li>
    <li>User authentication and access control will be handled outside the system scope</li>
    <li>All stakeholders have email accounts and regularly check their email</li>
</ul>

<h3>3.2 Design Constraints</h3>
<p>
Several constraints shaped the design decisions for this system:
</p>
<ul>
    <li>Infrastructure Minimization: The system must operate without requiring a database server or web infrastructure</li>
    <li>Technology Limitations: Implementation must use Python and its standard libraries to leverage existing skills</li>
    <li>Timeline Constraint: The complete system must be deliverable within the 7-week development timeline</li>
    <li>Team Size: The system must be maintainable by a small technical team with limited resources</li>
    <li>Budget Restrictions: The solution must be implemented without purchasing additional software licenses</li>
</ul>

<h3>3.3 Design Trade-offs</h3>
<p>
Key trade-offs were made to balance functionality, simplicity, and timeline constraints:
</p>

<p><strong>File-based vs. Database Storage</strong><br>
<strong>Decision</strong>: CSV files were chosen for data storage</p>
<ul>
    <li><strong>Advantages</strong>: Simplicity, portability, no additional infrastructure, human-readable format</li>
    <li><strong>Disadvantages</strong>: Limited concurrent access, constraints on complex queries, potential for data corruption</li>
    <li><strong>Rationale</strong>: The simplicity and zero-infrastructure requirements outweigh the limitations for initial implementation</li>
</ul>

<p><strong>Command-line vs. Web Interface</strong><br>
<strong>Decision</strong>: Command-line interface selected for user interaction</p>
<ul>
    <li><strong>Advantages</strong>: Rapid development, simple implementation, straightforward operation</li>
    <li><strong>Disadvantages</strong>: Less intuitive for non-technical users, limited visualization capabilities</li>
    <li><strong>Rationale</strong>: The CLI provides the fastest path to a functioning system, while a web interface is planned for future enhancement</li>
</ul>

<p><strong>Local vs. Cloud Deployment</strong><br>
<strong>Decision</strong>: Local network execution chosen for the initial version</p>
<ul>
    <li><strong>Advantages</strong>: Simpler security model, no cloud infrastructure costs, complete data control</li>
    <li><strong>Disadvantages</strong>: Limited remote access, manual deployment process</li>
    <li><strong>Rationale</strong>: Local deployment allows faster implementation while cloud migration can be considered in future phases</li>
</ul>

<p><strong>Manual vs. Automated Testing</strong><br>
<strong>Decision</strong>: Manual testing with some automated unit tests</p>
<ul>
    <li><strong>Advantages</strong>: Faster initial development, simpler test development</li>
    <li><strong>Disadvantages</strong>: Less comprehensive coverage, more labor-intensive verification</li>
    <li><strong>Rationale</strong>: The balance of manual and automated testing provides sufficient quality assurance within the timeline</li>
</ul>

<p>
These design considerations prioritize practical implementation within constraints while providing all required functionality. The system is designed to be extendable, allowing future enhancements to address the limitations of initial trade-offs.
</p>

<h2>Design Specifications</h2>

<table>
    <tr>
        <th>Requirement</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><strong>R1</strong></td>
        <td>The system shall automatically calculate review due dates based on the project start date and configured frequency.</td>
    </tr>
    <tr>
        <td><strong>R2</strong></td>
        <td>The system shall categorize projects as "Overdue," "Due Soon," or "Up to Date" based on calculated review dates.</td>
    </tr>
    <tr>
        <td><strong>R3</strong></td>
        <td>The system shall implement an algorithm to fairly distribute reviews among qualified reviewers based on the current workload.</td>
    </tr>
    <tr>
        <td><strong>R4</strong></td>
        <td>The system shall avoid assigning reviewers to projects from their department when possible.</td>
    </tr>
    <tr>
        <td><strong>R5</strong></td>
        <td>The system shall automatically send email notifications to assigned reviewers about upcoming reviews.</td>
    </tr>
    <tr>
        <td><strong>R6</strong></td>
        <td>The system shall send reminder notifications as due dates approach without completion.</td>
    </tr>
    <tr>
        <td><strong>R7</strong></td>
        <td>The system shall use three interconnected CSV files (Projects.csv, Users.csv, Reviews.csv) for data storage.</td>
    </tr>
    <tr>
        <td><strong>R8</strong></td>
        <td>The system shall maintain referential integrity between the three CSV files.</td>
    </tr>
    <tr>
        <td><strong>R9</strong></td>
        <td>The system shall generate monthly review schedules showing all upcoming reviews.</td>
    </tr>
    <tr>
        <td><strong>R10</strong></td>
        <td>The system shall generate workload distribution reports showing reviewer assignments.</td>
    </tr>
    <tr>
        <td><strong>R11</strong></td>
        <td>The system shall generate overdue review alerts for management attention.</td>
    </tr>
    <tr>
        <td><strong>R12</strong></td>
        <td>The system shall validate all data inputs and maintain data integrity across CSV files.</td>
    </tr>
    <tr>
        <td><strong>R13</strong></td>
        <td>The system shall check for the CSV file's existence and create it if it is missing.</td>
    </tr>
    <tr>
        <td><strong>R14</strong></td>
        <td>The system shall handle exceptions gracefully and continue operation when possible.</td>
    </tr>
    <tr>
        <td><strong>R15</strong></td>
        <td>The system shall provide a command-line interface with four primary operations.</td>
    </tr>
    <tr>
        <td><strong>R16</strong></td>
        <td>The system shall include comprehensive documentation for administrative users.</td>
    </tr>
    <tr>
        <td><strong>R17</strong></td>
        <td>The system shall include technical specifications for maintainers.</td>
    </tr>
    <tr>
        <td><strong>R18</strong></td>
        <td>The system shall export reports to CSV format for sharing.</td>
    </tr>
    <tr>
        <td><strong>R19</strong></td>
        <td>The system shall maintain backup copies of CSV files before operations.</td>
    </tr>
    <tr>
        <td><strong>R20</strong></td>
        <td>The system shall be implementable within a 7-week development timeline.</td>
    </tr>
</table>

<p>
These requirements directly address the inefficiencies identified in the current manual process while conforming to the design constraints and considerations previously outlined.
</p>

<h2>Detailed Design</h2>

<h3>5.1 Architecture Design</h3>
<p>
The system follows a modular architecture with clear separation of concerns:
</p>
<ul>
    <li><strong>Data Layer</strong>: CSV-based storage with defined schemas and relationships</li>
    <li><strong>Business Logic Layer</strong>: Core processing components implementing the requirements</li>
    <li><strong>Interface Layer</strong>: Command-line interface for user interaction</li>
    <li><strong>External Integration</strong>: Email notification system and report generation</li>
</ul>
<p>
All components communicate through well-defined interfaces, enabling independent development and testing while ensuring system cohesion.
</p>

<h3>5.2 Data Structure Design</h3>
<p>
The data model consists of three primary entities with the following attributes:
</p>

<p><strong>Projects</strong>:</p>
<ul>
    <li>Project_ID (Primary Key): Unique identifier for each project</li>
    <li>Project_Name: Descriptive name of the project</li>
    <li>Start_Date: When the project was initiated</li>
    <li>Last_Review_Date: When the project was last reviewed</li>
    <li>Review_Frequency_Years: How often the project should be reviewed</li>
    <li>Department: Which department owns the project</li>
    <li>Status: Calculated field (Overdue, Due Soon, Up to Date)</li>
</ul>

<p><strong>Users</strong>:</p>
<ul>
    <li>User_ID (Primary Key): Unique identifier for each user</li>
    <li>Name: Full name of the user</li>
    <li>Email: Contact address for notifications</li>
    <li>Department: Which department the user belongs to</li>
    <li>Current_Load: Number of active review assignments</li>
</ul>

<p><strong>Reviews</strong>:</p>
<ul>
    <li>Review_ID (Primary Key): Unique identifier for each review</li>
    <li>Project_ID (Foreign Key): Reference to the project being reviewed</li>
    <li>Reviewer_ID (Foreign Key): Reference to the assigned reviewer</li>
    <li>Scheduled Date: When the review should occur</li>
    <li>Status: Current state (Scheduled, In Progress, Completed)</li>
    <li>Completion_Date: When the review was completed</li>
</ul>

<h3>5.3 Component Specifications</h3>
<p>
Each system component has been designed with specific inputs, outputs, and processing logic:
</p>

<p><strong>Due Date Calculator</strong>:</p>
<ul>
    <li>Takes Projects.csv data and the current date as input</li>
    <li>Calculates the next review date based on the last review and frequency</li>
    <li>Categorizes projects based on days until review</li>
    <li>Returns updated project data with status information</li>
</ul>

<p><strong>Reviewer Assignment Algorithm</strong>:</p>
<ul>
    <li>Takes projects needing review and user workload information</li>
    <li>Sorts reviewers by current workload (ascending)</li>
    <li>Assigns reviews to the least-burdened reviewers</li>
    <li>Updates workload counts after each assignment</li>
    <li>Returns new review assignments</li>
</ul>

<p><strong>Email Notification System</strong>:</p>
<ul>
    <li>Takes review assignments, user data, and project information</li>
    <li>Formats personalized email notifications</li>
    <li>Uses SMTP library to send communications</li>
    <li>Returns confirmation of sent messages</li>
</ul>

<p><strong>Reporting Component</strong>:</p>
<ul>
    <li>Takes project status, review assignments, and workload data</li>
    <li>Generates monthly schedules, workload distributions, and alerts</li>
    <li>Formats output for CSV export and visualization</li>
    <li>Returns report data structures</li>
</ul>

<h3>5.4 Interface Implementation</h3>
<p>
The command-line interface provides four primary operations corresponding to the core functions:
</p>
<pre>
calculate_reviews   - Identifies projects requiring review based on dates
assign_reviewers    - Distributes reviews to available reviewers
send_notifications  - Sends email alerts to assigned reviewers
generate_reports    - Creates monthly schedule and workload reports
</pre>
<p>
Each command accepts relevant parameters and provides feedback through console output, making the system accessible to administrative staff without technical expertise.
</p>
<p>
The development documentation maintains additional detailed specifications for each component, including algorithmic implementations, validation rules, error handling mechanisms, and unit test specifications.
</p>

<h2>Implementation Plan</h2>

<h3>6.1 Implementation Strategy</h3>
<p>
The Project Review Scheduler will be implemented using an incremental development approach, with each component built and tested separately before integration. This strategy allows for early detection of issues and provides flexibility to adjust implementation details based on feedback.
</p>

<h3>6.2 Implementation Schedule</h3>
<table>
    <tr>
        <th>Phase</th>
        <th>Timeframe</th>
        <th>Key Activities</th>
        <th>Deliverables</th>
    </tr>
    <tr>
        <td><strong>Phase 1:</strong> Setup & Requirements (Week 1)</td>
        <td>May 7-13, 2025</td>
        <td>
            - Configure development environment<br>
            - Finalize requirements<br>
            - Create project structure
        </td>
        <td>
            - Configured Python environment<br>
            - Final requirements document<br>
            - GitHub repository structure
        </td>
    </tr>
    <tr>
        <td><strong>Phase 2:</strong> Data Layer (Week 2)</td>
        <td>May 14-20, 2025</td>
        <td>
            - Define CSV schemas<br>
            - Implement data validation<br>
            - Create sample data
        </td>
        <td>
            - CSV schema documentation<br>
            - Data validation module<br>
            - Test data sets
        </td>
    </tr>
    <tr>
        <td><strong>Phase 3:</strong> Core Components (Weeks 3-4)</td>
        <td>May 21-June 3, 2025</td>
        <td>
            - Implement due date calculator<br>
            - Develop reviewer assignment algorithm<br>
            - Build notification system<br>
            - Create reporting module
        </td>
        <td>
            - Functional core components<br>
            - Unit tests for each component<br>
            - Component documentation
        </td>
    </tr>
    <tr>
        <td><strong>Phase 4:</strong> Integration (Week 5)</td>
        <td>June 4-10, 2025</td>
        <td>
            - Integrate all components<br>
            - Implement command-line interface<br>
            - Conduct integration testing
        </td>
        <td>
            - Integrated system<br>
            - CLI documentation<br>
            - Integration test results
        </td>
    </tr>
    <tr>
        <td><strong>Phase 5:</strong> Testing & Refinement (Week 6)</td>
        <td>June 11-17, 2025</td>
        <td>
            - Conduct full system testing<br>
            - Refine based on test results<br>
            - Prepare user documentation
        </td>
        <td>
            - Test reports<br>
            - Refined system<br>
            - User guide draft
        </td>
    </tr>
    <tr>
        <td><strong>Phase 6:</strong> Deployment (Week 7)</td>
        <td>June 18-24, 2025</td>
        <td>
            - Finalize documentation<br>
            - Train administrative staff<br>
            - Deploy to production environment
        </td>
        <td>
            - Final documentation package<br>
            - Trained users<br>
            - Production-ready system
        </td>
    </tr>
</table>

<h3>6.3 Resource Allocation</h3>
<table>
    <tr>
        <th>Resource</th>
        <th>Allocation</th>
        <th>Responsibilities</th>
    </tr>
    <tr>
        <td>Python Developer</td>
        <td>100% (Weeks 1-7)</td>
        <td>Overall system implementation</td>
    </tr>
    <tr>
        <td>Technical Writer</td>
        <td>25% (Weeks 5-7)</td>
        <td>Documentation creation and review</td>
    </tr>
    <tr>
        <td>Administrative Staff</td>
        <td>10% (Weeks 1, 6-7)</td>
        <td>Requirements input and user testing</td>
    </tr>
    <tr>
        <td>Project Manager</td>
        <td>20% (All weeks)</td>
        <td>Schedule management and stakeholder communication</td>
    </tr>
</table>

<h3>6.4 Development Environment</h3>
<ul>
    <li><strong>Programming Language</strong>: Python 3.x</li>
    <li><strong>Libraries</strong>: pandas, matplotlib, smtplib, and standard libraries</li>
    <li><strong>Version Control</strong>: GitHub repository for code management</li>
    <li><strong>Development Tools</strong>: Visual Studio Code with Python extensions</li>
    <li><strong>Testing Framework</strong>: pytest for unit and integration testing</li>
</ul>

<h3>6.5 Risk Management</h3>
<table>
    <tr>
        <th>Risk</th>
        <th>Probability</th>
        <th>Impact</th>
        <th>Mitigation Strategy</th>
    </tr>
    <tr>
        <td>Schedule delays</td>
        <td>Medium</td>
        <td>High</td>
        <td>Buffer time built into each phase; weekly progress reviews</td>
    </tr>
    <tr>
        <td>Data integration issues</td>
        <td>Medium</td>
        <td>Medium</td>
        <td>Early validation with real data samples, incremental testing</td>
    </tr>
    <tr>
        <td>User adoption resistance</td>
        <td>Low</td>
        <td>High</td>
        <td>Early stakeholder involvement, comprehensive training</td>
    </tr>
    <tr>
        <td>Technical limitations</td>
        <td>Low</td>
        <td>Medium</td>
        <td>Proof-of-concept testing for critical components in Week 1</td>
    </tr>
    <tr>
        <td>Resource availability</td>
        <td>Low</td>
        <td>High</td>
        <td>Advance scheduling, clear prioritization of tasks</td>
    </tr>
</table>

<h3>6.6 Quality Assurance</h3>
<ul>
    <li><strong>Code Reviews</strong>: All components will undergo peer review before integration</li>
    <li><strong>Unit Testing</strong>: Minimum 85% code coverage for all core components</li>
    <li><strong>Integration Testing</strong>: Automated testing of component interactions</li>
    <li><strong>System Testing</strong>: Full workflow verification with representative data</li>
    <li><strong>User Acceptance Testing</strong>: Administrative staff validation of system operation</li>
</ul>
<p>
This implementation plan provides a structured approach to developing the Project Review Scheduler while managing risks and ensuring quality. The incremental approach allows for adjustments as development progresses, maximizing the likelihood of successful completion within the 7-week timeline.
</p>

<h2>Testing Plan</h2>

<h3>7.1 Testing Approach Overview</h3>
<p>
The Project Review Scheduler testing plan incorporates multiple testing methodologies to ensure the system meets all requirements and functions correctly in the intended environment. The testing process will be conducted in phases, moving from component-level to system-level verification.
</p>

<h3>7.2 Unit Testing</h3>
<table>
    <tr>
        <th>Component</th>
        <th>Test Cases</th>
        <th>Success Criteria</th>
    </tr>
    <tr>
        <td><strong>Due Date Calculator</strong></td>
        <td>
            - Calculate dates with various frequencies<br>
            - Categorize projects (Overdue, Due Soon, Up to Date)<br>
            - Handle edge cases (missing dates, zero frequency)
        </td>
        <td>
            - Correct next review date calculation<br>
            - Accurate status categorization<br>
            - Proper error handling<br>
            - 100% function coverage
        </td>
    </tr>
    <tr>
        <td><strong>Reviewer Assignment</strong></td>
        <td>
            - Balance workload across reviewers<br>
            - Avoid department conflicts<br>
            - Handle limited reviewer availability<br>
            - Process large assignment batches
        </td>
        <td>
            - Fair distribution of reviews<br>
            - Department conflict avoidance<br>
            - Graceful handling of edge cases<br>
            - Performance within acceptable limits
        </td>
    </tr>
    <tr>
        <td><strong>Email Notification</strong></td>
        <td>
            - Format emails correctly<br>
            - Handle various recipient scenarios<br>
            - Process multiple notifications<br>
            - Manage missing contact information
        </td>
        <td>
            - Correct email formatting<br>
            - Proper recipient handling<br>
            - Successful batch processing<br>
            - Appropriate error messages
        </td>
    </tr>
    <tr>
        <td><strong>Reporting Module</strong></td>
        <td>
            - Generate monthly schedules<br>
            - Create workload distribution reports<br>
            - Produce overdue review alerts<br>
            - Format CSV exports
        </td>
        <td>
            - Accurate report generation<br>
            - Correct data representation<br>
            - Valid CSV file creation<br>
            - Appropriate sorting and filtering
        </td>
    </tr>
</table>

<h3>7.3 Integration Testing</h3>
<table>
    <tr>
        <th>Integration Point</th>
        <th>Test Scenarios</th>
        <th>Validation Method</th>
    </tr>
    <tr>
        <td><strong>Calculator → Assignment</strong></td>
        <td>
            - Projects identified as needing review are correctly passed to the assignment module<br>
            - Status updates are reflected in project data
        </td>
        <td>
            - End-to-end workflow validation<br>
            - Data consistency verification
        </td>
    </tr>
    <tr>
        <td><strong>Assignment → Notification</strong></td>
        <td>
            - Newly assigned reviews trigger notifications<br>
            - Reviewer information is correctly included
        </td>
        <td>
            - Email content verification<br>
            - Notification timing checks
        </td>
    </tr>
    <tr>
        <td><strong>All Components → CSV Files</strong></td>
        <td>
            - Data consistency across operations<br>
            - File locking during updates<br>
            - Recovery from interrupted operations
        </td>
        <td>
            - File integrity checks<br>
            - Concurrent operation testing
        </td>
    </tr>
    <tr>
        <td><strong>Command Line → Components</strong></td>
        <td>
            - Commands correctly trigger appropriate functions<br>
            - Parameters are properly parsed<br>
            - Output is correctly formatted
        </td>
        <td>
            - CLI command execution testing<br>
            - Parameter validation
        </td>
    </tr>
</table>

<h3>7.4 User Acceptance Testing</h3>
<table>
    <tr>
        <th>User Role</th>
        <th>Test Activities</th>
        <th>Acceptance Criteria</th>
    </tr>
    <tr>
        <td><strong>Administrative Staff</strong></td>
        <td>
            - Run due date calculations<br>
            - Generate review assignments<br>
            - Send notifications<br>
            - Create reports
        </td>
        <td>
            - Intuitive command usage<br>
            - Expected results produced<br>
            - Clear error messages<br>
            - Acceptable performance
        </td>
    </tr>
    <tr>
        <td><strong>Team Lead</strong></td>
        <td>
            - Review workload distribution<br>
            - Verify assignment fairness<br>
            - Validate department conflict handling
        </td>
        <td>
            - Balanced reviewer workload<br>
            - Appropriate assignments<br>
            - Clear workload visualization
        </td>
    </tr>
    <tr>
        <td><strong>Project Manager</strong></td>
        <td>
            - Receive and review notifications<br>
            - Verify project information<br>
            - Check scheduling accuracy
        </td>
        <td>
            - Timely notification receipt<br>
            - Complete project information<br>
            - Accurate scheduling
        </td>
    </tr>
    <tr>
        <td><strong>Director</strong></td>
        <td>
            - Review monthly schedules<br>
            - Analyze workload reports<br>
            - Track completion statistics
        </td>
        <td>
            - Comprehensive reporting<br>
            - Clear visualization<br>
            - Actionable insights
        </td>
    </tr>
</table>

<h3>7.5 Performance Testing</h3>
<table>
    <tr>
        <th>Performance Aspect</th>
        <th>Test Scenario</th>
        <th>Performance Targets</th>
    </tr>
    <tr>
        <td><strong>Scalability</strong></td>
        <td>
            - Process 1,000+ projects<br>
            - Handle 100+ simultaneous reviews<br>
            - Manage 50+ reviewers
        </td>
        <td>
            - Processing time under 60 seconds<br>
            - No degradation in accuracy<br>
            - Memory usage within limits
        </td>
    </tr>
    <tr>
        <td><strong>Responsiveness</strong></td>
        <td>
            - Command execution time<br>
            - Report generation speed<br>
            - Email notification throughput
        </td>
        <td>
            - Commands complete in < 5 seconds<br>
            - Reports are generated in < 30 seconds<br>
            - Notifications sent at 10+ per minute
        </td>
    </tr>
    <tr>
        <td><strong>Resource Utilization</strong></td>
        <td>
            - CPU usage during operations<br>
            - Memory consumption<br>
            - Disk I/O during CSV operations
        </td>
        <td>
            - CPU usage < 50% of available<br>
            - Memory < 500MB<br>
            - Disk I/O optimized for minimal contention
        </td>
    </tr>
    <tr>
        <td><strong>Concurrent Operation</strong></td>
        <td>
            - Multiple commands executed simultaneously<br>
            - CSV file access during updates
        </td>
        <td>
            - No data corruption<br>
            - Appropriate locking mechanisms<br>
            - Graceful handling of concurrency
        </td>
    </tr>
</table>

<h3>7.6 Test Environment</h3>
<ul>
    <li><strong>Hardware</strong>: Standard office workstation (8GB RAM, 4-core CPU)</li>
    <li><strong>Operating System</strong>: Windows 10/11 and macOS Monterey</li>
    <li><strong>Python Version</strong>: 3.9 or later</li>
    <li><strong>Test Data</strong>: Realistic dataset with 500+ projects, 50+ users, 200+ reviews</li>
</ul>

<h3>7.7 Test Schedule</h3>
<table>
    <tr>
        <th>Testing Phase</th>
        <th>Timeframe</th>
        <th>Responsible</th>
    </tr>
    <tr>
        <td>Unit Testing</td>
        <td>Weeks 3-4</td>
        <td>Development Team</td>
    </tr>
    <tr>
        <td>Integration Testing</td>
        <td>Week 5</td>
        <td>Development Team</td>
    </tr>
    <tr>
        <td>User Acceptance Testing</td>
        <td>Week 6</td>
        <td>Administrative Staff, Team Leads</td>
    </tr>
    <tr>
        <td>Performance Testing</td>
        <td>Week 6</td>
        <td>Development Team</td>
    </tr>
    <tr>
        <td>Final System Testing</td>
        <td>Week 7</td>
        <td>All Stakeholders</td>
    </tr>
</table>
<p>
This testing plan ensures the Project Review Scheduler will be thoroughly validated before deployment, minimizing the risk of issues during production use while confirming that all requirements are met.
</p>

<h2>Maintenance Plan</h2>

<h3>8.1 Regular Maintenance Activities</h3>
<table>
    <tr>
        <th>Activity</th>
        <th>Frequency</th>
        <th>Responsible Party</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>CSV Backup</td>
        <td>Weekly</td>
        <td>System Administrator</td>
        <td>Automated backup of all CSV files to ensure data recovery capability</td>
    </tr>
    <tr>
        <td>Code Review</td>
        <td>Monthly</td>
        <td>Development Team</td>
        <td>Review of system code for optimization opportunities and technical debt</td>
    </tr>
    <tr>
        <td>Performance Analysis</td>
        <td>Quarterly</td>
        <td>Development Team</td>
        <td>Analysis of system performance metrics to identify bottlenecks</td>
    </tr>
    <tr>
        <td>Security Review</td>
        <td>Quarterly</td>
        <td>Security Team</td>
        <td>Verification of file permissions and data protection measures</td>
    </tr>
    <tr>
        <td>Documentation Update</td>
        <td>As needed</td>
        <td>Technical Writer</td>
        <td>Maintaining current user guides and technical specifications</td>
    </tr>
</table>

<h3>8.2 Bug Fix Process</h3>
<ol>
    <li><strong>Issue Reporting</strong>
        <ul>
            <li>Users report issues through the designated GitHub issue tracker</li>
            <li>Each issue receives a unique identifier and priority classification</li>
        </ul>
    </li>
    <li><strong>Triage Process</strong>
        <ul>
            <li>Issues are reviewed within 48 hours of submission</li>
            <li>Classification as Critical, High, Medium, or Low priority</li>
            <li>Assignment to appropriate technical resource</li>
        </ul>
    </li>
    <li><strong>Resolution Timeline</strong>
        <ul>
            <li>Critical: Fix within 24 hours</li>
            <li>High: Fix within 1 week</li>
            <li>Medium: Fix within 2 weeks</li>
            <li>Low: Address in next planned release</li>
        </ul>
    </li>
    <li><strong>Deployment Approach</strong>
        <ul>
            <li>Critical fixes: Immediate hotfix deployment</li>
            <li>Non-critical fixes: Bundled in scheduled releases</li>
            <li>All fixes undergo regression testing before deployment</li>
        </ul>
    </li>
</ol>

<h3>8.3 Enhancement Management</h3>
<table>
    <tr>
        <th>Phase</th>
        <th>Timeframe</th>
        <th>Enhancement Focus</th>
    </tr>
    <tr>
        <td>Phase 1 Enhancement</td>
        <td>Months 1-3</td>
        <td>User experience improvements based on initial feedback</td>
    </tr>
    <tr>
        <td>Phase 2 Enhancement</td>
        <td>Months 4-6</td>
        <td>Web-based interface development for improved accessibility</td>
    </tr>
    <tr>
        <td>Phase 3 Enhancement</td>
        <td>Months 7-9</td>
        <td>Database integration for concurrent access capability</td>
    </tr>
    <tr>
        <td>Phase 4 Enhancement</td>
        <td>Months 10-12</td>
        <td>Integration with project management systems</td>
    </tr>
</table>

<h3>8.4 Support Structure</h3>
<table>
    <tr>
        <th>Support Level</th>
        <th>Response Time</th>
        <th>Available Hours</th>
        <th>Contact Method</th>
    </tr>
    <tr>
        <td>Tier 1 Support</td>
        <td>4 business hours</td>
        <td>8am-5pm, Mon-Fri</td>
        <td>Email, GitHub issue</td>
    </tr>
    <tr>
        <td>Tier 2 Support</td>
        <td>1 business day</td>
        <td>8am-5pm, Mon-Fri</td>
        <td>Email escalation</td>
    </tr>
    <tr>
        <td>Emergency Support</td>
        <td>2 hours</td>
        <td>24/7 for critical issues</td>
        <td>Emergency contact</td>
    </tr>
</table>

<h3>8.5 System Availability</h3>
<ul>
    <li><strong>Scheduled Maintenance</strong>: Monthly, 2-hour window, scheduled on weekends</li>
    <li><strong>Target Uptime</strong>: 99.5% during business hours (excluding scheduled maintenance)</li>
    <li><strong>Downtime Notification</strong>: Minimum 3 business days advance notice for scheduled maintenance</li>
</ul>

<h3>8.6 Version Control</h3>
<ul>
    <li><strong>Version Naming</strong>: [Major].[Minor].[Patch] format (e.g., 1.2.3)</li>
    <li><strong>Release Cycle</strong>: Major releases quarterly, minor releases monthly, patches as needed</li>
    <li><strong>Change Documentation</strong>: Comprehensive changelog maintained for all versions</li>
    <li><strong>Code Repository</strong>: All changes tracked in GitHub with appropriate branching strategy</li>
</ul>

<h3>8.7 Knowledge Transfer</h3>
<ul>
    <li><strong>Documentation Repository</strong>: Centralized wiki for all system documentation</li>
    <li><strong>Training Materials</strong>: Updated with each major release</li>
    <li><strong>Knowledge Base</strong>: Searchable database of common issues and resolutions</li>
    <li><strong>Cross-Training</strong>: Multiple team members familiar with each system component</li>
</ul>

<h3>8.8 Continuous Improvement</h3>
<ul>
    <li><strong>User Feedback Collection</strong>: Quarterly surveys of administrative users</li>
    <li><strong>Metrics Monitoring</strong>: Tracking of system usage, error rates, and performance</li>
    <li><strong>Technology Review</strong>: Annual evaluation of newer technologies for potential adoption</li>
    <li><strong>Process Refinement</strong>: Ongoing optimization of maintenance procedures</li>
</ul>
<p>
This maintenance plan ensures the Project Review Scheduler remains reliable, secure, and aligned with user needs throughout its lifecycle. Regular monitoring and proactive maintenance activities minimize disruptions while the enhancement roadmap provides a clear path for system evolution.
</p>

<h2>Conclusion</h2>
<p>
This software design documentation overviews the Project Review Scheduler application design. It includes the system overview, design considerations, specifications, detailed design, implementation plan, testing plan, and maintenance plan.
</p>
<p>
The Project Review Scheduler has been designed to address the inefficiencies identified in the manual review process, including the 15% oversight rate and workload imbalances. The system will improve the organization's project review operations through automated date calculation, balanced reviewer assignment, structured notification, and comprehensive reporting.
</p>
<p>
The design balances practical constraints with functional requirements, delivering a solution that is technically feasible within the 7-week timeline and operationally effective. The CSV-based data storage and command-line interface provide simplicity and minimal infrastructure requirements while delivering all required functionality.
</p>
<p>
Implementation will follow an incremental approach with well-defined phases, allowing continuous testing and refinement. The testing strategy ensures all components function correctly individually and together, while the maintenance plan provides a roadmap for ongoing support and enhancement.
</p>
<p>
This document is the definitive reference for the development and future maintenance of the Project Review Scheduler. It establishes clear specifications, processes, and expectations for all aspects of the system, ensuring alignment among stakeholders and technical personnel throughout the project lifecycle.
</p>
<p>
Any revisions to this document will be recorded in the document control section and managed through version control to maintain a complete history of design decisions and changes.
</p>

<p style="margin-top:30px;"><strong>Signatures:</strong></p>
<p>
Project Manager: ___________________________________________<br>
Lead Developer: ____________________________________________
</p>

<h3>Revisions:</h3>
<table>
    <tr>
        <th>Version</th>
        <th>Date</th>
        <th>Author</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>1.0</td>
        <td>04/30/2025</td>
        <td>Cynthia McGinnis</td>
        <td>Initial version</td>
    </tr>
    <tr>
        <td>1.1</td>
        <td>05/1/2025</td>
        <td>Cynthia McGinnis</td>
        <td>Updated implementation plan</td>
    </tr>
    <tr>
        <td>1.2</td>
        <td>05/7/2025</td>
        <td>Cynthia McGinnis</td>
        <td>Updated maintenance plan</td>
    </tr>
</table>
    </style>
</head>
<body>
<!-- Rest of your HTML document content -->
</body>
</html>



