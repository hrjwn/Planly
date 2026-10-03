from datetime import date, datetime
import streamlit as st
from models.student import Student
from controllers.task_controller import TaskController
from controllers.subtask_controller import SubtaskController
from ui.components import page_header
from views.task_card import inject_task_card_styles, render_task_card

def render_task_view(student: Student):
    page_header(
        "My Tasks",
        "Organize your academic assignments, set deadlines, and track your completion status.",
    )

    should_expand_add = st.session_state.get("open_add_task", False)
    if should_expand_add:
        st.session_state.open_add_task = False

    with st.expander("Add New Academic Task", expanded=should_expand_add):
        with st.form(key="add_task_form", clear_on_submit=True):
            col_t1, col_t2 = st.columns([2, 1])

            with col_t1:
                title = st.text_input(
                    "Task Title",
                    placeholder="Enter your Assignment/Project here",
                )
                subject = st.text_input(
                    "Subject / Course",
                    placeholder="Enter your Subject/Course here",
                )

            with col_t2:
                deadline = st.date_input(
                    "Deadline",
                    value=date.today(),
                    min_value=date(2020, 1, 1),
                )
                priority = st.selectbox(
                    "Priority Level",
                    options=["High", "Medium", "Low"],
                    index=1,
                )

            submit_add = st.form_submit_button(
                "Save Task", type="primary", use_container_width=True
            )

            if submit_add:
                success, msg = TaskController.create_task(
                    student_id=student.student_id,
                    title=title,
                    subject=subject,
                    deadline=deadline,
                    priority=priority,
                )
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    st.write("")

    tasks = TaskController.get_student_tasks(student.student_id)

    if not tasks:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 16px; padding: 2.5rem; text-align: center; margin: 1.5rem 0;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #3B3036; margin-bottom: 0.4rem;">
                    No tasks yet
                </div>
                <div style="font-size: 0.92rem; color: #8A737D; margin-bottom: 1.2rem;">
                    Start by adding your first academic task using the form above.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    all_subjects = sorted(list(set(t.subject.strip() for t in tasks if t.subject and t.subject.strip())))

    st.markdown(
        """
        <div style="font-size: 0.9rem; font-weight: 600; color: #8A737D; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">
            Filter and Sort Controls
        </div>
        """,
        unsafe_allow_html=True,
    )

    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1.6, 1.1, 1.1, 1.1, 1.1])

    with f_col1:
        search_query = st.text_input(
            "Search",
            placeholder="Search title or subject...",
            label_visibility="collapsed",
            key="task_search",
        ).strip().lower()

    with f_col2:
        status_filter = st.selectbox(
            "Status",
            options=["All Statuses", "Pending", "Completed"],
            label_visibility="collapsed",
            key="task_status_filter",
        )

    with f_col3:
        priority_filter = st.selectbox(
            "Priority",
            options=["All Priorities", "High", "Medium", "Low"],
            label_visibility="collapsed",
            key="task_priority_filter",
        )

    with f_col4:
        subject_options = ["All Subjects"] + all_subjects
        subject_filter = st.selectbox(
            "Subject",
            options=subject_options,
            label_visibility="collapsed",
            key="task_subject_filter",
        )

    with f_col5:
        sort_by = st.selectbox(
            "Sort by",
            options=["Deadline", "Priority", "Status"],
            label_visibility="collapsed",
            key="task_sort_by",
        )

    filtered_tasks = tasks

    if search_query:
        filtered_tasks = [
            t for t in filtered_tasks
            if search_query in t.title.lower() or search_query in t.subject.lower()
        ]

    if status_filter == "Pending":
        filtered_tasks = [t for t in filtered_tasks if not t.completed]
    elif status_filter == "Completed":
        filtered_tasks = [t for t in filtered_tasks if t.completed]

    if priority_filter != "All Priorities":
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority_filter]

    if subject_filter != "All Subjects":
        filtered_tasks = [t for t in filtered_tasks if t.subject.strip() == subject_filter]

    def sort_key(t):
        if sort_by == "Deadline":
            try:
                return (datetime.strptime(t.deadline, "%Y-%m-%d").date(), t.title)
            except Exception:
                return (date.max, t.title)
        elif sort_by == "Priority":
            order = {"High": 0, "Medium": 1, "Low": 2}
            return (order.get(t.priority, 1), t.deadline)
        elif sort_by == "Status":
            return (0 if not t.completed else 1, t.deadline)
        return t.deadline

    filtered_tasks = sorted(filtered_tasks, key=sort_key)

    st.markdown(
        f"""
        <div style="font-size: 0.85rem; color: #8A737D; margin-top: 0.4rem; margin-bottom: 0.8rem;">
            Showing <b style="color: #3B3036;">{len(filtered_tasks)}</b> of <b style="color: #3B3036;">{len(tasks)}</b> tasks
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not filtered_tasks:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 2rem; text-align: center; color: #8A737D; font-size: 0.9rem;">
                No tasks match your filter criteria. Try clearing the search or changing the filters.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    editing_id = st.session_state.get("editing_task_id", None)
    if "open_task_ids" not in st.session_state:
        st.session_state.open_task_ids = set()
    inject_task_card_styles()
    subtasks_by_task = SubtaskController.get_student_subtasks(student.student_id)

    for task in filtered_tasks:
        is_editing = (editing_id == task.task_id)

        if is_editing:
            st.markdown(
                f"""
                <div style="background-color: #FFF7FA; border: 1.5px solid #D96C9D; border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem; box-shadow: 0 4px 12px rgba(217, 108, 157, 0.1);">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #D96C9D; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem;">
                        Editing Task: {task.title}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.form(key=f"edit_form_{task.task_id}"):
                ec1, ec2 = st.columns([2, 1])
                with ec1:
                    edit_title = st.text_input("Task Title", value=task.title)
                    edit_subject = st.text_input("Subject / Course", value=task.subject)
                with ec2:
                    try:
                        cur_due = datetime.strptime(task.deadline, "%Y-%m-%d").date()
                    except Exception:
                        cur_due = date.today()
                    edit_deadline = st.date_input("Deadline", value=cur_due)

                    p_indices = {"High": 0, "Medium": 1, "Low": 2}
                    cur_idx = p_indices.get(task.priority, 1)
                    edit_priority = st.selectbox(
                        "Priority",
                        options=["High", "Medium", "Low"],
                        index=cur_idx,
                    )

                edit_status = st.checkbox("Mark as Completed", value=task.completed)

                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    save_edit = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
                with btn_c2:
                    cancel_edit = st.form_submit_button("Cancel", use_container_width=True)

                if save_edit:
                    ok, msg = TaskController.update_task(
                        task_id=task.task_id,
                        title=edit_title,
                        subject=edit_subject,
                        deadline=edit_deadline,
                        priority=edit_priority,
                        completed=edit_status,
                    )
                    if ok:
                        task.update_details(edit_title, edit_subject, edit_deadline, edit_priority, edit_status)
                        st.session_state.editing_task_id = None
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

                if cancel_edit:
                    st.session_state.editing_task_id = None
                    st.rerun()

        else:
            render_task_card(student, task, subtasks_by_task.get(task.task_id, []))
