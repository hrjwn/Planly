from typing import List
import streamlit as st
from models.student import Student
from controllers.auth_controller import AuthController


def render_sidebar(student: Student, nav_options: List[str]) -> str:
    """Draw the sidebar and return the selected page name."""
    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = nav_options[0]

    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 0.5rem 0 1.2rem 0; border-bottom: 1px solid #F3B6CF; margin-bottom: 1.2rem;">
                <h1 style="margin: 0; font-size: 1.8rem; font-weight: 800; color: #D96C9D; letter-spacing: -0.01em;">
                    PLANLY
                </h1>
                <p style="margin: 0.15rem 0 0.4rem 0; color: #3B3036; font-size: 0.8rem; font-weight: 600;">
                    Student Workload & Task Management System
                </p>
                <div style="font-size: 0.75rem; color: #8A737D; font-style: italic; margin-bottom: 0.8rem;">
                    Plan your work. Track your progress.
                </div>
                <div style="background-color: #FFF7FA; border: 1px solid #F3B6CF; color: #3B3036; padding: 0.5rem 0.8rem; border-radius: 12px; font-size: 0.82rem; text-align: left;">
                    <div style="font-weight: 700; color: #D96C9D;">{student.name}</div>
                    <div style="font-size: 0.75rem; color: #8A737D;">{student.course}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Check if programmatic page navigation was requested (e.g., from Quick Actions)
        if st.session_state.get("page_to_navigate"):
            target_page = st.session_state.pop("page_to_navigate")
            if target_page in nav_options:
                st.session_state.nav_radio = target_page

        if st.session_state.nav_radio not in nav_options:
            st.session_state.nav_radio = nav_options[0]

        page = st.radio(
            "Navigation",
            nav_options,
            key="nav_radio",
            label_visibility="collapsed",
        )

        st.markdown(
            """
            <div style="margin: 1.2rem 0; border-top: 1px solid #F3B6CF;"></div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="background-color: #FFF7FA; border: 1px solid #F3B6CF; border-radius: 10px; padding: 0.9rem; font-size: 0.8rem; color: #3B3036; line-height: 1.5; margin-bottom: 1.2rem;">
                <b style="color: #D96C9D; display: block; margin-bottom: 0.2rem;">Academic Well-Being</b>
                Maintain steady progress by scheduling tasks across multiple days and setting realistic deadlines.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Log Out", use_container_width=True):
            AuthController.logout_student()

    return page
