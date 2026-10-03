import time
import streamlit as st
from models.student import Student
from controllers.task_controller import TaskController
from controllers.focus_controller import FocusController
from ui.components import html, page_header, section_title, stat_card, empty_state

DURATION_OPTIONS = [15, 25, 45, 60]
GENERAL_STUDY = "General Study"


def _timer_running() -> bool:
    return st.session_state.get("focus_active", False)


def _remaining_seconds() -> int:
    if st.session_state.focus_paused:
        return st.session_state.focus_remaining
    return max(0, int(round(st.session_state.focus_end - time.time())))


def _start_timer(minutes: int, task):
    st.session_state.focus_active = True
    st.session_state.focus_paused = False
    st.session_state.focus_total = minutes * 60
    st.session_state.focus_end = time.time() + minutes * 60
    st.session_state.focus_task_id = task.task_id if task else None
    st.session_state.focus_subject = task.subject if task else GENERAL_STUDY
    st.session_state.focus_title = task.title if task else GENERAL_STUDY


def _clear_timer():
    for key in ["focus_active", "focus_paused", "focus_total", "focus_end",
                "focus_remaining", "focus_task_id", "focus_subject", "focus_title"]:
        st.session_state.pop(key, None)


def _pause_timer(remaining: int):
    st.session_state.focus_remaining = remaining
    st.session_state.focus_paused = True


def _resume_timer():
    st.session_state.focus_end = time.time() + st.session_state.focus_remaining
    st.session_state.focus_paused = False


def _save_session(student: Student, minutes: int):
    ok, msg = FocusController.record_focus_session(
        student_id=student.student_id,
        task_id=st.session_state.focus_task_id,
        duration=minutes,
        subject=st.session_state.focus_subject,
        task_title=st.session_state.focus_title,
    )
    st.session_state.focus_flash = (ok, f"{msg} ({FocusController.format_duration(minutes)})")
    _clear_timer()


@st.fragment(run_every=1)
def _render_active_timer(student: Student):
    remaining = _remaining_seconds()
    total = st.session_state.focus_total

    if remaining <= 0 and not st.session_state.focus_paused:
        _save_session(student, total // 60)
        st.session_state.focus_celebrate = True
        st.rerun()

    mins, secs = divmod(remaining, 60)
    status = "Paused" if st.session_state.focus_paused else "Focusing on"
    html(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 16px; padding: 2rem; text-align: center; box-shadow: 0 4px 14px rgba(217, 108, 157, 0.06); margin-bottom: 1rem;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.08em;">
                {status}
            </div>
            <div style="font-size: 1.05rem; font-weight: 600; color: #3B3036; margin: 0.3rem 0 0.8rem 0;">
                {st.session_state.focus_title}
            </div>
            <div style="font-size: 4.5rem; font-weight: 800; color: #D96C9D; line-height: 1; font-variant-numeric: tabular-nums;">
                {mins:02d}:{secs:02d}
            </div>
        </div>
        """
    )
    st.progress(1 - remaining / total if total else 0.0)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.session_state.focus_paused:
            if st.button("Resume", type="primary", use_container_width=True, key="focus_resume"):
                _resume_timer()
                st.rerun()
        else:
            if st.button("Pause", use_container_width=True, key="focus_pause"):
                _pause_timer(remaining)
                st.rerun()
    with c2:
        if st.button("End & Save", use_container_width=True, key="focus_finish"):
            elapsed_minutes = (total - remaining) // 60
            if elapsed_minutes >= 1:
                _save_session(student, elapsed_minutes)
            else:
                _clear_timer()
                st.session_state.focus_flash = (False, "Session was under a minute, so it wasn't saved.")
            st.rerun()
    with c3:
        if st.button("Cancel", use_container_width=True, key="focus_cancel"):
            _clear_timer()
            st.rerun()


def _render_setup(student: Student):
    pending = [t for t in TaskController.get_student_tasks(student.student_id) if not t.completed]
    options = [None] + pending

    with st.form(key="focus_setup_form"):
        c1, c2 = st.columns([2, 1])
        with c1:
            task = st.selectbox(
                "What are you working on?",
                options=options,
                format_func=lambda t: GENERAL_STUDY if t is None else f"{t.title} ({t.subject})",
            )
        with c2:
            minutes = st.selectbox(
                "Session length",
                options=DURATION_OPTIONS,
                index=DURATION_OPTIONS.index(25),
                format_func=lambda m: f"{m} minutes",
            )
        if st.form_submit_button("Start Focus Session", type="primary", use_container_width=True):
            _start_timer(minutes, task)
            st.rerun()


def _render_recent_sessions(sessions):
    section_title("Recent Sessions", margin="1.2rem 0 0.7rem 0")
    if not sessions:
        empty_state("No focus sessions yet. Start one above to begin tracking your study time.")
        return
    newest_first = sorted(reversed(sessions), key=lambda s: s.session_date, reverse=True)
    for s in newest_first[:5]:
        html(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; padding: 0.8rem 1.1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; color: #3B3036; font-size: 0.92rem;">{s.task_title or s.subject or GENERAL_STUDY}</div>
                    <div style="font-size: 0.8rem; color: #8A737D;">{s.session_date}</div>
                </div>
                <span style="background-color: #FCE8F0; color: #C95A8D; padding: 3px 9px; border-radius: 6px; font-size: 0.8rem; font-weight: 600;">
                    {FocusController.format_duration(s.duration)}
                </span>
            </div>
            """
        )


def render_focus_view(student: Student):
    page_header("Focus", "Pick a task, start the timer, and build steady study habits.")

    flash = st.session_state.pop("focus_flash", None)
    if flash:
        ok, msg = flash
        (st.success if ok else st.info)(msg)
    if st.session_state.pop("focus_celebrate", False):
        st.balloons()

    summary = FocusController.get_weekly_focus_summary(student.student_id)
    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("Sessions This Week", summary["weekly_sessions"], "Completed focus sessions")
    with c2:
        stat_card("Focus Time This Week", summary["formatted_weekly_time"], "Last 7 days", "#D96C9D")
    with c3:
        stat_card("Total Focus Time", summary["formatted_total_time"], "All sessions", "#C95A8D")

    st.write("")

    if _timer_running():
        _render_active_timer(student)
    else:
        _render_setup(student)

    _render_recent_sessions(summary["all_sessions"])


FLOATING_TIMER_CSS = """
<style>
    .st-key-floating_timer {
        position: fixed;
        bottom: 1.5rem;
        right: 1.5rem;
        z-index: 1000;
        width: 270px;
        background-color: #FFFFFF;
        border: 1px solid #F3B6CF;
        border-radius: 16px;
        padding: 0.9rem 1rem;
        box-shadow: 0 8px 24px rgba(217, 108, 157, 0.18);
        gap: 0.5rem;
        cursor: grab;
        user-select: none;
        touch-action: none;
    }
    .st-key-floating_timer.ft-dragging {
        cursor: grabbing;
    }
    .st-key-ft_drag_script {
        display: none;
    }
    .st-key-floating_timer:has(.ft-collapsed) {
        width: 190px;
        padding: 0.6rem 0.8rem;
    }
    .st-key-floating_timer .stButton > button {
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        min-height: 0;
    }
</style>
"""

# Injected into the page with st.html. Dragging starts
# anywhere on the widget except its buttons; the position is kept in
# localStorage and applied through an injected <style> so it survives reruns.
FLOATING_TIMER_DRAG_JS = """
<script>
(function () {
    const win = window;
    const doc = document;
    const STORAGE_KEY = "planly_focus_timer_pos";
    const SELECTOR = ".st-key-floating_timer";

    let styleEl = doc.getElementById("ft-pos-style");
    if (!styleEl) {
        styleEl = doc.createElement("style");
        styleEl.id = "ft-pos-style";
        doc.head.appendChild(styleEl);
    }

    function applyPos(pos) {
        styleEl.textContent = pos
            ? `${SELECTOR} { left: ${pos.x}px !important; top: ${pos.y}px !important; right: auto !important; bottom: auto !important; }`
            : "";
    }

    function clamp(x, y, el) {
        const maxX = win.innerWidth - el.offsetWidth;
        const maxY = win.innerHeight - el.offsetHeight;
        return { x: Math.max(0, Math.min(x, maxX)), y: Math.max(0, Math.min(y, maxY)) };
    }

    try { applyPos(JSON.parse(win.localStorage.getItem(STORAGE_KEY))); } catch (e) {}

    // Replace handlers from a previous run so only one set is active.
    if (win.__ftDragCleanup) win.__ftDragCleanup();

    let drag = null;

    function onDown(e) {
        const el = e.target.closest(SELECTOR);
        if (!el || e.button !== 0 || e.target.closest("button")) return;
        const rect = el.getBoundingClientRect();
        drag = { el, dx: e.clientX - rect.left, dy: e.clientY - rect.top, pos: null };
        el.classList.add("ft-dragging");
        e.preventDefault();
    }

    function onMove(e) {
        if (!drag) return;
        drag.pos = clamp(e.clientX - drag.dx, e.clientY - drag.dy, drag.el);
        applyPos(drag.pos);
    }

    function onUp() {
        if (!drag) return;
        drag.el.classList.remove("ft-dragging");
        if (drag.pos) {
            try { win.localStorage.setItem(STORAGE_KEY, JSON.stringify(drag.pos)); } catch (e) {}
        }
        drag = null;
    }

    doc.addEventListener("pointerdown", onDown);
    doc.addEventListener("pointermove", onMove);
    doc.addEventListener("pointerup", onUp);
    win.__ftDragCleanup = function () {
        doc.removeEventListener("pointerdown", onDown);
        doc.removeEventListener("pointermove", onMove);
        doc.removeEventListener("pointerup", onUp);
    };
})();
</script>
"""


@st.fragment(run_every=1)
def _render_floating_timer_widget(student: Student):
    if not _timer_running():
        # Ended elsewhere (e.g. Focus page) - refresh so the widget disappears.
        st.rerun()

    remaining = _remaining_seconds()
    total = st.session_state.focus_total

    if remaining <= 0 and not st.session_state.focus_paused:
        _save_session(student, total // 60)
        st.rerun()

    mins, secs = divmod(remaining, 60)
    paused = st.session_state.focus_paused
    collapsed = st.session_state.get("focus_mini_collapsed", False)

    with st.container(key="floating_timer"):
        if collapsed:
            c1, c2 = st.columns([3, 2], vertical_alignment="center")
            with c1:
                html(
                    f"""
                    <div class="ft-collapsed" style="font-size: 1.25rem; font-weight: 800; color: #D96C9D; font-variant-numeric: tabular-nums;">
                        {"⏸" if paused else "⏱"} {mins:02d}:{secs:02d}
                    </div>
                    """
                )
            with c2:
                if st.button("Show", key="ft_expand", use_container_width=True):
                    st.session_state.focus_mini_collapsed = False
                    st.rerun()
            return

        html(
            f"""
            <div style="font-size: 0.7rem; font-weight: 700; color: #C95A8D; text-transform: uppercase; letter-spacing: 0.08em;">
                {"Paused" if paused else "Focusing on"}
            </div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #3B3036; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {st.session_state.focus_title}
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #D96C9D; line-height: 1.1; font-variant-numeric: tabular-nums;">
                {mins:02d}:{secs:02d}
            </div>
            """
        )
        st.progress(1 - remaining / total if total else 0.0)

        c1, c2, c3 = st.columns(3)
        with c1:
            if paused:
                if st.button("Resume", type="primary", key="ft_resume", use_container_width=True):
                    _resume_timer()
                    st.rerun()
            elif st.button("Pause", key="ft_pause", use_container_width=True):
                _pause_timer(remaining)
                st.rerun()
        with c2:
            if st.button("Open", key="ft_open", use_container_width=True):
                st.session_state.page_to_navigate = "Focus"
                st.rerun()
        with c3:
            if st.button("Hide", key="ft_collapse", use_container_width=True):
                st.session_state.focus_mini_collapsed = True
                st.rerun()


def render_floating_timer(student: Student):
    """Mini timer shown on every page except Focus, only while a session is active."""
    flash = st.session_state.pop("focus_flash", None)
    if flash:
        ok, msg = flash
        st.toast(msg, icon="🎉" if ok else "ℹ️")

    if not _timer_running():
        return

    html(FLOATING_TIMER_CSS)
    with st.container(key="ft_drag_script"):
        st.html(FLOATING_TIMER_DRAG_JS, unsafe_allow_javascript=True)
    _render_floating_timer_widget(student)
