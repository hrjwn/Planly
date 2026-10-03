import streamlit as st

st.set_page_config(
    page_title="PLANLY - Student Workload & Task Management System",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #3B3036;
        }

        .stApp {
            background-color: #FFF7FA;
        }

        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #F3B6CF;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #3B3036 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease-in-out;
            border: 1px solid #F3B6CF;
            color: #3B3036;
            background-color: #FFFFFF;
        }

        .stButton > button:hover {
            border-color: #D96C9D;
            color: #D96C9D;
            background-color: #FFF7FA;
        }

        .stButton > button[kind="primary"], 
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #D96C9D !important;
            color: #FFFFFF !important;
            border: 1px solid #D96C9D !important;
            box-shadow: 0 2px 8px rgba(217, 108, 157, 0.25);
        }

        .stButton > button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #C95A8D !important;
            border-color: #C95A8D !important;
            box-shadow: 0 4px 12px rgba(201, 90, 141, 0.35);
        }

        div[data-baseweb="input"] {
            border-radius: 8px;
            border-color: #F3B6CF !important;
            background-color: #FFFFFF !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #D96C9D !important;
            box-shadow: 0 0 0 2px rgba(217, 108, 157, 0.15) !important;
        }

        div[data-baseweb="select"] > div {
            border-radius: 8px;
            border-color: #F3B6CF !important;
            background-color: #FFFFFF !important;
        }

        button[data-baseweb="tab"] {
            font-weight: 600;
            color: #8A737D;
            padding: 0.8rem 1.2rem;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #D96C9D !important;
            border-bottom-color: #D96C9D !important;
        }

        div[data-testid="stProgress"] > div > div > div > div {
            background-color: #D96C9D !important;
            border-radius: 10px;
        }

        div[data-testid="stRadio"] > div {
            gap: 6px;
        }

        div[data-testid="stRadio"] label {
            background-color: #FFFFFF;
            border: 1px solid transparent;
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            transition: all 0.15s ease-in-out;
            font-weight: 500;
            color: #3B3036;
        }

        div[data-testid="stRadio"] label:hover {
            background-color: #FFF7FA;
            border-color: #FCE8F0;
        }

        details[data-testid="stExpander"] {
            border: 1px solid #F3B6CF !important;
            border-radius: 12px !important;
            background-color: #FFFFFF !important;
            box-shadow: 0 2px 6px rgba(217, 108, 157, 0.04) !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 10px;
            border: 1px solid #F3B6CF;
        }

        header[data-testid="stHeader"] {
            background-color: transparent;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

from views.login_view import render_login_view
from views.dashboard_view import render_dashboard
from views.task_view import render_task_view
from views.progress_view import render_progress_view
from views.profile_view import render_profile_view
from controllers.auth_controllers import AuthController

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student" not in st.session_state:
    st.session_state.student = None
if "nav_radio" not in st.session_state:
    st.session_state.nav_radio = "Dashboard"

if not st.session_state.get("logged_in") or st.session_state.get("student") is None:
    render_login_view()
    st.stop()

student = st.session_state.student

if student:
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

        nav_options = [
            "Dashboard",
            "My Tasks",
            "My Progress",
            "Profile",
        ]

        # Check if programmatic page navigation was requested (e.g., from Quick Actions)
        if st.session_state.get("page_to_navigate"):
            target_page = st.session_state.pop("page_to_navigate")
            if target_page in nav_options:
                st.session_state.nav_radio = target_page

        if st.session_state.nav_radio not in nav_options:
            st.session_state.nav_radio = "Dashboard"

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

    if page == "Dashboard":
        render_dashboard(student)
    elif page == "My Tasks":
        render_task_view(student)
    elif page == "My Progress":
        render_progress_view(student)
    elif page == "Profile":
        render_profile_view(student)