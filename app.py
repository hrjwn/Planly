import streamlit as st

st.set_page_config(
    page_title="PLANLY - Student Workload & Task Management System",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui import apply_global_styles, render_sidebar
from views import (
    render_login_view,
    render_dashboard,
    render_task_view,
    render_progress_view,
    render_profile_view,
)

PAGES = {
    "Dashboard": render_dashboard,
    "My Tasks": render_task_view,
    "My Progress": render_progress_view,
    "Profile": render_profile_view,
}

apply_global_styles()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student" not in st.session_state:
    st.session_state.student = None

if not st.session_state.get("logged_in") or st.session_state.get("student") is None:
    render_login_view()
    st.stop()

student = st.session_state.student
page = render_sidebar(student, list(PAGES))
PAGES[page](student)
