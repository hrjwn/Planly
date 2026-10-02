# =========================================================
# PLANLY
# Student Workload & Task Management System
# =========================================================

import streamlit as st

from backend import PlanlyApp
from frontend import apply_styles, render_sidebar, PAGES


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Planly",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "planly" not in st.session_state:
    st.session_state.planly = PlanlyApp()

app = st.session_state.planly


# =========================================================
# STYLES, SIDEBAR & PAGE ROUTING
# =========================================================

apply_styles()

page = render_sidebar(list(PAGES))

PAGES[page](app)
