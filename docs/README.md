# Week 7: Secure Authentication System
Student Name: Hana Mundambra
Student ID: M01087805
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper password verification.

## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence

## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation:
- Username: 3-20 alphanumeric characters, no spaces
- Password: (6-50 characters, must include at least one uppercase letter, one lowercase letter, one number, and one special character)

# Week 8: Data Pipeline & CRUD (SQL)

## Week 8 Lab Description
Loading CSV files for various domains such as cyber_incidents, datasets_metadata and it_tickets into sql database format. 
Implementing CRUD functions on the created databases.

## Features:
- Databse schema with multiple domain tables (users, cyber_incidents, datasets_metadata and it_tickets)
- Error handling for schema mismatches and constraint violations
- Analytical queries for all databases

## Technical Implementation
- Tables implemented:
- users - stores registered user accounts
-  cyber_incidents - Incident tracking with incident_type, severity, category, status and description
-  datasets_metadata - Manage datasetes including record_count 
-  it_tickets - Manage IT service tickets with priority, category, subject and resolution time

# Week 9: Web Interface, MVC & Visualization 

## Week 9 Lab Description:
This week focused on creating a streamlit main page and dashboard for first domain, implementing the CRUD functions created on week 8 to the webpage. 
The goal is to create a clean user experience while separating logic, UI, and data handling.

## Features:
- Main page with login and register tabs.
- Cyber Incidents Dashboard showcasing datasets and data visualizaiton to achieve the aim of the domain.
- Structured MVC with proper layout of files in dedicated folders.

## Technical Implementation:
- Main page contains login and register tabs that validates password and username using week 07 functions.
- Dashboard for cyber incidents analyses the cyber threat with most records.
- Plotly used for data visualization.

# Week 10: Final Dashboards & AI Integration

## Week 10 Lab Description:
This week focuses on finishing up all three domain dashboards as well as AI integration to the dashboards to aid users for analysis and various other purposes.

## Features:
- Dashboards for datasets and IT tickets created. 
- All three streamlit pages contains data visualization as well as AI chatbots for queries prompted by the users.
- Gemini API set up in environment, and integrated to the streamlit web-interface.

## Technical Implementation:
- Gemini API key can distinguish queries according to the keywords.
- Keyword dictionary helps model to identify if the question is about the datasets or general.
- Stacked Bar charts created for all domains for easier and simplified classification of data, this also aids in achieving the main objective of each domains.



