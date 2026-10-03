import streamlit as st
from supabase import create_client, Client

def get_supabase_client() -> Client:
    if "supabase_client" not in st.session_state:
        try:
            supabase_url = st.secrets.get("SUPABASE_URL", "").strip()
            supabase_key = st.secrets.get("SUPABASE_KEY", "").strip()
        except Exception:
            supabase_url = ""
            supabase_key = ""

        if not supabase_url or not supabase_key or "your-project-id" in supabase_url:
            st.error(
                "Supabase credentials are missing or not configured. "
                "Please configure .streamlit/secrets.toml with your Supabase URL and anon key."
            )
            st.stop()

        st.session_state.supabase_client = create_client(supabase_url, supabase_key)

    return st.session_state.supabase_client

def reset_supabase_client():
    if "supabase_client" in st.session_state:
        try:
            st.session_state.supabase_client.auth.sign_out()
        except Exception:
            pass
        del st.session_state["supabase_client"]
