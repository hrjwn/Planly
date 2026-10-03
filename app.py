import streamlit as st

st.set_page_config(
    page_title="PLANLY - Student Workload & Task Management System",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui import apply_global_styles, render_sidebar
from views import (
    render_dashboard,
    render_floating_timer,
    render_focus_view,
    render_login_view,
    render_profile_view,
    render_progress_view,
    render_task_view,
)

PAGES = {
    "Dashboard": render_dashboard,
    "My Tasks": render_task_view,
    "Focus": render_focus_view,
    "My Progress": render_progress_view,
    "Profile": render_profile_view,
}

apply_global_styles()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student" not in st.session_state:
    st.session_state.student = None

student = st.session_state.student
if not st.session_state.logged_in or student is None:
    render_login_view()
    st.stop()

page = render_sidebar(student, list(PAGES))
PAGES[page](student)

if page != "Focus":
    render_floating_timer(student)
