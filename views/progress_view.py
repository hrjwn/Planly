from datetime import date, datetime, timedelta
from html import escape
import streamlit as st
from models.student import Student
from controllers.task_controller import TaskController
from controllers.subtask_controller import SubtaskController
from controllers.focus_controller import FocusController
from services.workload_analyzer import WorkloadAnalyzer
from services.study_scheduler import StudyScheduler
from services.roadmap_service import RoadmapService
from ui.components import html
from ui.roadmap import roadmap_card_html
from ui.charts import (
    ACCENT, INK, INK_MUTED, PRIORITY_COLORS,
    bar_list, card, column_chart, inject_chart_styles, ring, stat_tile,
)


def _focus_by_day(sessions, today: date):
    minutes = {today - timedelta(days=i): 0 for i in range(6, -1, -1)}
    counts = dict.fromkeys(minutes, 0)
    for s in sessions:
        if not s.completed:
            continue
        try:
            d = datetime.strptime(s.session_date, "%Y-%m-%d").date()
        except Exception:
            continue
        if d in minutes:
            minutes[d] += s.duration
            counts[d] += 1
    return minutes, counts


def render_progress_view(student: Student):
    inject_chart_styles()

    tasks = TaskController.get_student_tasks(student.student_id)
    subtasks_by_task = SubtaskController.get_student_subtasks(student.student_id)
    analysis = WorkloadAnalyzer.analyze(tasks, subtasks_by_task)
    focus_summary = FocusController.get_weekly_focus_summary(student.student_id)

    workload = analysis["workload_level"]
    pct = analysis["completion_percentage"]
    total = analysis["total_tasks"]
    completed = analysis["completed_tasks"]
    today = date.today()

    all_steps = [s for steps in subtasks_by_task.values() for s in steps]
    steps_done = sum(1 for s in all_steps if s.completed)
    pending = [t for t in tasks if not t.is_completed()]
    in_progress = sum(1 for t in pending if any(s.completed for s in subtasks_by_task.get(t.task_id, [])))
    not_started = len(pending) - in_progress
    deadlines_this_week = sum(1 for t in pending if 0 <= t.days_until_deadline() <= 7)

    html(
        f"""<div style="margin-bottom: 1.1rem;">
<h1 style="font-size: 2.2rem; font-weight: 800; color: {INK}; margin-bottom: 0.2rem;">My Progress</h1>
<p style="font-size: 0.95rem; color: {INK_MUTED}; margin: 0;">See how far you've come and what's next.</p>
</div>"""
    )

    # ---------- Hero: ring + status breakdown ----------
    def mini(label, value, color):
        return (
            f'<div style="flex: 1; min-width: 110px; background: #FFF7FA; border-radius: 12px; padding: 0.7rem 0.9rem;">'
            f'<div style="display: flex; align-items: center; gap: 6px; font-size: 0.72rem; font-weight: 700; color: {INK_MUTED}; text-transform: uppercase; letter-spacing: 0.05em;">'
            f'<span class="pl-swatch" style="background: {color};"></span>{label}</div>'
            f'<div style="font-size: 1.5rem; font-weight: 800; color: {INK};">{value}</div></div>'
        )

    if total:
        segments = [("Completed", completed, "#A8417A"), ("In progress", in_progress, ACCENT), ("Not started", not_started, "#F3C6DA")]
        stacked = "".join(
            f'<div class="pl-tip" data-tip="{label}: {n}" style="flex: {n}; background: {c}; height: 100%;"></div>'
            for label, n, c in segments if n
        )
        stacked_bar = f'<div style="display: flex; gap: 2px; height: 10px; border-radius: 6px; overflow: visible; margin: 0.9rem 0 0.8rem 0;">{stacked}</div>'
    else:
        stacked_bar = '<div style="height: 10px; background: #FCE8F0; border-radius: 6px; margin: 0.9rem 0 0.8rem 0;"></div>'

    steps_line = f" · {steps_done} of {len(all_steps)} steps done" if all_steps else ""
    html(
        f"""<div style="background: linear-gradient(135deg, #FFFFFF 0%, #FFF0F6 100%); border: 1px solid #F3B6CF; border-radius: 20px; padding: 1.5rem 1.8rem; margin-bottom: 1.1rem; display: flex; gap: 1.8rem; align-items: center; flex-wrap: wrap; box-shadow: 0 4px 18px rgba(217, 108, 157, 0.08);">
{ring(pct, size=150, thickness=15, label="overall")}
<div style="flex: 1; min-width: 280px;">
<div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem;">
<div>
<div class="pl-eyebrow">Overall progress</div>
<div style="font-size: 1.15rem; font-weight: 700; color: {INK}; margin-top: 0.2rem;">{completed} of {total} tasks completed{steps_line}</div>
</div>
<div style="font-size: 0.8rem; color: {INK_MUTED};">Workload: <b style="color: {INK};">{workload}</b> · {deadlines_this_week} due this week</div>
</div>
{stacked_bar}
<div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
{mini("Completed", completed, "#A8417A")}
{mini("In progress", in_progress, ACCENT)}
{mini("Not started", not_started, "#F3C6DA")}
</div>
</div>
</div>"""
    )

    # ---------- Stat tiles ----------
    overdue = len(analysis["overdue_tasks"])
    tiles = [
        stat_tile("Steps done", f"{steps_done}<span style='font-size: 0.95rem; color: {INK_MUTED}; font-weight: 600;'>/{len(all_steps)}</span>", "Across all tasks", "✅", "#F0FDF4"),
        stat_tile("Overdue", overdue, "Needs catching up" if overdue else "Nothing overdue", "⏰", "#FEF2F2" if overdue else "#F0FDF4"),
        stat_tile("Focus sessions", focus_summary["weekly_sessions"], "Last 7 days", "🎯", "#F5F0FF"),
        stat_tile("Focus time", focus_summary["formatted_weekly_time"], "Last 7 days", "⏱️", "#FFF7ED"),
    ]
    for col, tile in zip(st.columns(4, gap="small"), tiles):
        with col:
            html(tile)

    st.write("")

    _render_roadmap(RoadmapService.build_roadmap(tasks, subtasks_by_task))

    st.write("")

    # ---------- Subjects + priority ----------
    col_subj, col_prio = st.columns([1.3, 1], gap="medium")

    with col_subj:
        subject_progress = analysis["subject_progress"]
        if subject_progress:
            rows = [
                (
                    subj,
                    stats["percentage"],
                    f'<b>{stats["percentage"]:.0f}%</b> · {stats["completed"]}/{stats["total"]} tasks',
                    f'{subj}: {stats["completed"]} of {stats["total"]} tasks done',
                )
                for subj, stats in sorted(subject_progress.items(), key=lambda kv: -kv[1]["percentage"])
            ]
            body = bar_list(rows, max_value=100)
        else:
            body = f'<div style="font-size: 0.86rem; color: {INK_MUTED};">Add tasks with a subject to see your breakdown.</div>'
        html(card("Progress by Subject", "Completed steps count toward each subject", body))

    with col_prio:
        p_counts = analysis["tasks_by_priority"]
        if sum(p_counts.values()):
            rows = [
                (p, p_counts.get(p, 0), f'<b>{p_counts.get(p, 0)}</b> pending', f'{p} priority: {p_counts.get(p, 0)} pending')
                for p in ("High", "Medium", "Low")
            ]
            body = bar_list(rows, colors=PRIORITY_COLORS)
        else:
            body = f'<div style="font-size: 0.86rem; color: {INK_MUTED};">No pending tasks. Everything is done! 🎉</div>'
        html(card("Pending by Priority", "What's left on your plate", body))

    st.write("")

    # ---------- Focus chart + study plan ----------
    col_focus, col_sched = st.columns([1, 1.3], gap="medium")

    with col_focus:
        minutes, counts = _focus_by_day(focus_summary["all_sessions"], today)
        points = [
            (
                "Today" if d == today else d.strftime("%a"),
                m,
                f'{d.strftime("%a %b %d")}: {FocusController.format_duration(m)} · {counts[d]} session{"s" if counts[d] != 1 else ""}',
                d == today,
            )
            for d, m in minutes.items()
        ]
        week_total = sum(minutes.values())
        if week_total:
            body = column_chart(points, unit_label=lambda v: FocusController.format_duration(int(v)))
        else:
            body = (
                f'<div style="height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; '
                f'color: {INK_MUTED}; font-size: 0.86rem; text-align: center; background: #FFF7FA; border-radius: 12px;">'
                f'<div style="font-size: 1.6rem;">🎯</div>No focus sessions in the last 7 days.<br>Start one from the Focus page.</div>'
            )
        html(card("Focus This Week", f"{FocusController.format_duration(week_total)} total over the last 7 days", body))

    with col_sched:
        schedule_data = StudyScheduler.create_schedule(tasks, workload)
        task_schedules = schedule_data["task_schedules"]
        general_tips = schedule_data["general_tips"]

        if task_schedules:
            blocks = []
            for item in task_schedules[:3]:
                t = item["task"]
                steps_html = "".join(
                    f'<div style="display: flex; gap: 0.6rem; margin-bottom: 0.3rem; font-size: 0.8rem;">'
                    f'<span style="flex-shrink: 0; min-width: 78px; font-weight: 700; color: #C95A8D;">{escape(step["day"])}</span>'
                    f'<span style="color: {INK};">{escape(step["activity"])}</span></div>'
                    for step in item["schedule"]
                )
                blocks.append(
                    f'<div style="padding: 0.7rem 0; border-bottom: 1px solid #FCE8F0;">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 0.4rem;">'
                    f'<span style="font-weight: 700; color: {INK}; font-size: 0.9rem;">{escape(t.title)}</span>'
                    f'<span style="background: #FCE8F0; color: #C95A8D; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; white-space: nowrap;">{t.get_deadline_label()}</span>'
                    f'</div>{steps_html}</div>'
                )
            body = "".join(blocks)
        else:
            body = f'<div style="font-size: 0.86rem; color: {INK_MUTED};">No pending tasks to schedule. You are fully caught up!</div>'

        if general_tips:
            tips = "".join(f'<li style="margin-bottom: 0.25rem;">{escape(tip)}</li>' for tip in general_tips[:3])
            body += (
                f'<div style="background: #FFF7FA; border-radius: 12px; padding: 0.8rem 1rem; margin-top: 0.8rem;">'
                f'<div class="pl-eyebrow" style="margin-bottom: 0.3rem;">💡 Pacing tips</div>'
                f'<ul style="margin: 0; padding-left: 1.1rem; font-size: 0.8rem; color: {INK}; line-height: 1.55;">{tips}</ul></div>'
            )
        html(card("Study Plan", "Suggested pacing for your nearest deadlines", body))


def _render_roadmap(roadmap: list):
    st.markdown(
        """
        <div style="font-size: 1.15rem; font-weight: 700; color: #3B3036; margin-bottom: 0.2rem;">
            Task Roadmap
        </div>
        <div style="font-size: 0.85rem; color: #8A737D; margin-bottom: 0.7rem;">
            Each main task and the steps that get you there. Add steps from the My Tasks page.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not roadmap:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: 1.5rem; text-align: center; color: #8A737D; font-size: 0.9rem;">
                No tasks yet. Add a main task and break it into steps to build your roadmap.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    show_completed = st.toggle("Show completed tasks", value=False, key="roadmap_show_completed")
    entries = [e for e in roadmap if show_completed or not e["task"].is_completed()]

    if not entries:
        st.caption("All main tasks are complete. Turn on 'Show completed tasks' to review them.")
        return

    for entry in entries:
        st.markdown(roadmap_card_html(entry), unsafe_allow_html=True)
