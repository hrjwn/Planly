from datetime import date, datetime, timedelta
from html import escape
import streamlit as st
from models.student import Student
from controllers.task_controller import TaskController
from controllers.subtask_controller import SubtaskController
from controllers.focus_controller import FocusController
from services.workload_analyzer import WorkloadAnalyzer
from services.recommendation_service import RecommendationService
from ui.components import deadline_style, html
from ui.charts import (
    ACCENT, INK, INK_MUTED, PRIORITY_COLORS,
    card, inject_chart_styles, priority_legend, ring, stat_tile, week_strip,
)

WORKLOAD_PILL = {
    "Low": ("#F0FDF4", "#15803D", "Light load"),
    "Medium": ("#FFF7ED", "#C2410C", "Moderate load"),
    "High": ("#FEF2F2", "#B91C1C", "Heavy load"),
}


def _greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


def _parse(d: str):
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except Exception:
        return None


def render_dashboard(student: Student):
    inject_chart_styles()

    tasks = TaskController.get_student_tasks(student.student_id)
    subtasks_by_task = SubtaskController.get_student_subtasks(student.student_id)
    analysis = WorkloadAnalyzer.analyze(tasks, subtasks_by_task)
    focus = FocusController.get_weekly_focus_summary(student.student_id)

    workload = analysis["workload_level"]
    pct = analysis["completion_percentage"]
    today = date.today()
    week_end = today + timedelta(days=6)

    pending_tasks = analysis["upcoming_tasks"]
    tasks_by_day = {}
    for t in pending_tasks:
        d = _parse(t.deadline)
        if d and today <= d <= week_end:
            tasks_by_day.setdefault(d, []).append(t)
    due_this_week = sum(len(v) for v in tasks_by_day.values())
    overdue = len(analysis["overdue_tasks"])

    # ---------- Hero ----------
    pill_bg, pill_fg, pill_text = WORKLOAD_PILL.get(workload, WORKLOAD_PILL["Low"])
    html(
        f"""<div style="background: linear-gradient(135deg, #FFFFFF 0%, #FFF0F6 100%); border: 1px solid #F3B6CF; border-radius: 20px; padding: 1.6rem 1.9rem; margin-bottom: 1.2rem; display: flex; justify-content: space-between; align-items: center; gap: 1.5rem; flex-wrap: wrap; box-shadow: 0 4px 18px rgba(217, 108, 157, 0.08);">
<div style="flex: 1; min-width: 260px;">
<div class="pl-eyebrow">{today.strftime("%A, %B %d").replace(" 0", " ")}</div>
<div style="font-size: 1.9rem; font-weight: 800; color: {INK}; margin: 0.25rem 0 0.55rem 0; line-height: 1.2;">{_greeting()}, {escape(student.name.split(" ")[0] if student.name else "there")} 👋</div>
<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0.8rem;">
<span style="background: #FFFFFF; border: 1px solid #F3B6CF; color: #C95A8D; padding: 3px 10px; border-radius: 999px; font-size: 0.76rem; font-weight: 600;">🎓 {escape(student.course or "Student")}</span>
<span style="background: {pill_bg}; color: {pill_fg}; padding: 3px 10px; border-radius: 999px; font-size: 0.76rem; font-weight: 700;">● {pill_text}</span>
</div>
<div style="font-size: 0.9rem; color: {INK_MUTED}; max-width: 560px; line-height: 1.5;">{RecommendationService.get_primary_recommendation(workload)}</div>
</div>
<div style="display: flex; align-items: center; gap: 1.1rem;">
{ring(pct, size=128, thickness=13, label="overall")}
<div style="font-size: 0.82rem; color: {INK_MUTED}; line-height: 1.7;">
<div><b style="color: {INK}; font-size: 1rem;">{analysis["completed_tasks"]}</b> of {analysis["total_tasks"]} tasks done</div>
<div><b style="color: {INK}; font-size: 1rem;">{analysis["pending_tasks"]}</b> still pending</div>
</div>
</div>
</div>"""
    )

    # ---------- Stat tiles ----------
    tiles = [
        stat_tile("Pending", analysis["pending_tasks"], "Tasks to finish", "📝"),
        stat_tile("Due this week", due_this_week, "Next 7 days", "📅", "#FFF7ED"),
        stat_tile("Overdue", overdue, "Past their deadline" if overdue else "You're on track", "⏰", "#FEF2F2" if overdue else "#F0FDF4"),
        stat_tile("Focus time", focus["formatted_weekly_time"], f'{focus["weekly_sessions"]} sessions this week', "🎯", "#F5F0FF"),
    ]
    for col, tile in zip(st.columns(4, gap="small"), tiles):
        with col:
            html(tile)

    st.write("")

    # ---------- Quick actions ----------
    with st.container(horizontal=True, gap="small", key="dash_actions"):
        if st.button("＋ Add Task", key="qa_add_task", type="primary"):
            st.session_state.page_to_navigate = "My Tasks"
            st.session_state.open_add_task = True
            st.rerun()
        if st.button("▶ Start Focus", key="qa_start_focus"):
            st.session_state.page_to_navigate = "Focus"
            st.rerun()
        if st.button("📋 My Tasks", key="qa_view_tasks"):
            st.session_state.page_to_navigate = "My Tasks"
            st.rerun()
        if st.button("📈 My Progress", key="qa_view_progress"):
            st.session_state.page_to_navigate = "My Progress"
            st.rerun()

    st.write("")

    col_plan, col_side = st.columns([1.35, 1], gap="medium")

    # ---------- Today's plan ----------
    with col_plan:
        html(
            f"""<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.6rem;">
<div style="font-size: 1.1rem; font-weight: 700; color: {INK};">Today's Plan</div>
<div style="font-size: 0.78rem; color: {INK_MUTED};">Most urgent first</div>
</div>"""
        )

        plan = analysis["todays_plan"][:4]
        if not plan:
            html(card("All caught up ✨", "", f'<div style="font-size: 0.88rem; color: {INK_MUTED};">No active tasks need attention today. Enjoy the breather, or add your next task.</div>'))
        for i, t in enumerate(plan, start=1):
            steps = subtasks_by_task.get(t.task_id, [])
            done = sum(1 for s in steps if s.completed)
            next_step = next((s.title for s in steps if not s.completed), None)
            steps_html = ""
            if steps:
                steps_pct = int(done / len(steps) * 100)
                steps_html = (
                    f'<div style="display: flex; align-items: center; gap: 8px; margin-top: 0.45rem;">'
                    f'<div style="flex: 1; max-width: 160px; height: 6px; background: #FCE8F0; border-radius: 6px; overflow: hidden;">'
                    f'<div style="width: {steps_pct}%; height: 100%; background: {ACCENT};"></div></div>'
                    f'<span style="font-size: 0.74rem; color: {INK_MUTED};">{done}/{len(steps)} steps'
                    + (f' · Next: <b style="color: {INK};">{escape(next_step)}</b>' if next_step else "")
                    + "</span></div>"
                )

            with st.container(border=True, key=f"plan_card_{t.task_id}"):
                c_info, c_btn = st.columns([5, 1.1], vertical_alignment="center")
                with c_info:
                    html(
                        f"""<div style="display: flex; gap: 0.85rem; align-items: flex-start;">
<div style="width: 30px; height: 30px; border-radius: 10px; background: #FCE8F0; color: #C95A8D; font-weight: 800; font-size: 0.85rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">{i}</div>
<div style="flex: 1; min-width: 0;">
<div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
<span style="font-weight: 700; color: {INK}; font-size: 0.95rem;">{escape(t.title)}</span>
<span style="{deadline_style(t.days_until_deadline())} padding: 1px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;">{t.get_deadline_label()}</span>
</div>
<div style="font-size: 0.78rem; color: {INK_MUTED}; margin-top: 0.15rem; display: flex; align-items: center; gap: 6px;">
<span class="pl-swatch" style="background: {PRIORITY_COLORS.get(t.priority, ACCENT)};"></span>{t.priority} priority · {escape(t.subject)}
</div>
{steps_html}
</div>
</div>"""
                    )
                with c_btn:
                    if st.button("Focus", key=f"plan_focus_{t.task_id}", use_container_width=True):
                        st.session_state.focus_target_task_id = t.task_id
                        st.session_state.page_to_navigate = "Focus"
                        st.rerun()

    # ---------- This week + needs attention ----------
    with col_side:
        html(card("This Week", "Each dot is a pending task due that day", week_strip(tasks_by_day, today) + priority_legend()))
        st.write("")

        attention = analysis["needs_attention"][:4]
        if attention:
            rows = []
            for t in attention:
                days_left = t.days_until_deadline()
                if days_left < 0 or days_left <= 2:
                    reason = t.get_deadline_label()
                else:
                    reason = f"{t.priority} priority"
                rows.append(
                    f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; padding: 0.55rem 0; border-bottom: 1px solid #FCE8F0;">'
                    f'<div style="min-width: 0;"><div style="font-size: 0.86rem; font-weight: 600; color: {INK}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{escape(t.title)}</div>'
                    f'<div style="font-size: 0.74rem; color: {INK_MUTED};">{escape(t.subject)}</div></div>'
                    f'<span style="{deadline_style(days_left)} padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; white-space: nowrap;">{reason}</span>'
                    f'</div>'
                )
            body = "".join(rows)
        else:
            body = f'<div style="font-size: 0.86rem; color: {INK_MUTED};">Nothing urgent: no overdue work or deadlines in the next two days. 🎉</div>'
        html(card("Needs Attention", "Overdue, due soon, or high priority", body))

    html(
        """<style>
div[class*="st-key-plan_card_"] {
    border: 1px solid #F3B6CF !important; border-radius: 14px !important; background: #FFFFFF;
    transition: box-shadow 0.15s ease, border-color 0.15s ease;
}
div[class*="st-key-plan_card_"]:hover { border-color: #D96C9D !important; box-shadow: 0 4px 14px rgba(217, 108, 157, 0.12); }
div[class*="st-key-plan_focus_"] button, div[class*="st-key-dash_actions"] button {
    min-height: 0 !important; padding: 0.35rem 0.9rem !important; border-radius: 10px !important;
}
div[class*="st-key-plan_focus_"] button p, div[class*="st-key-dash_actions"] button p { font-size: 0.82rem !important; }
</style>"""
    )
