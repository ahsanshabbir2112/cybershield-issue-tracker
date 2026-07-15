# CyberShield Issue & Vulnerability Tracking System

## Student

Ahsan Shabbir

## Project Overview

This project is an Issue and Vulnerability Tracking System developed using Python, Flask and SQLite.

The purpose of this system is to help a company manage security issues and vulnerabilities. Users can add new issues, view existing issues, update issue information and delete issues when they are no longer required.

The system also provides search, filtering, sorting and reporting features. All API endpoints were tested using Postman.

## Technologies Used

- Python
- Flask
- SQLite
- Postman
- GitHub

## System Requirements

The system allows users to:

- Add a new issue
- View all issues
- View one issue by ID
- Update an issue
- Delete an issue
- Search issues
- Filter issues by severity and status
- Sort issues
- View a summary report
- Validate user input

## Data Requirements

Each issue contains:

| Field | Description |
|-------|-------------|
| id | Unique issue ID |
| title | Issue title |
| description | Issue description |
| severity | Low, Medium, High or Critical |
| status | Open, In Progress, Resolved or Closed |
| assigned_to | Person responsible for the issue |
| date_created | Date and time the issue was created |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Check if the API is running |
| POST | /issues | Add a new issue |
| GET | /issues | View all issues |
| GET | /issues/<id> | View one issue |
| PUT/PATCH | /issues/<id> | Update an issue |
| DELETE | /issues/<id> | Delete an issue |
| GET | /reports/summary | View summary report |

## Search, Filtering and Sorting

The system allows users to search for issues using keywords.

Example:

GET /issues?search=password

Filter by severity:

GET /issues?severity=Critical

Filter by status:

GET /issues?status=Open

Sort by title:

GET /issues?sort_by=title&order=asc

Sort by newest issue:

GET /issues?sort_by=id&order=desc

## Validation

The system checks user input before saving data.

Validation rules:

- Title cannot be empty.
- Title must contain at least 5 characters.
- Title cannot be longer than 100 characters.
- Description cannot be longer than 500 characters.
- Severity must be Low, Medium, High or Critical.
- Status must be Open, In Progress, Resolved or Closed.

## Running the Project

1. Create a virtual environment.

python -m venv venv

2. Activate the virtual environment.

.\venv\Scripts\Activate.ps1

3. Install the required packages.

pip install -r requirements.txt

4. Run the application.

python app.py

The API will run at:

http://127.0.0.1:5000

## Testing

The API was tested using Postman.

The following tests were completed:

- Create Issue
- View All Issues
- View Single Issue
- Update Issue
- Delete Issue
- Search Issues
- Filter Issues
- Sort Issues
- Summary Report
- Invalid Input Testing

## Code Attribution

This project was developed with the help of OpenAI ChatGPT.

The generated code was reviewed, typed, integrated and tested by Ahsan Shabbir.

Postman testing, GitHub commits, project setup and documentation were completed by Ahsan Shabbir.