"""
Quality & Delivery Risk Radar — MVP
A manager-friendly decision-support tool that converts
engineering execution signals into business risk insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Quality & Delivery Risk Radar",
    page_icon="🎯",
    layout="wide",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Executive dark theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f5f6fa;
    color: #1a1d2e;
}
.main { background-color: #f5f6fa; }
.block-container { padding: 2rem 2.5rem 3rem; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Headings */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif;
    letter-spacing: -0.02em;
}
            


/* ── HERO HEADER ── */
.hero-header {
    background: linear-gradient(135deg, #ffffff 0%, #eef2ff 50%, #e8f0fe 100%);
    border: 1px solid rgba(99,130,237,0.2);
    border-radius: 16px;
    padding: 2.2rem 2.5rem 1.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(99,130,237,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #1a1d2e;
    margin: 0 0 0.3rem;
    letter-spacing: -0.03em;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #6b7280;
    font-weight: 300;
    margin: 0;
    letter-spacing: 0.01em;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,130,237,0.1);
    color: #4361ee;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    border: 1px solid rgba(99,130,237,0.25);
    margin-bottom: 0.9rem;
}

/* ── METRIC CARDS ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #4361ee);
    opacity: 0.7;
}
.metric-card.red::after   { --accent: #e53e3e; }
.metric-card.orange::after { --accent: #dd6b20; }
.metric-card.green::after  { --accent: #276749; }
.metric-card.blue::after   { --accent: #4361ee; }
.metric-label {
    font-size: 0.73rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9ca3af;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-value.red    { color: #e53e3e; }
.metric-value.orange { color: #dd6b20; }
.metric-value.green  { color: #276749; }
.metric-value.blue   { color: #4361ee; }
.metric-sub {
    font-size: 0.78rem;
    color: #9ca3af;
}

/* ── RISK TABLE ── */
.risk-table-wrap {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.risk-table-header {
    padding: 1.2rem 1.5rem;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #fafafa;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #1a1d2e;
    margin: 0;
    letter-spacing: -0.01em;
}
.section-subtitle {
    font-size: 0.78rem;
    color: #9ca3af;
    margin: 0;
}

/* ── RISK BADGE ── */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    letter-spacing: 0.04em;
}
.risk-badge.high {
    background: rgba(229,62,62,0.08);
    color: #c53030;
    border: 1px solid rgba(229,62,62,0.25);
}
.risk-badge.medium {
    background: rgba(221,107,32,0.08);
    color: #c05621;
    border: 1px solid rgba(221,107,32,0.25);
}
.risk-badge.low {
    background: rgba(39,103,73,0.08);
    color: #276749;
    border: 1px solid rgba(39,103,73,0.25);
}

/* ── SCORE BAR ── */
.score-bar-wrap { width: 100%; }
.score-bar-track {
    height: 6px;
    background: #e5e7eb;
    border-radius: 3px;
    overflow: hidden;
    margin-top: 5px;
}
.score-bar-fill {
    height: 100%;
    border-radius: 3px;
}

/* ── PROJECT DETAIL CARD ── */
.detail-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.detail-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
}
.project-name-big {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #1a1d2e;
    margin: 0 0 0.25rem;
}
.sprint-tag {
    font-size: 0.75rem;
    color: #9ca3af;
    font-weight: 400;
}

/* ── RISK BREAKDOWN ── */
.risk-breakdown {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.2rem;
}
.breakdown-item {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.9rem 1rem;
}
.breakdown-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9ca3af;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.breakdown-score {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.breakdown-explain {
    font-size: 0.73rem;
    color: #6b7280;
    line-height: 1.4;
}

/* ── DRIVERS & ACTIONS ── */
.driver-block, .action-block {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.7rem;
}
.driver-block { border-left: 3px solid #e53e3e; }
.action-block { border-left: 3px solid #4361ee; }
.driver-title, .action-title {
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
}
.driver-title { color: #c53030; }
.action-title { color: #4361ee; }
.driver-text, .action-text {
    font-size: 0.82rem;
    color: #4b5563;
    line-height: 1.5;
    margin: 0;
}

/* ── INSIGHT BOX ── */
.insight-box {
    background: rgba(67,97,238,0.05);
    border: 1px solid rgba(67,97,238,0.18);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
}
.insight-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4361ee;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.insight-text {
    font-size: 0.85rem;
    color: #374151;
    line-height: 1.55;
    margin: 0;
    font-style: italic;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.2rem;
}
            
/* ── SIDEBAR TOGGLE BUTTON (collapsed state) ── */
[data-testid="collapsedControl"] {
    background: #4361ee !important;
    border-radius: 50% !important;
    box-shadow: 0 2px 8px rgba(67,97,238,0.4) !important;
}

[data-testid="collapsedControl"] svg {
    fill: #ffffff !important;
    stroke: #ffffff !important;
}

/* Also target the expand button on the sidebar itself */
[data-testid="baseButton-headerNoPadding"] {
    color: #4361ee !important;
}

button[kind="header"] {
    color: #4361ee !important;
}

/* Nuclear option — force any chevron/arrow inside sidebar controls to be visible */
section[data-testid="stSidebar"] button svg,
div[data-testid="collapsedControl"] svg,
button[data-testid="collapsedControl"] svg {
    fill: #ffffff !important;
    color: #ffffff !important;
    stroke: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* ── UPLOAD ZONE ── */
.upload-zone {
    background: #ffffff;
    border: 2px dashed #d1d5db;
    border-radius: 14px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.upload-zone:hover { border-color: #4361ee; }
.upload-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1d2e;
    margin-bottom: 0.4rem;
}
.upload-sub { font-size: 0.82rem; color: #9ca3af; }

/* ── DIVIDER ── */
.section-divider {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 2rem 0;
}

/* ── WHAT-IF ── */
.whatif-box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

/* Streamlit overrides */
.stButton > button {
    background: linear-gradient(135deg, #eef2ff, #e0e7ff);
    color: #4361ee;
    border: 1px solid rgba(67,97,238,0.3);
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.5rem 1.2rem;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
    border-color: rgba(67,97,238,0.5);
    transform: translateY(-1px);
}
.stSelectbox > div > div {
    background: #ffffff;
    border-color: #d1d5db;
    color: #1a1d2e;
    border-radius: 8px;
}
div[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem !important;
}
.stDataFrame {
    background: #ffffff !important;
    border-radius: 10px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #f3f4f6;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #e5e7eb;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #9ca3af;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    border-radius: 7px;
    padding: 0.4rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #1a1d2e !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* Table row divider */
hr { border-color: #f3f4f6 !important; }

/* ── HIDE SIDEBAR ENTIRELY ── */
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"]  { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RISK SCORING ENGINE
# ─────────────────────────────────────────────

WEIGHTS = {
    "critical_defects":     0.25,
    "high_defects":         0.12,
    "test_pass":            0.18,
    "automation_coverage":  0.12,
    "velocity_drop":        0.18,
    "release_delay":        0.15,
}

def score_critical_defects(val, team_size):
    ratio = val / max(team_size, 1)
    if ratio >= 2.5:   return 100
    if ratio >= 1.5:   return 85
    if ratio >= 0.8:   return 65
    if ratio >= 0.3:   return 40
    if ratio >= 0.1:   return 20
    return 5

def score_high_defects(val, team_size):
    ratio = val / max(team_size, 1)
    if ratio >= 3:    return 100
    if ratio >= 2:    return 80
    if ratio >= 1:    return 55
    if ratio >= 0.5:  return 30
    return 10

def score_test_pass(pct):
    if pct <= 40:  return 100
    if pct <= 55:  return 80
    if pct <= 70:  return 60
    if pct <= 80:  return 40
    if pct <= 90:  return 20
    return 5

def score_automation(pct):
    if pct <= 20:  return 100
    if pct <= 35:  return 80
    if pct <= 50:  return 60
    if pct <= 65:  return 35
    if pct <= 80:  return 15
    return 5

def score_velocity_drop(current, previous):
    if previous == 0: return 50
    drop_pct = (previous - current) / previous * 100
    if drop_pct >= 40:  return 100
    if drop_pct >= 25:  return 80
    if drop_pct >= 15:  return 60
    if drop_pct >= 5:   return 30
    if drop_pct >= 0:   return 10
    return 0  # velocity improved

def score_release_delay(days):
    if days == 0:   return 0
    if days <= 3:   return 20
    if days <= 7:   return 45
    if days <= 14:  return 70
    if days <= 21:  return 85
    return 100

def compute_risk_scores(row):
    ts = max(row["Team Size"], 1)

    s_crit  = score_critical_defects(row["Critical Defects Count"], ts)
    s_high  = score_high_defects(row["High Defects Count"], ts)
    s_pass  = score_test_pass(row["Test Pass Percentage"])
    s_auto  = score_automation(row["Automation Coverage Percentage"])
    s_vel   = score_velocity_drop(row["Sprint Velocity Current"], row["Sprint Velocity Previous"])
    s_delay = score_release_delay(row["Release Delay (days)"])

    overall = (
        s_crit  * WEIGHTS["critical_defects"] +
        s_high  * WEIGHTS["high_defects"] +
        s_pass  * WEIGHTS["test_pass"] +
        s_auto  * WEIGHTS["automation_coverage"] +
        s_vel   * WEIGHTS["velocity_drop"] +
        s_delay * WEIGHTS["release_delay"]
    )
    overall = round(min(overall, 100))

    # Quality risk: defects + pass rate
    quality = round(min(s_crit*0.40 + s_high*0.25 + s_pass*0.35, 100))
    # Schedule risk: delay + velocity
    schedule = round(min(s_delay*0.55 + s_vel*0.45, 100))
    # Execution risk: automation + velocity + open defects proxy
    open_proxy = min((row["Open Defects Count"] / max(ts*5, 1)) * 100, 100)
    execution = round(min(s_auto*0.35 + s_vel*0.30 + open_proxy*0.35, 100))

    return {
        "overall": overall,
        "quality": quality,
        "schedule": schedule,
        "execution": execution,
        "s_crit": s_crit,
        "s_high": s_high,
        "s_pass": s_pass,
        "s_auto": s_auto,
        "s_vel": s_vel,
        "s_delay": s_delay,
    }

def risk_category(score):
    if score >= 65: return "High", "🔴", "high"
    if score >= 35: return "Medium", "🟠", "medium"
    return "Low", "🟢", "low"

def get_top_drivers_and_actions(row, scores):
    ts = max(row["Team Size"], 1)
    vel_drop = ((row["Sprint Velocity Previous"] - row["Sprint Velocity Current"])
                / max(row["Sprint Velocity Previous"], 1) * 100)

    candidates = [
        {
            "weight": scores["s_crit"],
            "driver": "Critical Defect Density",
            "why": f"{int(row['Critical Defects Count'])} critical defects on a team of {ts} signals immediate stability risk. "
                   f"These are customer-facing issues that can erode trust and trigger escalations.",
            "action": "Convene a war-room: assign senior engineers exclusively to critical defect resolution. "
                      "Freeze non-critical feature work until the count drops below 3."
        },
        {
            "weight": scores["s_high"],
            "driver": "Elevated High-Severity Backlog",
            "why": f"{int(row['High Defects Count'])} high-severity defects indicate systemic quality gaps. "
                   f"Left unresolved, these migrate to critical and compound release risk.",
            "action": "Triage high defects within 48 hours. Assign ownership and daily status checks. "
                      "Consider a focused 'quality sprint' before the next feature sprint."
        },
        {
            "weight": scores["s_pass"],
            "driver": "Low Test Pass Rate",
            "why": f"A {row['Test Pass Percentage']:.0f}% pass rate means roughly 1 in "
                   f"{max(1,int(100/(100-row['Test Pass Percentage']+0.1)))} test scenarios is failing. "
                   f"This undermines release confidence.",
            "action": "Review failing test categories. Identify root cause patterns. "
                      "Do not advance to UAT or production until pass rate exceeds 85%."
        },
        {
            "weight": scores["s_auto"],
            "driver": "Insufficient Automation Coverage",
            "why": f"Only {row['Automation Coverage Percentage']:.0f}% automation coverage means the team "
                   f"relies on manual testing, slowing feedback loops and increasing regression risk.",
            "action": "Prioritize automation for the top 20% highest-risk regression paths. "
                      "A 10% improvement in coverage can reduce regression cycle time by 30-40%."
        },
        {
            "weight": scores["s_vel"],
            "driver": "Sprint Velocity Decline",
            "why": f"Velocity dropped from {int(row['Sprint Velocity Previous'])} to "
                   f"{int(row['Sprint Velocity Current'])} ({vel_drop:.0f}% decline). "
                   f"This signals team strain, blockers, or scope creep.",
            "action": "Hold a focused retrospective to identify root cause. "
                      "Check for hidden technical debt, unclear requirements, or team bandwidth issues."
        },
        {
            "weight": scores["s_delay"],
            "driver": "Release Schedule Slippage",
            "why": f"A {int(row['Release Delay (days)'])}-day release delay cascades: stakeholder commitments "
                   f"missed, downstream teams blocked, and market timing at risk.",
            "action": "Re-baseline the schedule with the team immediately. Identify the single biggest blocker "
                      "and escalate it. Communicate a revised date to stakeholders today."
        },
    ]

    # sort by weight descending, return top 3
    top3 = sorted(candidates, key=lambda x: x["weight"], reverse=True)[:3]
    return top3

def get_executive_summary(row, scores):
    cat, _, _ = risk_category(scores["overall"])
    if cat == "High":
        return (f"This delivery is in a critical state. The combination of "
                f"{int(row['Critical Defects Count'])} critical defects, a "
                f"{row['Test Pass Percentage']:.0f}% pass rate, and "
                f"{int(row['Release Delay (days)'])} days of slippage creates compounding risk. "
                f"Immediate management intervention is required.")
    elif cat == "Medium":
        return (f"This delivery shows warning signs that require active monitoring. "
                f"Quality and schedule indicators are trending in a concerning direction. "
                f"Proactive intervention now can prevent escalation to high risk.")
    else:
        return (f"This delivery is on a healthy trajectory. Key risk indicators are within "
                f"acceptable bounds. Continue current practices and maintain vigilance "
                f"as scope or complexity increases.")


# ─────────────────────────────────────────────
# WHAT-IF ENGINE
# ─────────────────────────────────────────────

def compute_whatif(row, extra_qa, resolved_critical, automation_boost):
    modified = row.copy()
    modified["Critical Defects Count"] = max(0, row["Critical Defects Count"] - resolved_critical)
    modified["Automation Coverage Percentage"] = min(100, row["Automation Coverage Percentage"] + automation_boost)
    # Extra QA → velocity improvement proxy (each QA adds ~5 velocity points)
    modified["Sprint Velocity Current"] = row["Sprint Velocity Current"] + extra_qa * 5
    return compute_risk_scores(modified)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def color_for_score(score):
    if score >= 65: return "#fc8181"
    if score >= 35: return "#f6ad55"
    return "#68d391"

def score_bar_html(score, label=""):
    color = color_for_score(score)
    return f"""
    <div class="score-bar-wrap">
        <span style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:{color};">{score}</span>
        <div class="score-bar-track">
            <div class="score-bar-fill" style="width:{score}%;background:{color};"></div>
        </div>
    </div>
    """

def risk_badge_html(category, css_class):
    icons = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
    return f'<span class="risk-badge {css_class}">{icons[category]} {category}</span>'


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

REQUIRED_COLUMNS = [
    "Project Name", "Sprint / Release Name",
    "Open Defects Count", "Critical Defects Count", "High Defects Count",
    "Test Pass Percentage", "Automation Coverage Percentage",
    "Sprint Velocity Current", "Sprint Velocity Previous",
    "Release Delay (days)", "Team Size"
]

def load_and_validate(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            return None, f"Missing columns: {', '.join(missing)}"
        df = df[REQUIRED_COLUMNS].dropna()
        return df, None
    except Exception as e:
        return None, str(e)

def enrich_df(df):
    results = []
    for _, row in df.iterrows():
        scores = compute_risk_scores(row)
        cat, icon, css = risk_category(scores["overall"])
        q_cat, q_icon, q_css = risk_category(scores["quality"])
        s_cat, s_icon, s_css = risk_category(scores["schedule"])
        e_cat, e_icon, e_css = risk_category(scores["execution"])
        drivers = get_top_drivers_and_actions(row, scores)
        summary = get_executive_summary(row, scores)
        results.append({
            **row.to_dict(),
            **scores,
            "category": cat, "icon": icon, "css": css,
            "q_cat": q_cat, "q_icon": q_icon, "q_css": q_css,
            "s_cat": s_cat, "s_icon": s_icon, "s_css": s_css,
            "e_cat": e_cat, "e_icon": e_icon, "e_css": e_css,
            "drivers": drivers,
            "summary": summary,
        })
    return pd.DataFrame(results)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero-header">
    <div class="hero-badge">Decision Intelligence</div>
    <div class="hero-title">Quality & Delivery Risk Radar</div>
    <div class="hero-subtitle">
        Converts engineering execution signals into business risk insights and recommended actions —
        built for delivery managers, not developers.
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TOP CONTROLS (replaces sidebar)
# ─────────────────────────────────────────────

ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2.5, 2, 2, 1.2])

with ctrl1:
    uploaded_file = st.file_uploader(
        "Upload CSV / Excel",
        type=["csv", "xlsx", "xls"],
        help="Upload your project metrics file",
        label_visibility="visible",
    )

with ctrl2:
    risk_filter = st.multiselect(
        "Filter by Risk Level",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
    )

with ctrl3:
    sort_by = st.selectbox(
        "Sort Projects By",
        options=["Overall Risk ↓", "Overall Risk ↑", "Project Name", "Quality Risk ↓", "Schedule Risk ↓"],
    )

with ctrl4:
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
    with open(sample_path, "rb") as f:
        st.download_button(
            "⬇ Sample CSV",
            data=f,
            file_name="risk_radar_sample.csv",
            mime="text/csv",
        )

st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:0.5rem 0 1.5rem;'>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────

# Load data
df_raw = None
error_msg = None

if uploaded_file:
    df_raw, error_msg = load_and_validate(uploaded_file)
    if error_msg:
        st.error(f"⚠️ File Error: {error_msg}")
else:
    # Use sample data by default
    sample_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
    df_raw = pd.read_csv(sample_path)

if df_raw is not None and not df_raw.empty:
    df = enrich_df(df_raw)

    # Apply filters
    df_filtered = df[df["category"].isin(risk_filter)]

    # Sort
    if sort_by == "Overall Risk ↓":
        df_filtered = df_filtered.sort_values("overall", ascending=False)
    elif sort_by == "Overall Risk ↑":
        df_filtered = df_filtered.sort_values("overall", ascending=True)
    elif sort_by == "Project Name":
        df_filtered = df_filtered.sort_values("Project Name")
    elif sort_by == "Quality Risk ↓":
        df_filtered = df_filtered.sort_values("quality", ascending=False)
    elif sort_by == "Schedule Risk ↓":
        df_filtered = df_filtered.sort_values("schedule", ascending=False)

    # ── SUMMARY METRICS ──
    n_high   = (df["category"] == "High").sum()
    n_medium = (df["category"] == "Medium").sum()
    n_low    = (df["category"] == "Low").sum()
    avg_risk = df["overall"].mean()

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card red">
            <div class="metric-label">High Risk Projects</div>
            <div class="metric-value red">{n_high}</div>
            <div class="metric-sub">Require immediate action</div>
        </div>
        <div class="metric-card orange">
            <div class="metric-label">Medium Risk Projects</div>
            <div class="metric-value orange">{n_medium}</div>
            <div class="metric-sub">Need active monitoring</div>
        </div>
        <div class="metric-card green">
            <div class="metric-label">Low Risk Projects</div>
            <div class="metric-value green">{n_low}</div>
            <div class="metric-sub">On track</div>
        </div>
        <div class="metric-card blue">
            <div class="metric-label">Portfolio Avg Risk</div>
            <div class="metric-value {'red' if avg_risk>=65 else 'orange' if avg_risk>=35 else 'green'}">{avg_risk:.0f}</div>
            <div class="metric-sub">Out of 100</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3 = st.tabs(["📊  Portfolio Summary", "🔍  Project Deep Dive", "🔮  What-If Analysis"])

    # ════════════════════════════════════
    # TAB 1: PORTFOLIO SUMMARY
    # ════════════════════════════════════
    with tab1:
        st.markdown("""
        <div class="risk-table-wrap">
          <div class="risk-table-header">
            <div>
              <p class="section-title">Project Risk Summary</p>
              <p class="section-subtitle">Ranked by overall delivery risk score</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Build display table
        for _, row in df_filtered.iterrows():
            vel_change = row["Sprint Velocity Current"] - row["Sprint Velocity Previous"]
            vel_icon = "▲" if vel_change >= 0 else "▼"
            vel_color = "#68d391" if vel_change >= 0 else "#fc8181"

            col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1.6, 1.4, 1.4, 1.4, 1.4])

            with col1:
                st.markdown(f"""
                <div style="padding:0.6rem 0;">
                    <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.2rem;color:#000000;margin-bottom:0.15rem;">
                        {row['Project Name']}
                    </div>
                    <div style="font-size:0.95rem;color:#5a6278;">{row['Sprint / Release Name']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(risk_badge_html(row['category'], row['css']), unsafe_allow_html=True)
                st.markdown(score_bar_html(row['overall']), unsafe_allow_html=True)

            with col3:
                q_color = color_for_score(row['quality'])
                st.markdown(f"""
                <div style="padding:0.6rem 0;">
                    <div style="font-size:0.7rem;color:#5a6278;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Quality</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:{q_color};">{row['quality']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                s_color = color_for_score(row['schedule'])
                st.markdown(f"""
                <div style="padding:0.6rem 0;">
                    <div style="font-size:0.7rem;color:#5a6278;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Schedule</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:{s_color};">{row['schedule']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col5:
                e_color = color_for_score(row['execution'])
                st.markdown(f"""
                <div style="padding:0.6rem 0;">
                    <div style="font-size:0.7rem;color:#5a6278;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Execution</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:{e_color};">{row['execution']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col6:
                st.markdown(f"""
                <div style="padding:0.6rem 0;">
                    <div style="font-size:0.7rem;color:#5a6278;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">Velocity</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:{vel_color};">{vel_icon} {abs(int(vel_change))}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<hr style='border:none;border-top:1px solid #1e2333;margin:0;'>", unsafe_allow_html=True)

        # Portfolio health chart using native streamlit
        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="risk-table-header" style="margin-bottom:1rem;">
            <div>
              <p class="section-title">Portfolio Risk Distribution</p>
              <p class="section-subtitle">Overall risk scores across all projects</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        chart_df = df_filtered[["Project Name", "overall", "quality", "schedule", "execution"]].set_index("Project Name")
        st.bar_chart(chart_df[["overall"]], height=200, use_container_width=True)


    # ════════════════════════════════════
    # TAB 2: PROJECT DEEP DIVE
    # ════════════════════════════════════
    with tab2:
        project_names = df_filtered["Project Name"].tolist()
        if not project_names:
            st.info("No projects match the current filters.")
        else:
            selected = st.selectbox("Select Project", project_names)
            row = df_filtered[df_filtered["Project Name"] == selected].iloc[0]
            scores = {k: row[k] for k in ["overall","quality","schedule","execution",
                                           "s_crit","s_high","s_pass","s_auto","s_vel","s_delay"]}

            # Header
            cat_color = color_for_score(row["overall"])
            # Header row
            col_name, col_score = st.columns([3, 1])
            with col_name:
                st.markdown(f"### {row['Project Name']}")
                st.caption(f"{row['Sprint / Release Name']}  ·  Team of {int(row['Team Size'])}")
            with col_score:
                cat_color = color_for_score(row["overall"])
                st.markdown(
                    f"<div style='text-align:right'>{risk_badge_html(row['category'], row['css'])}"
                    f"<div style='font-family:Syne,sans-serif;font-size:2.2rem;font-weight:800;"
                    f"color:{cat_color};line-height:1.2;'>{row['overall']}"
                    f"<span style='font-size:0.9rem;color:#9ca3af;'>/100</span></div></div>",
                    unsafe_allow_html=True
                )

            st.divider()

            # Risk breakdown
            st.markdown("**Risk Breakdown**")
            rb1, rb2, rb3 = st.columns(3)
            with rb1:
                q_color = color_for_score(row['quality'])
                st.markdown(
                    f"<div class='breakdown-item'><div class='breakdown-label'>Quality Risk</div>"
                    f"<div class='breakdown-score' style='color:{q_color};'>{row['quality']}</div>"
                    f"<div class='breakdown-explain'>Defect density & test confidence</div>"
                    f"{score_bar_html(row['quality'])}</div>",
                    unsafe_allow_html=True
                )
            with rb2:
                s_color = color_for_score(row['schedule'])
                st.markdown(
                    f"<div class='breakdown-item'><div class='breakdown-label'>Schedule Risk</div>"
                    f"<div class='breakdown-score' style='color:{s_color};'>{row['schedule']}</div>"
                    f"<div class='breakdown-explain'>Delay exposure & velocity trend</div>"
                    f"{score_bar_html(row['schedule'])}</div>",
                    unsafe_allow_html=True
                )
            with rb3:
                e_color = color_for_score(row['execution'])
                st.markdown(
                    f"<div class='breakdown-item'><div class='breakdown-label'>Execution Risk</div>"
                    f"<div class='breakdown-score' style='color:{e_color};'>{row['execution']}</div>"
                    f"<div class='breakdown-explain'>Automation gaps & delivery capacity</div>"
                    f"{score_bar_html(row['execution'])}</div>",
                    unsafe_allow_html=True
                )

            st.divider()

            # Executive summary
            st.markdown(
                f"<div class='insight-box'><div class='insight-label'>Executive Summary</div>"
                f"<p class='insight-text'>{row['summary']}</p></div>",
                unsafe_allow_html=True
            )

            # Key Metrics
            st.markdown("""
            <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#c5cad9;
                        margin:1.5rem 0 0.8rem;letter-spacing:-0.01em;">
                Key Metrics
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3, m4, m5, m6 = st.columns(6)
            metrics = [
                (m1, "Critical Defects", int(row["Critical Defects Count"]), ""),
                (m2, "High Defects", int(row["High Defects Count"]), ""),
                (m3, "Test Pass %", f"{row['Test Pass Percentage']:.0f}%", ""),
                (m4, "Automation %", f"{row['Automation Coverage Percentage']:.0f}%", ""),
                (m5, "Velocity", f"{int(row['Sprint Velocity Current'])} / {int(row['Sprint Velocity Previous'])}", "curr/prev"),
                (m6, "Delay (days)", int(row["Release Delay (days)"]), ""),
            ]
            for col, label, val, sub in metrics:
                with col:
                    st.metric(label, val, sub if sub else None)

            # Drivers & Actions
            st.markdown("""
            <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#c5cad9;
                        margin:1.5rem 0 0.8rem;letter-spacing:-0.01em;">
                Top Risk Drivers & Recommended Actions
            </div>
            """, unsafe_allow_html=True)

            #for i, d in enumerate(row["drivers"], 1):
            #    with st.expander(f"Driver {i}: {d['driver']}", expanded=(i==1)):
            #        st.markdown(f"""
            #        <div class="driver-block">
            #            <div class="driver-title">⚠ Why This Matters</div>
            #            <p class="driver-text">{d['why']}</p>
            #        </div>
            #        <div class="action-block" style="margin-top:0.6rem;">
            #            <div class="action-title">→ Recommended Action</div>
            #            <p class="action-text">{d['action']}</p>
            #        </div>
            #        """, unsafe_allow_html=True)
            
            for i, d in enumerate(row["drivers"], 1):
                with st.expander(f"Driver {i}: {d['driver']}", expanded=(i==1)):
                    st.error(f"⚠ **Why This Matters**\n\n{d['why']}", icon=None)
                    st.info(f"→ **Recommended Action**\n\n{d['action']}", icon=None)


    # ════════════════════════════════════
    # TAB 3: WHAT-IF ANALYSIS
    # ════════════════════════════════════
    with tab3:
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#c5cad9;
                    margin-bottom:0.5rem;">
            What-If Scenario Modeler
        </div>
        <div style="font-size:0.83rem;color:#5a6278;margin-bottom:1.5rem;">
            Simulate the risk impact of management interventions before committing resources.
        </div>
        """, unsafe_allow_html=True)

        wi_project = st.selectbox("Choose Project to Model", df["Project Name"].tolist(), key="wi_select")
        wi_row = df[df["Project Name"] == wi_project].iloc[0]
        baseline = compute_risk_scores(wi_row)

        st.markdown("<div class='whatif-box'>", unsafe_allow_html=True)
        wc1, wc2, wc3 = st.columns(3)
        with wc1:
            extra_qa = st.slider("Add QA Engineers", 0, 5, 0,
                                 help="Each QA engineer adds ~5 velocity points")
        with wc2:
            max_crit = max(1, int(wi_row["Critical Defects Count"]))
            resolve_crit = st.slider("Resolve Critical Defects", 0, max_crit, 0,
                                    help="How many critical defects can you resolve?")
            if int(wi_row["Critical Defects Count"]) == 0:
                st.caption("No critical defects — nothing to resolve ✅")
        with wc3:
            auto_boost = st.slider("Automation Coverage (%+)", 0, 30, 0,
                                   help="Expected automation coverage improvement")
        st.markdown("</div>", unsafe_allow_html=True)

        projected = compute_whatif(wi_row, extra_qa, resolve_crit, auto_boost)

        # Show comparison
        delta_overall  = projected["overall"]  - baseline["overall"]
        delta_quality  = projected["quality"]  - baseline["quality"]
        delta_schedule = projected["schedule"] - baseline["schedule"]
        delta_exec     = projected["execution"]- baseline["execution"]

        def delta_str(d):
            if d < 0: return f"<span style='color:#68d391;font-weight:600;'>▼ {abs(d)} improvement</span>"
            if d > 0: return f"<span style='color:#fc8181;font-weight:600;'>▲ {abs(d)} worse</span>"
            return "<span style='color:#5a6278;'>No change</span>"

        proj_cat, proj_icon, proj_css = risk_category(projected["overall"])
        base_cat = wi_row["category"]

        st.markdown(f"""
        <div class="detail-card" style="margin-top:1rem;">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#5a6278;margin-bottom:1rem;font-weight:600;">
                Scenario Impact: {wi_project}
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;">
                <div>
                    <div style="font-size:0.72rem;color:#5a6278;margin-bottom:0.3rem;text-transform:uppercase;letter-spacing:0.08em;">Overall Risk</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:{color_for_score(projected['overall'])};">{projected['overall']}</div>
                    <div style="font-size:0.78rem;color:#5a6278;">was {baseline['overall']}</div>
                    <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_overall)}</div>
                </div>
                <div>
                    <div style="font-size:0.72rem;color:#5a6278;margin-bottom:0.3rem;text-transform:uppercase;letter-spacing:0.08em;">Quality Risk</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:{color_for_score(projected['quality'])};">{projected['quality']}</div>
                    <div style="font-size:0.78rem;color:#5a6278;">was {baseline['quality']}</div>
                    <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_quality)}</div>
                </div>
                <div>
                    <div style="font-size:0.72rem;color:#5a6278;margin-bottom:0.3rem;text-transform:uppercase;letter-spacing:0.08em;">Schedule Risk</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:{color_for_score(projected['schedule'])};">{projected['schedule']}</div>
                    <div style="font-size:0.78rem;color:#5a6278;">was {baseline['schedule']}</div>
                    <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_schedule)}</div>
                </div>
                <div>
                    <div style="font-size:0.72rem;color:#5a6278;margin-bottom:0.3rem;text-transform:uppercase;letter-spacing:0.08em;">Execution Risk</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:{color_for_score(projected['execution'])};">{projected['execution']}</div>
                    <div style="font-size:0.78rem;color:#5a6278;">was {baseline['execution']}</div>
                    <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_exec)}</div>
                </div>
            </div>
            {"<div class='insight-box' style='margin-top:1.2rem;'><div class='insight-label'>Risk Category Change</div><p class='insight-text'>" + base_cat + " Risk → " + proj_cat + " Risk &nbsp;" + proj_icon + "</p></div>" if base_cat != proj_cat else ""}
        </div>
        """, unsafe_allow_html=True)

        if extra_qa == 0 and resolve_crit == 0 and auto_boost == 0:
            st.info("👆 Adjust the sliders above to model different intervention scenarios.")

else:
    # ── EMPTY STATE ──
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📂</div>
        <div class="upload-title">Upload your project data to get started</div>
        <div class="upload-sub">Supports CSV and Excel files · Download the sample CSV from the sidebar to see the expected format</div>
    </div>
    """, unsafe_allow_html=True)
