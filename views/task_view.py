from datetime import date
import streamlit as st
from models.student import Student
from controllers.task_controller import TaskController
from ui.components import html, page_header, empty_state, priority_badge_style, deadline_badge

PRIORITY_OPTIONS = ["High", "Medium", "Low"]
PRIORITY_ORDER = {p: i for i, p in enumerate(PRIORITY_OPTIONS)}


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
                    placeholder="e.g., Programming Activity / Database Assignment",
                )
                subject = st.text_input(
                    "Subject / Course",
                    placeholder="e.g., Computer Science / Data Structures",
                )

            with col_t2:
                deadline = st.date_input(
                    "Deadline",
                    value=date.today(),
                    min_value=date(2020, 1, 1),
                )
                priority = st.selectbox(
                    "Priority Level",
                    options=PRIORITY_OPTIONS,
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
        html(
            """
            <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 16px; padding: 2.5rem; text-align: center; margin: 1.5rem 0;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #3B3036; margin-bottom: 0.4rem;">
                    No tasks yet
                </div>
                <div style="font-size: 0.92rem; color: #8A737D; margin-bottom: 1.2rem;">
                    Start by adding your first academic task using the form above.
                </div>
            </div>
            """
        )
        return

    all_subjects = sorted(list(set(t.subject.strip() for t in tasks if t.subject and t.subject.strip())))

    html(
        """
        <div style="font-size: 0.9rem; font-weight: 600; color: #8A737D; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">
            Filter and Sort Controls
        </div>
        """
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
            options=["All Priorities"] + PRIORITY_OPTIONS,
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
            return (t.deadline_date() or date.max, t.title)
        elif sort_by == "Priority":
            return (PRIORITY_ORDER.get(t.priority, 1), t.deadline)
        elif sort_by == "Status":
            return (0 if not t.completed else 1, t.deadline)
        return t.deadline

    filtered_tasks = sorted(filtered_tasks, key=sort_key)

    html(
        f"""
        <div style="font-size: 0.85rem; color: #8A737D; margin-top: 0.4rem; margin-bottom: 0.8rem;">
            Showing <b style="color: #3B3036;">{len(filtered_tasks)}</b> of <b style="color: #3B3036;">{len(tasks)}</b> tasks
        </div>
        """
    )

    if not filtered_tasks:
        empty_state(
            "No tasks match your filter criteria. Try clearing the search or changing the filters.",
            padding="2rem",
        )
        return

    editing_id = st.session_state.get("editing_task_id", None)

    for task in filtered_tasks:
        is_editing = (editing_id == task.task_id)

        if is_editing:
            html(
                f"""
                <div style="background-color: #FFF7FA; border: 1.5px solid #D96C9D; border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem; box-shadow: 0 4px 12px rgba(217, 108, 157, 0.1);">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #D96C9D; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem;">
                        Editing Task: {task.title}
                    </div>
                </div>
                """
            )
            with st.form(key=f"edit_form_{task.task_id}"):
                ec1, ec2 = st.columns([2, 1])
                with ec1:
                    edit_title = st.text_input("Task Title", value=task.title)
                    edit_subject = st.text_input("Subject / Course", value=task.subject)
                with ec2:
                    edit_deadline = st.date_input("Deadline", value=task.deadline_date() or date.today())
                    edit_priority = st.selectbox(
                        "Priority",
                        options=PRIORITY_OPTIONS,
                        index=PRIORITY_ORDER.get(task.priority, 1),
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
            is_done = task.is_completed()

            priority_style = priority_badge_style(task.priority)

            if is_done:
                status_badge = "<span style='background-color: #FDF2F8; color: #9D174D; border: 1px solid #FBCFE8; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>Completed</span>"
                title_style = "text-decoration: line-through; color: #8A737D;"
                urgency_badge = ""
            else:
                status_badge = "<span style='background-color: #FCE8F0; color: #C95A8D; border: 1px solid #F3B6CF; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>Pending</span>"
                title_style = "color: #3B3036; font-weight: 600;"

                days_left = task.days_until_deadline()
                if days_left > 1:
                    urgency_badge = f"<span style='color: #8A737D; font-size: 0.8rem;'>Due in {days_left}d</span>"
                else:
                    badge_text, badge_style = deadline_badge(days_left)
                    urgency_badge = f"<span style='{badge_style} padding: 2px 7px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>{badge_text}</span>"

            html(
                f"""
                <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 1.1rem 1.3rem; margin-bottom: 0.6rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            {status_badge}
                            <span style="{priority_style} padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">{task.priority} Priority</span>
                        </div>
                        <div>
                            {urgency_badge}
                        </div>
                    </div>
                    <div style="font-size: 1.05rem; margin-bottom: 0.35rem; {title_style}">
                        {task.title}
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px; font-size: 0.83rem; color: #8A737D;">
                        <span>Subject: <b style="color: #3B3036;">{task.subject}</b></span>
                        <span>•</span>
                        <span>Deadline: <b style="color: #3B3036;">{task.deadline}</b></span>
                    </div>
                </div>
                """
            )

            btn_col_toggle, btn_col_edit, btn_col_delete = st.columns([1.5, 1, 1])

            with btn_col_toggle:
                toggle_btn_label = "Mark Incomplete" if is_done else "Mark Complete"
                if st.button(toggle_btn_label, key=f"tgl_{task.task_id}", use_container_width=True):
                    ok, msg = TaskController.toggle_task_completion(task)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            with btn_col_edit:
                if st.button("Edit", key=f"edt_{task.task_id}", use_container_width=True):
                    st.session_state.editing_task_id = task.task_id
                    st.rerun()

            with btn_col_delete:
                if st.button("Delete", key=f"del_{task.task_id}", use_container_width=True):
                    ok, msg = TaskController.delete_task(task.task_id)
                    if ok:
                        st.warning(msg)
                        st.rerun()
                    else:
                        st.error(msg)