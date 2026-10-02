# =========================================================
# STUDY SCHEDULE
# Planly - Student Workload & Task Management System
# =========================================================

import streamlit as st


def render(app):

    st.title(
        "📅 Study Schedule Recommendation"
    )

    st.write(
        "Planly helps distribute your study time "
        "so you don't have to rush everything at once. 💗"
    )

    st.divider()

    schedule = (
        app.scheduler.generate_schedule(
            app.student
        )
    )

    if not schedule:

        st.info(
            "🌸 No pending tasks available "
            "for scheduling."
        )

    else:

        for item in schedule:

            task = item["task"]

            study_days = item["study_days"]

            daily_hours = item["daily_hours"]

            st.markdown(
                '<div class="pink-card">',
                unsafe_allow_html=True
            )

            st.subheader(
                f"📚 {task.name}"
            )

            st.write(
                f"**Subject:** {task.subject}"
            )

            st.write(
                f"**Deadline:** {task.deadline}"
            )

            st.write(
                f"**Total Study Time:** "
                f"{task.estimated_hours} hour(s)"
            )

            if study_days == 1:

                st.info(
                    f"🎀 Recommendation: Spend about "
                    f"{daily_hours:.1f} hour(s) "
                    "on this task today."
                )

            else:

                st.info(
                    f"🎀 Recommendation: Spread this "
                    f"task across {study_days} day(s), "
                    f"about {daily_hours:.1f} hour(s) "
                    "per day."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )