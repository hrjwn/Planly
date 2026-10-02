from . import (
    dashboard,
    add_task,
    my_tasks,
    workload_balance,
    study_schedule
)


# =========================================================
# NAVIGATION -> PAGE RENDERER
# =========================================================

PAGES = {
    "🏠 Dashboard": dashboard.render,
    "➕ Add Task": add_task.render,
    "📝 My Tasks": my_tasks.render,
    "⚖️ Workload Balance": workload_balance.render,
    "📅 Study Schedule": study_schedule.render
}
