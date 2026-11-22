# IT Incident Tracker

A command-line IT incident management application built with Python and SQLite. It allows users to record incidents, assign priorities based on impact and urgency, update incident details, and track resolutions.

## Features

- **Create incidents:** Record incident details and reporter information.
- **Automatic prioritisation:** Calculate priority using impact and urgency.
- **View incidents:** Retrieve an incident by its ID.
- **List incidents:** Display incidents, newest first.
- **Update incidents:** Modify details while keeping unchanged values.
- **Resolve incidents:** Save resolution notes and mark incidents resolved.
- **Input validation:** Reject invalid or incomplete information.
- **SQLite persistence:** Store incidents in a local database.
- **Logging:** Record application events and unexpected errors.
- **Automated tests:** Verify behaviour using pytest.

## Technologies

- Python
- SQLite
- pytest
- Git

## Requirements

- Python 3.14 or a compatible Python version
- pip

## Installation

Open Command Prompt in the project directory and create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows Command Prompt:

```bat
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the application

From the project root, run:

```bash
python -m incident_tracker.app
```

The application stores incidents in a local SQLite database named `incidents.db`.

## Running the tests

Run the complete test suite with:

```bash
python -m pytest -v
```

The project currently has **53 automated tests**, all passing.

## Project structure

```text
incident-tracker/
|-- incident_tracker/
|   |-- __init__.py
|   |-- app.py
|   |-- cli.py
|   |-- database.py
|   |-- errors.py
|   |-- logging_setup.py
|   |-- models.py
|   |-- repository.py
|   `-- validation.py
|-- tests/
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Learning objectives

This project demonstrates:

- Python modules and functions
- Input validation and exception handling
- SQLite database operations and SQL queries
- Separation of concerns
- Logging and error reporting
- Automated testing with pytest
- Git version control