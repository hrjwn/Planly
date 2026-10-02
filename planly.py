# =========================================================
# PLANLY
# Student Workload & Task Management System
# =========================================================

import sys
from pathlib import Path

import streamlit as st

# Make project packages importable regardless of OS or working directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from planly_app import PlanlyApp
from ui import apply_styles, render_sidebar
from views import PAGES


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
