# =========================================================
# SIDEBAR
# Planly - Student Workload & Task Management System
# =========================================================

import streamlit as st


SIDEBAR_HEADER = (
    """
    <h1>🎀 Planly</h1>
    <p>
    Student Workload & Task Management System
    </p>
    """
)


def render_sidebar(pages):

    st.sidebar.markdown(
        SIDEBAR_HEADER,
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        pages
    )

    st.sidebar.divider()

    st.sidebar.caption(
        "Plan your tasks. Balance your workload. 💗"
    )

    return page
