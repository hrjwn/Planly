"""Lightweight HTML/CSS charts and stat tiles (no pandas, no chart library).

Every function returns an HTML string; render it with ui.components.html().
Call inject_chart_styles() once per page before rendering any of them.
"""
from datetime import date, timedelta
from html import escape
from typing import Dict, List, Optional, Sequence, Tuple

import streamlit as st

INK = "#3B3036"
INK_MUTED = "#8A737D"
INK_FAINT = "#B9A5AE"
BORDER = "#F3B6CF"
TRACK = "#FCE8F0"
SURFACE = "#FFFFFF"
ACCENT = "#D96C9D"
ACCENT_DARK = "#C95A8D"

# Ordinal pink ramp: light = low, dark = high. Always shown with a text label.
PRIORITY_COLORS = {"Low": "#F0A3C3", "Medium": "#D96C9D", "High": "#A8417A"}

_CHART_CSS = f"""
<style>
.pl-card {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 16px;
    padding: 1.1rem 1.25rem; box-shadow: 0 2px 10px rgba(217, 108, 157, 0.05);
    height: 100%;
}}
.pl-card-title {{ font-size: 0.95rem; font-weight: 700; color: {INK}; margin: 0 0 0.15rem 0; }}
.pl-card-sub {{ font-size: 0.78rem; color: {INK_MUTED}; margin: 0 0 0.9rem 0; }}
.pl-eyebrow {{
    font-size: 0.7rem; font-weight: 700; color: {ACCENT_DARK};
    text-transform: uppercase; letter-spacing: 0.08em;
}}

/* Hover tooltip */
.pl-tip {{ position: relative; }}
.pl-tip::after {{
    content: attr(data-tip); position: absolute; left: 50%; bottom: calc(100% + 6px);
    transform: translateX(-50%) translateY(4px); white-space: nowrap;
    background: {INK}; color: #FFFFFF; font-size: 0.72rem; font-weight: 600;
    padding: 4px 8px; border-radius: 6px; opacity: 0; pointer-events: none;
    transition: opacity 0.12s ease, transform 0.12s ease; z-index: 20;
}}
.pl-tip:hover::after {{ opacity: 1; transform: translateX(-50%) translateY(0); }}

/* Stat tile */
.pl-stat {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 0.95rem 1.1rem; display: flex; gap: 0.85rem; align-items: center;
    box-shadow: 0 2px 8px rgba(217, 108, 157, 0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.pl-stat:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(217, 108, 157, 0.12); }}
.pl-stat-icon {{
    width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 1.15rem;
}}
.pl-stat-label {{ font-size: 0.7rem; font-weight: 700; color: {INK_MUTED}; text-transform: uppercase; letter-spacing: 0.06em; }}
.pl-stat-value {{ font-size: 1.55rem; font-weight: 800; color: {INK}; line-height: 1.15; }}
.pl-stat-caption {{ font-size: 0.74rem; color: {INK_MUTED}; }}

/* Horizontal bars */
.pl-bar-row {{ margin-bottom: 0.75rem; }}
.pl-bar-row:last-child {{ margin-bottom: 0; }}
.pl-bar-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 0.5rem; margin-bottom: 0.3rem; }}
.pl-bar-label {{ font-size: 0.85rem; font-weight: 600; color: {INK}; display: flex; align-items: center; gap: 0.45rem; }}
.pl-bar-value {{ font-size: 0.8rem; color: {INK_MUTED}; white-space: nowrap; }}
.pl-bar-value b {{ color: {INK}; }}
.pl-bar-track {{ height: 10px; background: {TRACK}; border-radius: 6px; overflow: hidden; }}
.pl-bar-fill {{ height: 100%; border-radius: 6px; transition: width 0.4s ease; }}
.pl-swatch {{ width: 10px; height: 10px; border-radius: 3px; display: inline-block; flex-shrink: 0; }}

/* Column chart */
.pl-cols {{ display: flex; align-items: flex-end; gap: 10px; height: 150px; padding-top: 1.2rem; border-bottom: 1px solid {TRACK}; }}
.pl-col {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%; cursor: default; }}
.pl-col-value {{ font-size: 0.7rem; font-weight: 700; color: {INK}; margin-bottom: 4px; }}
.pl-col-bar {{ width: 100%; max-width: 24px; border-radius: 4px 4px 0 0; background: {ACCENT}; min-height: 2px; }}
.pl-col:hover .pl-col-bar {{ filter: brightness(0.92); }}
.pl-col-labels {{ display: flex; gap: 10px; margin-top: 0.4rem; }}
.pl-col-label {{ flex: 1; text-align: center; font-size: 0.72rem; color: {INK_MUTED}; }}
.pl-col-label.today {{ color: {ACCENT_DARK}; font-weight: 700; }}

/* Week strip */
.pl-week {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }}
.pl-day {{
    border: 1px solid {TRACK}; border-radius: 12px; padding: 0.55rem 0.2rem 0.6rem 0.2rem;
    text-align: center; background: {SURFACE}; transition: border-color 0.15s ease;
}}
.pl-day:hover {{ border-color: {ACCENT}; }}
.pl-day.today {{ background: #FFF7FA; border-color: {ACCENT}; }}
.pl-day-name {{ font-size: 0.66rem; font-weight: 700; color: {INK_MUTED}; text-transform: uppercase; letter-spacing: 0.05em; }}
.pl-day-num {{ font-size: 1.05rem; font-weight: 800; color: {INK}; margin: 0.1rem 0 0.3rem 0; }}
.pl-day-dots {{ display: flex; justify-content: center; gap: 3px; min-height: 8px; flex-wrap: wrap; padding: 0 4px; }}
.pl-dot {{ width: 7px; height: 7px; border-radius: 50%; }}

/* Ring */
.pl-ring {{ border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
.pl-ring-inner {{ background: {SURFACE}; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
</style>
"""


def inject_chart_styles():
    st.markdown(_CHART_CSS, unsafe_allow_html=True)


def card(title: str, subtitle: str, body: str) -> str:
    sub = f'<div class="pl-card-sub">{subtitle}</div>' if subtitle else '<div style="height: 0.6rem;"></div>'
    return f'<div class="pl-card"><div class="pl-card-title">{title}</div>{sub}{body}</div>'


def stat_tile(label: str, value, caption: str, icon: str, tint: str = TRACK) -> str:
    return (
        f'<div class="pl-stat">'
        f'<div class="pl-stat-icon" style="background: {tint};">{icon}</div>'
        f'<div><div class="pl-stat-label">{label}</div>'
        f'<div class="pl-stat-value">{value}</div>'
        f'<div class="pl-stat-caption">{caption}</div></div>'
        f'</div>'
    )


def ring(pct: float, size: int = 132, thickness: int = 14, label: str = "complete") -> str:
    pct = max(0.0, min(100.0, float(pct)))
    inner = size - thickness * 2
    value = f"{pct:.0f}%" if pct == int(pct) else f"{pct:.1f}%"
    return (
        f'<div class="pl-ring pl-tip" data-tip="{value} {escape(label)}" '
        f'style="width: {size}px; height: {size}px; background: conic-gradient({ACCENT} {pct * 3.6}deg, {TRACK} 0deg);">'
        f'<div class="pl-ring-inner" style="width: {inner}px; height: {inner}px;">'
        f'<div style="font-size: {size * 0.2:.0f}px; font-weight: 800; color: {INK}; line-height: 1;">{value}</div>'
        f'<div style="font-size: 0.7rem; color: {INK_MUTED}; margin-top: 3px;">{escape(label)}</div>'
        f'</div></div>'
    )


def bar_list(
    rows: Sequence[Tuple[str, float, str, str]],
    max_value: Optional[float] = None,
    color: str = ACCENT,
    colors: Optional[Dict[str, str]] = None,
) -> str:
    """rows: (label, value, value_text, tooltip). Bars scale to max_value (or the largest value)."""
    if not rows:
        return ""
    top = max_value if max_value else max((r[1] for r in rows), default=0) or 1
    out = []
    for label, value, value_text, tip in rows:
        fill = colors.get(label, color) if colors else color
        width = max(0.0, min(100.0, value / top * 100)) if top else 0
        swatch = f'<span class="pl-swatch" style="background: {fill};"></span>' if colors else ""
        out.append(
            f'<div class="pl-bar-row pl-tip" data-tip="{escape(tip)}">'
            f'<div class="pl-bar-head"><span class="pl-bar-label">{swatch}{escape(label)}</span>'
            f'<span class="pl-bar-value">{value_text}</span></div>'
            f'<div class="pl-bar-track"><div class="pl-bar-fill" style="width: {width:.1f}%; background: {fill};"></div></div>'
            f'</div>'
        )
    return "".join(out)


def column_chart(points: List[Tuple[str, float, str, bool]], unit_label=lambda v: str(v)) -> str:
    """points: (x_label, value, tooltip, highlight). One series, single hue."""
    top = max((p[1] for p in points), default=0) or 1
    cols, labels = [], []
    for x_label, value, tip, highlight in points:
        height = value / top * 100 if value else 0
        value_html = f'<div class="pl-col-value">{unit_label(value)}</div>' if value else ""
        cols.append(
            f'<div class="pl-col pl-tip" data-tip="{escape(tip)}">{value_html}'
            f'<div class="pl-col-bar" style="height: {height:.1f}%;"></div></div>'
        )
        labels.append(f'<div class="pl-col-label{" today" if highlight else ""}">{escape(x_label)}</div>')
    return f'<div class="pl-cols">{"".join(cols)}</div><div class="pl-col-labels">{"".join(labels)}</div>'


def week_strip(tasks_by_day: Dict[date, list], start: Optional[date] = None) -> str:
    """Seven day cells; each pending task due that day is a dot coloured by priority."""
    start = start or date.today()
    cells = []
    for offset in range(7):
        day = start + timedelta(days=offset)
        due = tasks_by_day.get(day, [])
        dots = "".join(
            f'<span class="pl-dot" style="background: {PRIORITY_COLORS.get(t.priority, ACCENT)};"></span>'
            for t in due[:6]
        )
        if due:
            names = ", ".join(t.title for t in due[:3]) + ("…" if len(due) > 3 else "")
            tip = f"{len(due)} due: {names}"
        else:
            tip = "Nothing due"
        cells.append(
            f'<div class="pl-day pl-tip{" today" if offset == 0 else ""}" data-tip="{escape(tip)}">'
            f'<div class="pl-day-name">{"Today" if offset == 0 else day.strftime("%a")}</div>'
            f'<div class="pl-day-num">{day.day}</div>'
            f'<div class="pl-day-dots">{dots}</div></div>'
        )
    return f'<div class="pl-week">{"".join(cells)}</div>'


def priority_legend() -> str:
    items = "".join(
        f'<span style="display: inline-flex; align-items: center; gap: 5px; margin-right: 12px;">'
        f'<span class="pl-swatch" style="background: {c};"></span>{p}</span>'
        for p, c in (("High", PRIORITY_COLORS["High"]), ("Medium", PRIORITY_COLORS["Medium"]), ("Low", PRIORITY_COLORS["Low"]))
    )
    return f'<div style="font-size: 0.74rem; color: {INK_MUTED}; margin-top: 0.7rem;">{items}</div>'
