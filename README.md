# Planly

## Student Workload & Task Management System

Planly is a student workload and task management system designed to help students organize their academic tasks, monitor their workload, and plan their study time.

## Features

- Add academic tasks
- Set task priorities
- Set deadlines
- Assign subjects or courses
- Track completed and pending tasks
- Calculate workload balance
- Generate study schedule recommendations

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Streamlit
- VS Code

## Project Structure

```text
Planly/
│
├── planly.py                  # Entry point (streamlit run planly.py)
├── planly_app.py              # PlanlyApp: single entry point to the app logic
├── run.py                     # Cross-platform launcher (python run.py)
│
├── model/                     # Data models
│   ├── __init__.py
│   ├── task.py
│   └── student.py
│
├── services/                  # Business logic (no Streamlit)
│   ├── __init__.py
│   ├── workload_analyzer.py
│   └── study_scheduler.py
│
├── ui/                        # Shared Streamlit UI pieces
│   ├── __init__.py
│   ├── styles.py              # Pink aesthetic CSS
│   └── sidebar.py             # Sidebar header & navigation
│
├── views/                     # Streamlit pages
│   ├── __init__.py            # PAGES: navigation label -> page renderer
│   ├── dashboard.py
│   ├── add_task.py
│   ├── my_tasks.py
│   ├── workload_balance.py
│   └── study_schedule.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the App

Works the same on Windows, macOS, and Linux:

```bash
python -m pip install -r requirements.txt
python run.py
```

(On macOS/Linux use `python3` if `python` isn't available.)
`python run.py` is equivalent to `python -m streamlit run planly.py`; using
`python -m` avoids "streamlit is not recognized" errors on Windows when the
`streamlit` command isn't on PATH.
