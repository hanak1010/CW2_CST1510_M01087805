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