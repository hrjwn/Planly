import streamlit as st

PRIORITY_BADGE_STYLES = {
    "High": "background-color: #FDF2F8; color: #BE185D; border: 1px solid #FBCFE8;",
    "Medium": "background-color: #FFF7ED; color: #C2410C; border: 1px solid #FFEDD5;",
    "Low": "background-color: #F0FDF4; color: #15803D; border: 1px solid #DCFCE7;",
}
_DEFAULT_PRIORITY_STYLE = "background-color: #F3F4F6; color: #4B5563;"


def html(markup: str):
    st.markdown(markup, unsafe_allow_html=True)


def page_header(title: str, subtitle: str):
    html(
        f"""
        <div style="margin-bottom: 1.2rem;">
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #3B3036; margin-bottom: 0.2rem;">
                {title}
            </h1>
            <p style="font-size: 0.95rem; color: #8A737D; margin: 0;">
                {subtitle}
            </p>
        </div>
        """
    )


def section_title(text: str, size: str = "1.05rem", margin: str = "0 0 0.7rem 0"):
    html(
        f"""
        <div style="font-size: {size}; font-weight: 600; color: #3B3036; margin: {margin};">
            {text}
        </div>
        """
    )


def stat_card(label: str, value, caption: str, color: str = "#3B3036", large: bool = False):
    """Metric card. `large` is the left-aligned dashboard style; otherwise centered."""
    if large:
        box = "padding: 1.1rem 1.2rem; box-shadow: 0 2px 8px rgba(217, 108, 157, 0.05); text-align: left;"
        label_extra = " letter-spacing: 0.06em;"
        value_size, caption_size = "2.1rem", "0.8rem"
    else:
        box = "padding: 1.1rem; box-shadow: 0 1px 4px rgba(217, 108, 157, 0.04); text-align: center;"
        label_extra = ""
        value_size, caption_size = "1.8rem", "0.78rem"

    html(
        f"""
        <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 12px; {box}">
            <div style="font-size: 0.75rem; font-weight: 600; color: #8A737D; text-transform: uppercase;{label_extra}">{label}</div>
            <div style="font-size: {value_size}; font-weight: 700; color: {color}; margin: 0.2rem 0;">{value}</div>
            <div style="font-size: {caption_size}; color: #8A737D;">{caption}</div>
        </div>
        """
    )


def empty_state(message: str, padding: str = "1.5rem"):
    html(
        f"""
        <div style="background-color: #FFFFFF; border: 1px dashed #F3B6CF; border-radius: 12px; padding: {padding}; text-align: center; color: #8A737D; font-size: 0.9rem;">
            {message}
        </div>
        """
    )


def priority_badge_style(priority: str) -> str:
    return PRIORITY_BADGE_STYLES.get(priority, _DEFAULT_PRIORITY_STYLE)


def deadline_style(days_left: int) -> str:
    """Background/text colours for a deadline badge `days_left` days away."""
    if days_left < 0:
        return "background-color: #FEE2E2; color: #B91C1C;"
    if days_left <= 1:
        return "background-color: #FEF3C7; color: #B45309;"
    return "background-color: #FCE8F0; color: #C95A8D;"
