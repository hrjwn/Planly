"""A single task on the My Tasks page: header, clickable title, steps and actions.

Each card is a Streamlit fragment, so opening it or ticking a step only redraws
that card instead of rerunning the whole page.
"""
import streamlit as st
from models.student import Student
from models.task import Task
from controllers.task_controller import TaskController
from controllers.subtask_controller import SubtaskController
from ui.components import deadline_style, priority_badge_style

BADGE = "padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 600; white-space: nowrap;"


def _card_header_html(task: Task, steps: list) -> str:
    is_done = task.is_completed()
    priority_style = priority_badge_style(task.priority)

    if is_done:
        status_badge = f"<span style='background-color: #FDF2F8; color: #9D174D; border: 1px solid #FBCFE8; {BADGE}'>Completed</span>"
        urgency_badge = ""
    else:
        status_badge = f"<span style='background-color: #FCE8F0; color: #C95A8D; border: 1px solid #F3B6CF; {BADGE}'>Pending</span>"
        urgency_style = deadline_style(task.days_until_deadline())
        urgency_badge = f"<span style='{urgency_style} {BADGE}'>{task.get_deadline_label()}</span>"

    return f"""<div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; min-height: 24px; padding: 2px 0;">
<div style="display: flex; align-items: center; gap: 6px;">{status_badge}<span style="{priority_style} {BADGE}">{task.priority} Priority</span></div>
<div>{urgency_badge}</div>
</div>"""


def _card_meta_html(task: Task, steps: list) -> str:
    steps_html = ""
    if steps:
        done = sum(1 for s in steps if s.completed)
        pct = int(done / len(steps) * 100)
        steps_html = (
            f'<span style="color: #E5C3D3;">•</span><span>Steps <b style="color: #D96C9D;">{done}/{len(steps)}</b></span>'
            f'<span style="display: inline-block; width: 70px; height: 5px; background-color: #FCE8F0; border-radius: 6px; overflow: hidden;">'
            f'<span style="display: block; width: {pct}%; height: 100%; background-color: #D96C9D;"></span></span>'
        )
    return f"""<div style="display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: #8A737D; flex-wrap: wrap; padding-bottom: 0.15rem;">
<span>Subject <b style="color: #3B3036;">{task.subject}</b></span>
<span style="color: #E5C3D3;">•</span>
<span>Deadline <b style="color: #3B3036;">{task.deadline}</b></span>
{steps_html}
</div>"""


@st.fragment
def render_task_card(student: Student, task: Task, steps: list):
    # Runs as a fragment: opening the card or ticking a step only redraws this card,
    # without refetching every task from the database.
    is_done = task.is_completed()
    is_open = task.task_id in st.session_state.open_task_ids

    with st.container(border=True, key=f"task_card_{task.task_id}"):
        st.markdown(_card_header_html(task, steps), unsafe_allow_html=True)

        chevron = "▾" if is_open else "▸"
        title_label = f"~~{task.title}~~" if is_done else task.title
        st.button(
            f"{chevron}  {title_label}",
            key=f"open_{task.task_id}",
            type="tertiary",
            use_container_width=True,
            on_click=_toggle_open,
            args=(task.task_id,),
        )

        st.markdown(_card_meta_html(task, steps), unsafe_allow_html=True)

        if is_open:
            _render_steps(student, task, steps)

        with st.container(horizontal=True, horizontal_alignment="right", gap="small", key=f"task_actions_{task.task_id}"):
            toggle_btn_label = "Mark Incomplete" if is_done else "Mark Complete"
            if st.button(toggle_btn_label, key=f"tgl_{task.task_id}", type="primary" if not is_done else "secondary"):
                ok, msg = TaskController.toggle_task_completion(task)
                if ok:
                    st.rerun()
                else:
                    st.error(msg)

            if not is_done:
                if st.button("Start Focus", key=f"foc_{task.task_id}"):
                    st.session_state.focus_target_task_id = task.task_id
                    st.session_state.page_to_navigate = "Focus"
                    st.rerun()

            if st.button("Edit", key=f"edt_{task.task_id}"):
                st.session_state.editing_task_id = task.task_id
                st.rerun()

            if st.button("Delete", key=f"del_{task.task_id}"):
                ok, msg = TaskController.delete_task(task.task_id)
                if ok:
                    st.rerun()
                else:
                    st.error(msg)


def _toggle_open(task_id: str):
    open_ids = st.session_state.open_task_ids
    if task_id in open_ids:
        open_ids.discard(task_id)
    else:
        open_ids.add(task_id)


def _sync_local_task(task: Task, steps: list):
    """Mirror SubtaskController's parent sync so the card updates without a refetch."""
    if steps:
        task.completed = all(s.completed for s in steps)


def _on_step_toggled(step, task: Task, steps: list):
    checked = st.session_state[f"sub_{step.subtask_id}"]
    ok, msg = SubtaskController.set_subtask_completion(step, checked)
    if ok:
        _sync_local_task(task, steps)
    else:
        # Shown by _render_steps; displaying elements inside a fragment callback is unsupported.
        st.session_state[f"step_error_{task.task_id}"] = msg


def _reload_steps(task: Task, steps: list):
    steps[:] = SubtaskController.get_task_subtasks(task.task_id)
    _sync_local_task(task, steps)


def _render_steps(student: Student, task: Task, steps: list):
    with st.container(key=f"task_steps_{task.task_id}"):
        st.markdown(
            """<div style="font-size: 0.72rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.06em; line-height: 1.6; padding: 2px 0;">Steps</div>""",
            unsafe_allow_html=True,
        )

        error = st.session_state.pop(f"step_error_{task.task_id}", None)
        if error:
            st.error(error)

        if not steps:
            st.caption("Split this task into smaller, specific steps. Finishing every step completes the task.")

        for step in steps:
            with st.container(horizontal=True, vertical_alignment="center", gap="small", key=f"step_row_{step.subtask_id}"):
                st.checkbox(
                    f"~~{step.title}~~" if step.completed else step.title,
                    value=step.completed,
                    key=f"sub_{step.subtask_id}",
                    on_change=_on_step_toggled,
                    args=(step, task, steps),
                )
                if st.button(":material/close:", key=f"subdel_{step.subtask_id}", type="tertiary", help="Delete step"):
                    ok, msg = SubtaskController.delete_subtask(step)
                    if ok:
                        _reload_steps(task, steps)
                        st.rerun(scope="fragment")
                    else:
                        st.error(msg)

        with st.form(key=f"add_step_{task.task_id}", clear_on_submit=True, border=False):
            with st.container(horizontal=True, vertical_alignment="center", gap="small"):
                new_step = st.text_input(
                    "New step",
                    placeholder="Add a step, e.g. Research sources, Write outline...",
                    label_visibility="collapsed",
                )
                add_step = st.form_submit_button("+ Add Step")

            if add_step:
                next_position = max((s.position for s in steps), default=-1) + 1
                ok, msg = SubtaskController.create_subtask(
                    student_id=student.student_id,
                    task_id=task.task_id,
                    title=new_step,
                    position=next_position,
                )
                if ok:
                    _reload_steps(task, steps)
                    st.rerun(scope="fragment")
                else:
                    st.error(msg)


def inject_task_card_styles():
    st.markdown(
        """
        <style>
        div[class*="st-key-task_card_"] {
            border: 1px solid #F3B6CF !important;
            border-radius: 14px !important;
            background-color: #FFFFFF;
            box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);
            padding: 0.9rem 1.1rem 0.8rem 1.1rem !important;
            gap: 0.35rem !important;
            transition: box-shadow 0.15s ease-in-out, border-color 0.15s ease-in-out;
        }
        div[class*="st-key-task_card_"]:hover {
            border-color: #D96C9D !important;
            box-shadow: 0 4px 14px rgba(217, 108, 157, 0.12);
        }

        div[class*="st-key-task_card_"] [data-testid="stMarkdown"],
        div[class*="st-key-task_card_"] [data-testid="stMarkdownContainer"] {
            margin: 0 !important;
            overflow: visible;
        }

        /* Clickable title: left aligned, full width, no button chrome */
        div[class*="st-key-open_"] button {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            justify-content: flex-start !important;
            text-align: left !important;
            padding: 0.15rem 0 !important;
            min-height: 0 !important;
            width: 100%;
        }
        div[class*="st-key-open_"] button > div,
        div[class*="st-key-open_"] button [data-testid="stMarkdownContainer"] {
            justify-content: flex-start !important;
            text-align: left !important;
            width: 100%;
        }
        div[class*="st-key-open_"] button p {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            color: #3B3036;
            text-align: left !important;
        }
        div[class*="st-key-open_"] button:hover p {
            color: #D96C9D;
        }

        /* Steps block */
        div[class*="st-key-task_steps_"] {
            border-top: 1px dashed #F3B6CF;
            margin-top: 0.3rem;
            padding-top: 0.55rem;
            gap: 0.25rem !important;
        }
        div[class*="st-key-step_row_"] {
            padding: 0.1rem 0.4rem;
            border-radius: 8px;
            justify-content: space-between;
        }
        div[class*="st-key-step_row_"]:hover {
            background-color: #FFF7FA;
        }
        div[class*="st-key-step_row_"] [data-testid="stCheckbox"] p {
            font-size: 0.9rem;
        }
        div[class*="st-key-subdel_"] button {
            min-height: 0 !important;
            padding: 0 0.3rem !important;
        }
        div[class*="st-key-subdel_"] button p {
            color: #B9A5AE;
            font-size: 0.85rem;
        }
        div[class*="st-key-subdel_"] button:hover p {
            color: #B91C1C;
        }
        div[class*="st-key-task_steps_"] [data-testid="stForm"] button {
            min-height: 2.1rem;
            padding: 0.2rem 0.9rem;
            white-space: nowrap;
        }

        /* Small action buttons, grouped on the right */
        div[class*="st-key-task_actions_"] {
            border-top: 1px solid #FCE8F0;
            margin-top: 0.3rem;
            padding-top: 0.6rem;
        }
        div[class*="st-key-task_actions_"] button {
            min-height: 0 !important;
            height: auto !important;
            padding: 0.25rem 0.75rem !important;
            border-radius: 8px !important;
        }
        div[class*="st-key-task_actions_"] button p {
            font-size: 0.78rem !important;
            font-weight: 600;
        }
        div[class*="st-key-del_"] button:hover {
            border-color: #B91C1C !important;
            background-color: #FEF2F2 !important;
        }
        div[class*="st-key-del_"] button:hover p {
            color: #B91C1C !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
