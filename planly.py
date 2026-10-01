# =========================================================
# PLANLY
# Student Workload & Task Management System
# =========================================================

import streamlit as st
from datetime import date

from model import Task, Student
from services import WorkloadAnalyzer, StudyScheduler


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
# PLANLY APPLICATION CLASS
# =========================================================

class PlanlyApp:

    def __init__(self):
        self.student = Student("Student")
        self.analyzer = WorkloadAnalyzer()
        self.scheduler = StudyScheduler()

    def add_task(
        self,
        name,
        subject,
        priority,
        deadline,
        estimated_hours
    ):

        task = Task(
            name,
            subject,
            priority,
            deadline,
            estimated_hours
        )

        self.student.add_task(task)

    def complete_task(self, task_index):

        if 0 <= task_index < len(
            self.student.tasks
        ):

            self.student.tasks[
                task_index
            ].mark_completed()

            return True

        return False


# =========================================================
# SESSION STATE
# =========================================================

if "planly" not in st.session_state:
    st.session_state.planly = PlanlyApp()

app = st.session_state.planly


# =========================================================
# PINK AESTHETIC CSS
# =========================================================

st.markdown(
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
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <h1>🎀 Planly</h1>
    <p>
    Student Workload & Task Management System
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Task",
        "📝 My Tasks",
        "⚖️ Workload Balance",
        "📅 Study Schedule"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Plan your tasks. Balance your workload. 💗"
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="planly-title">'
        'Welcome to Planly 🎀'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="planly-subtitle">'
        'Stay organized, manage your workload, '
        'and study at your own pace. 💗'
        '</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------------------
    # STATISTICS
    # ---------------------------------------------

    total_tasks = len(
        app.student.tasks
    )

    pending_tasks = len(
        app.student.get_pending_tasks()
    )

    completed_tasks = len(
        app.student.get_completed_tasks()
    )

    score = app.analyzer.calculate_score(
        app.student
    )

    workload = app.analyzer.get_workload_level(
        score
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📚 Total Tasks",
            total_tasks
        )

    with col2:
        st.metric(
            "📌 Pending",
            pending_tasks
        )

    with col3:
        st.metric(
            "✅ Completed",
            completed_tasks
        )

    with col4:
        st.metric(
            "💗 Workload",
            workload
        )

    st.divider()

    # ---------------------------------------------
    # WORKLOAD MESSAGE
    # ---------------------------------------------

    st.subheader("💗 Your Current Workload")

    message = app.analyzer.get_workload_message(
        workload
    )

    if workload == "LOW":

        st.success(message)

    elif workload == "MODERATE":

        st.warning(message)

    else:

        st.error(message)

    st.markdown(
        f"""
        <div class="pink-card">
            <strong>Workload Balance Score</strong>
            <h2>{score}</h2>
            <p>
            This score is based on task priority,
            deadline proximity, and estimated study time.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer">
            Made with 💗 for students who want to stay organized.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ADD TASK
# =========================================================

elif page == "➕ Add Task":

    st.title("➕ Add a New Task")

    st.write(
        "Add your academic task and let Planly help "
        "you organize your workload."
    )

    st.divider()

    with st.form("add_task_form"):

        task_name = st.text_input(
            "📚 Task Name",
            placeholder="Example: Research Paper"
        )

        subject = st.text_input(
            "📖 Subject / Course",
            placeholder="Example: Computer Science"
        )

        priority = st.selectbox(
            "💗 Priority",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        deadline = st.date_input(
            "📅 Deadline",
            min_value=date.today()
        )

        estimated_hours = st.number_input(
            "⏰ Estimated Study Time (hours)",
            min_value=0.5,
            max_value=24.0,
            value=1.0,
            step=0.5
        )

        st.write("")

        submitted = st.form_submit_button(
            "🎀 Add Task"
        )

        if submitted:

            if not task_name.strip():

                st.error(
                    "Please enter a task name."
                )

            elif not subject.strip():

                st.error(
                    "Please enter a subject."
                )

            else:

                app.add_task(
                    task_name,
                    subject,
                    priority,
                    deadline,
                    estimated_hours
                )

                st.success(
                    f"🎀 '{task_name}' has been added to Planly!"
                )


# =========================================================
# MY TASKS
# =========================================================

elif page == "📝 My Tasks":

    st.title("📝 My Tasks")

    st.write(
        "View and manage all your academic tasks."
    )

    st.divider()

    if not app.student.tasks:

        st.info(
            "💗 No tasks yet. Go to 'Add Task' "
            "to create your first task."
        )

    else:

        for index, task in enumerate(
            app.student.tasks
        ):

            st.markdown(
                '<div class="task-card">',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(
                [3, 2, 1]
            )

            with col1:

                if task.completed:

                    st.markdown(
                        f"### ✅ {task.name}"
                    )

                else:

                    st.markdown(
                        f"### 📌 {task.name}"
                    )

                st.write(
                    f"**Subject:** {task.subject}"
                )

            with col2:

                st.write(
                    f"**Priority:** "
                    f"{task.priority}"
                )

                st.write(
                    f"**Deadline:** "
                    f"{task.deadline}"
                )

                st.write(
                    f"**Study Time:** "
                    f"{task.estimated_hours} hour(s)"
                )

            with col3:

                if task.completed:

                    st.success(
                        "Completed"
                    )

                else:

                    if st.button(
                        "✅ Complete",
                        key=f"complete_{index}"
                    ):

                        app.complete_task(index)

                        st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# =========================================================
# WORKLOAD BALANCE
# =========================================================

elif page == "⚖️ Workload Balance":

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


# =========================================================
# STUDY SCHEDULE
# =========================================================

elif page == "📅 Study Schedule":

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