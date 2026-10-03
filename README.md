# Planly

## Student Workload & Task Management System

Planly is a student workload and task management system designed to help students organize their academic tasks, monitor their workload, and plan their study time.

## Features

- Student accounts: sign up, log in, and edit your profile
- Add, edit, and delete academic tasks
- Set a subject, deadline, and priority (Low / Medium / High) for each task
- Mark tasks as completed or pending
- Dashboard with workload level (Low / Medium / High) and overdue tasks
- Progress page with completion rate and charts by priority and subject
- Study recommendations based on your current workload
- Each student only sees their own data (Supabase Row Level Security)

### How workload is calculated

Workload level is based on the number of **pending** tasks:

| Pending tasks | Workload level |
|---|---|
| 0–3 | Low |
| 4–7 | Medium |
| 8 or more | High |

The thresholds live in `services/workload_analyzer.py` (`LOW_WORKLOAD_MAX`, `MEDIUM_WORKLOAD_MAX`).

## Technologies Used

- Python (Object-Oriented Programming)
- Streamlit (web interface)
- Supabase (accounts and database)
- pandas (charts and tables)

## Project Structure

```text
Planly/
│
├── test_app.py                # Entry point (streamlit run test_app.py)
│
├── models/                    # Data models
│   ├── task.py
│   └── student.py
│
├── controllers/               # Auth, student, and task logic (Supabase)
│   ├── auth_controllers.py
│   ├── student_controllers.py
│   └── task_controllers.py
│
├── services/                  # Business logic (no Streamlit)
│   ├── workload_analyzer.py
│   └── recommendation_service.py
│
├── database/
│   ├── supabase_client.py     # Supabase connection
│   └── schema.sql             # Tables to create in Supabase
│
├── views/                     # Streamlit pages
│   ├── login_view.py
│   ├── dashboard_view.py
│   ├── task_view.py
│   ├── progress_view.py
│   └── profile_view.py
│
├── .streamlit/secrets.toml.example
├── requirements.txt
└── README.md
```

## Running the App

Works the same on Windows, macOS, and Linux.

1. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Set up Supabase (one time):
   - Create a project at https://supabase.com.
   - In the SQL Editor, run `database/schema.sql`.
   - For local testing, turn off **Authentication → Sign In / Providers → Email → Confirm email**.
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in
     `SUPABASE_URL` and `SUPABASE_KEY` (Project Settings → API). This file is git-ignored.
     You can also set `SUPABASE_URL` and `SUPABASE_KEY` as environment variables instead.

3. Start the app:

   ```bash
   python -m streamlit run test_app.py
   ```

   It opens at http://localhost:8501.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Supabase is not configured" | Make sure `.streamlit/secrets.toml` exists (or the environment variables are set). The app does not read `secrets.toml.example`. |
| `ModuleNotFoundError` | Run `python -m pip install -r requirements.txt` again. |
| "Email not confirmed" when logging in | Turn off **Confirm email** in Supabase (see step 2), or click the link in your inbox. |
| `streamlit` command not found | Use `python -m streamlit run test_app.py` instead of `streamlit run`. |

> Never commit `.streamlit/secrets.toml` or put real keys in `secrets.toml.example`.
