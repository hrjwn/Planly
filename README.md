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
├── planly.py                      # Entry point: connects frontend to backend
│
├── backend/                       # Pure Python logic (no Streamlit)
│   ├── __init__.py
│   ├── planly_app.py              # PlanlyApp: the backend's single entry point
│   ├── model/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── student.py
│   └── services/
│       ├── __init__.py
│       ├── workload_analyzer.py
│       └── study_scheduler.py
│
├── frontend/                      # Streamlit UI (talks to backend only via PlanlyApp)
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── styles.py              # Pink aesthetic CSS
│   │   └── sidebar.py             # Sidebar header & navigation
│   └── views/
│       ├── __init__.py            # PAGES: navigation label -> page renderer
│       ├── dashboard.py
│       ├── add_task.py
│       ├── my_tasks.py
│       ├── workload_balance.py
│       └── study_schedule.py
│
└── README.md
```

## Running the App

```bash
pip install -r requirements.txt
streamlit run planly.py
```
