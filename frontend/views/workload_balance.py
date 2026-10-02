# =========================================================
# WORKLOAD BALANCE
# Planly - Student Workload & Task Management System
# =========================================================

import streamlit as st


def render(app):

    st.title("⚖️ Workload Balance")

    st.write(
        "See how manageable your current academic "
        "workload is."
    )

    st.divider()

    score = app.analyzer.calculate_score(
        app.student
    )

    level = app.analyzer.get_workload_level(
        score
    )

    st.metric(
        "💗 Workload Balance Score",
        score
    )

    st.write("")

    if level == "LOW":

        st.success(
            f"Current Workload: {level}"
        )

    elif level == "MODERATE":

        st.warning(
            f"Current Workload: {level}"
        )

    else:

        st.error(
            f"Current Workload: {level}"
        )

    st.write(
        app.analyzer.get_workload_message(
            level
        )
    )

    st.divider()

    st.subheader(
        "🌸 How Planly Calculates Your Workload"
    )

    st.markdown(
        """
        Planly considers three main factors:

        **💗 Task Priority**  
        High-priority tasks contribute more points.

        **📅 Deadline Proximity**  
        Tasks with closer deadlines contribute more points.

        **⏰ Estimated Study Time**  
        Longer tasks contribute additional workload points.
        """
    )
