import streamlit as st

_GLOBAL_CSS = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0..1,0&display=block');

        .pl-icon {
            font-family: 'Material Symbols Rounded';
            font-weight: normal;
            font-style: normal;
            font-size: 1.15em;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            vertical-align: -0.2em;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-smoothing: antialiased;
        }

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
"""


def apply_global_styles():
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)
