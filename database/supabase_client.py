import os
import streamlit as st
from supabase import Client, create_client

# Each browser session gets its own client so one student's login
# never leaks into another student's session.
_SESSION_KEY = "_supabase_client"


def _get_setting(name: str) -> str:
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.environ.get(name, "")


def get_supabase_client() -> Client:
    client = st.session_state.get(_SESSION_KEY)
    if client is not None:
        return client

    url = _get_setting("SUPABASE_URL")
    key = _get_setting("SUPABASE_KEY")
    if not url or not key:
        st.error(
            "Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY to "
            ".streamlit/secrets.toml (see .streamlit/secrets.toml.example)."
        )
        st.stop()

    client = create_client(url, key)
    st.session_state[_SESSION_KEY] = client
    return client


def reset_supabase_client():
    client = st.session_state.pop(_SESSION_KEY, None)
    if client is not None:
        try:
            client.auth.sign_out()
        except Exception:
            pass
