# =========================================================
# PINK AESTHETIC CSS
# Planly - Student Workload & Task Management System
# =========================================================

import streamlit as st


CSS = (
    """
    <style>

    /* ==============================================
       MAIN PAGE
       ============================================== */

    .stApp {
        background-color: #FFF8FB;
    }


    /* ==============================================
       SIDEBAR
       ============================================== */

    [data-testid="stSidebar"] {
        background-color: #FFE6F0;
        border-right: 1px solid #F7B6CE;
    }

    [data-testid="stSidebar"] h1 {
        color: #D94F7D;
        font-weight: 800;
    }

    [data-testid="stSidebar"] p {
        color: #7A5263;
    }


    /* ==============================================
       HEADINGS
       ============================================== */

    h1 {
        color: #C93F70;
        font-weight: 800;
    }

    h2 {
        color: #D94F7D;
    }

    h3 {
        color: #C94F78;
    }


    /* ==============================================
       DASHBOARD TITLE
       ============================================== */

    .planly-title {
        font-size: 46px;
        font-weight: 800;
        color: #C93F70;
        margin-bottom: 5px;
    }

    .planly-subtitle {
        font-size: 18px;
        color: #80606E;
        margin-bottom: 30px;
    }


    /* ==============================================
       CARDS
       ============================================== */

    .pink-card {
        background-color: #FFFFFF;
        border: 1px solid #F5C3D5;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(211, 93, 132, 0.08);
    }


    /* ==============================================
       METRIC CARDS
       ============================================== */

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #F5C3D5;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 3px 10px rgba(211, 93, 132, 0.07);
    }

    [data-testid="stMetricLabel"] {
        color: #8B6171;
    }

    [data-testid="stMetricValue"] {
        color: #C93F70;
    }


    /* ==============================================
       BUTTONS
       ============================================== */

    .stButton > button {
        background-color: #EFA3BD;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 18px;
    }

    .stButton > button:hover {
        background-color: #D94F7D;
        color: white;
    }


    /* ==============================================
       FORM SUBMIT BUTTON
       ============================================== */

    .stFormSubmitButton > button {
        background-color: #D94F7D;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }

    .stFormSubmitButton > button:hover {
        background-color: #C93F70;
        color: white;
    }


    /* ==============================================
       INPUT BOXES
       ============================================== */

    input, textarea {
        border-radius: 10px !important;
    }


    /* ==============================================
       DIVIDER
       ============================================== */

    hr {
        border-color: #F4C5D6;
    }


    /* ==============================================
       TASK CARD
       ============================================== */

    .task-card {
        background-color: #FFFFFF;
        border: 1px solid #F5C3D5;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 15px;
    }


    /* ==============================================
       FOOTER
       ============================================== */

    .footer {
        text-align: center;
        color: #9A7181;
        font-size: 14px;
        padding: 25px;
    }

    </style>
    """
)


def apply_styles():

    st.markdown(
        CSS,
        unsafe_allow_html=True
    )
