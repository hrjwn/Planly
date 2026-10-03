"""HTML for the Task Roadmap cards on the My Progress page."""
from html import escape
from ui.components import deadline_style


def _roadmap_node_html(label: str, symbol: str, state: str) -> str:
    """One stop on the roadmap. state: done | current | todo | goal | goal-done."""
    styles = {
        "done": ("#D96C9D", "#D96C9D", "#FFFFFF", "#8A737D", ""),
        "current": ("#FFFFFF", "#D96C9D", "#D96C9D", "#3B3036", "box-shadow: 0 0 0 4px rgba(217, 108, 157, 0.18);"),
        "todo": ("#FFFFFF", "#E5D3DB", "#B9A5AE", "#8A737D", ""),
        "goal": ("#FFF7FA", "#C95A8D", "#C95A8D", "#3B3036", ""),
        "goal-done": ("#C95A8D", "#C95A8D", "#FFFFFF", "#3B3036", ""),
    }
    bg, border, fg, text, extra = styles[state]
    weight = "700" if state in ("current", "goal", "goal-done") else "500"
    return (
        f'<div style="display: flex; flex-direction: column; align-items: center; width: 96px; flex-shrink: 0;">'
        f'<div style="width: 30px; height: 30px; border-radius: 50%; background-color: {bg}; border: 2px solid {border}; color: {fg}; '
        f'display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700; {extra}">{symbol}</div>'
        f'<div style="margin-top: 0.4rem; font-size: 0.75rem; color: {text}; font-weight: {weight}; text-align: center; line-height: 1.25; '
        f'word-break: break-word;">{label}</div>'
        f'</div>'
    )


def _roadmap_connector_html(filled: bool) -> str:
    color = "#D96C9D" if filled else "#F3E1E9"
    return (
        f'<div style="flex: 1 0 24px; height: 3px; background-color: {color}; margin-top: 14px; '
        f'margin-left: -30px; margin-right: -30px; border-radius: 2px;"></div>'
    )


def roadmap_card_html(entry: dict) -> str:
    task = entry["task"]
    steps = entry["steps"]
    pct = entry["percentage"]
    current = entry["current_index"]
    is_done = task.is_completed()

    if is_done:
        status_label, status_style = "Completed", "background-color: #FDF2F8; color: #9D174D;"
    else:
        status_label = task.get_deadline_label()
        status_style = deadline_style(task.days_until_deadline())

    nodes = []
    for i, step in enumerate(steps):
        if step.completed:
            state, symbol = "done", "✓"
        elif i == current:
            state, symbol = "current", str(i + 1)
        else:
            state, symbol = "todo", str(i + 1)
        if i > 0:
            nodes.append(_roadmap_connector_html(steps[i - 1].completed))
        nodes.append(_roadmap_node_html(escape(step.title), symbol, state))

    if steps:
        nodes.append(_roadmap_connector_html(all(s.completed for s in steps)))
    nodes.append(_roadmap_node_html(f"Goal<br>{escape(task.deadline)}", "★", "goal-done" if is_done else "goal"))

    if steps:
        steps_caption = f"{entry['done_steps']} of {entry['total_steps']} steps done"
        if current is not None:
            steps_caption += f" • Next: <b style='color: #3B3036;'>{escape(steps[current].title)}</b>"
    else:
        steps_caption = "No steps yet — break this task into steps on the My Tasks page."

    # Tasks without steps stay compact: just the header, caption and bar.
    nodes_html = (
        f'<div style="display: flex; align-items: flex-start; overflow-x: auto; padding: 0.2rem 0 0.3rem 0; margin-top: 0.9rem;">{"".join(nodes)}</div>'
        if steps else ""
    )

    return f"""<div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 0.8rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04);">
<div style="display: flex; justify-content: space-between; align-items: center; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 0.25rem;">
<div style="font-weight: 700; color: #3B3036; font-size: 1rem;">{escape(task.title)}</div>
<div style="display: flex; gap: 6px; align-items: center;">
<span style="{status_style} padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">{status_label}</span>
<span style="font-size: 0.85rem; font-weight: 700; color: #D96C9D;">{pct}%</span>
</div>
</div>
<div style="font-size: 0.8rem; color: #8A737D; margin-bottom: 0.6rem;">{escape(task.subject)} • {task.priority} Priority • {steps_caption}</div>
<div style="width: 100%; height: 6px; background-color: #FFF7FA; border: 1px solid #F3B6CF; border-radius: 8px; overflow: hidden;">
<div style="width: {pct}%; height: 100%; background-color: #D96C9D;"></div>
</div>{nodes_html}
</div>"""
