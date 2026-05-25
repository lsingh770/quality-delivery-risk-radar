"""
scoring.py
Pure risk scoring logic — no UI, no Streamlit imports.
All business rules and data enrichment live here.
"""

import pandas as pd

# ─────────────────────────────────────────────
# SCORING WEIGHTS
# Adjust these to tune sensitivity per your org
# All weights must sum to 1.0
# ─────────────────────────────────────────────

WEIGHTS = {
    "critical_defects":    0.25,
    "high_defects":        0.12,
    "test_pass":           0.18,
    "automation_coverage": 0.12,
    "velocity_drop":       0.18,
    "release_delay":       0.15,
}

REQUIRED_COLUMNS = [
    "Project Name", "Sprint / Release Name",
    "Open Defects Count", "Critical Defects Count", "High Defects Count",
    "Test Pass Percentage", "Automation Coverage Percentage",
    "Sprint Velocity Current", "Sprint Velocity Previous",
    "Release Delay (days)", "Team Size"
]


# ─────────────────────────────────────────────
# INDIVIDUAL SIGNAL SCORERS (0–100)
# ─────────────────────────────────────────────

def score_critical_defects(val, team_size):
    ratio = val / max(team_size, 1)
    if ratio >= 2.5: return 100
    if ratio >= 1.5: return 85
    if ratio >= 0.8: return 65
    if ratio >= 0.3: return 40
    if ratio >= 0.1: return 20
    return 5

def score_high_defects(val, team_size):
    ratio = val / max(team_size, 1)
    if ratio >= 3:   return 100
    if ratio >= 2:   return 80
    if ratio >= 1:   return 55
    if ratio >= 0.5: return 30
    return 10

def score_test_pass(pct):
    if pct <= 40: return 100
    if pct <= 55: return 80
    if pct <= 70: return 60
    if pct <= 80: return 40
    if pct <= 90: return 20
    return 5

def score_automation(pct):
    if pct <= 20: return 100
    if pct <= 35: return 80
    if pct <= 50: return 60
    if pct <= 65: return 35
    if pct <= 80: return 15
    return 5

def score_velocity_drop(current, previous):
    if previous == 0: return 50
    drop_pct = (previous - current) / previous * 100
    if drop_pct >= 40: return 100
    if drop_pct >= 25: return 80
    if drop_pct >= 15: return 60
    if drop_pct >= 5:  return 30
    if drop_pct >= 0:  return 10
    return 0  # velocity improved

def score_release_delay(days):
    if days == 0:   return 0
    if days <= 3:   return 20
    if days <= 7:   return 45
    if days <= 14:  return 70
    if days <= 21:  return 85
    return 100


# ─────────────────────────────────────────────
# COMPOSITE RISK SCORER
# ─────────────────────────────────────────────

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

    quality  = round(min(s_crit * 0.40 + s_high * 0.25 + s_pass * 0.35, 100))
    schedule = round(min(s_delay * 0.55 + s_vel * 0.45, 100))
    open_proxy = min((row["Open Defects Count"] / max(ts * 5, 1)) * 100, 100)
    execution = round(min(s_auto * 0.35 + s_vel * 0.30 + open_proxy * 0.35, 100))

    return {
        "overall":   overall,
        "quality":   quality,
        "schedule":  schedule,
        "execution": execution,
        "s_crit":    s_crit,
        "s_high":    s_high,
        "s_pass":    s_pass,
        "s_auto":    s_auto,
        "s_vel":     s_vel,
        "s_delay":   s_delay,
    }


# ─────────────────────────────────────────────
# RISK CATEGORY
# ─────────────────────────────────────────────

def risk_category(score):
    if score >= 65: return "High",   "🔴", "high"
    if score >= 35: return "Medium", "🟠", "medium"
    return "Low", "🟢", "low"


# ─────────────────────────────────────────────
# RISK DRIVERS & RECOMMENDED ACTIONS
# ─────────────────────────────────────────────

def get_top_drivers_and_actions(row, scores):
    ts = max(row["Team Size"], 1)
    vel_drop = ((row["Sprint Velocity Previous"] - row["Sprint Velocity Current"])
                / max(row["Sprint Velocity Previous"], 1) * 100)

    candidates = [
        {
            "weight": scores["s_crit"],
            "driver": "Critical Defect Density",
            "why": (
                f"{int(row['Critical Defects Count'])} critical defects on a team of {ts} "
                f"signals immediate stability risk. These are customer-facing issues that "
                f"can erode trust and trigger escalations."
            ),
            "action": (
                "Convene a war-room: assign senior engineers exclusively to critical defect "
                "resolution. Freeze non-critical feature work until the count drops below 3."
            ),
        },
        {
            "weight": scores["s_high"],
            "driver": "Elevated High-Severity Backlog",
            "why": (
                f"{int(row['High Defects Count'])} high-severity defects indicate systemic "
                f"quality gaps. Left unresolved, these migrate to critical and compound release risk."
            ),
            "action": (
                "Triage high defects within 48 hours. Assign ownership and daily status checks. "
                "Consider a focused quality sprint before the next feature sprint."
            ),
        },
        {
            "weight": scores["s_pass"],
            "driver": "Low Test Pass Rate",
            "why": (
                f"A {row['Test Pass Percentage']:.0f}% pass rate means roughly 1 in "
                f"{max(1, int(100 / (100 - row['Test Pass Percentage'] + 0.1)))} test scenarios "
                f"is failing. This undermines release confidence."
            ),
            "action": (
                "Review failing test categories. Identify root cause patterns. "
                "Do not advance to UAT or production until pass rate exceeds 85%."
            ),
        },
        {
            "weight": scores["s_auto"],
            "driver": "Insufficient Automation Coverage",
            "why": (
                f"Only {row['Automation Coverage Percentage']:.0f}% automation coverage means "
                f"the team relies on manual testing, slowing feedback loops and increasing "
                f"regression risk."
            ),
            "action": (
                "Prioritize automation for the top 20% highest-risk regression paths. "
                "A 10% improvement in coverage can reduce regression cycle time by 30-40%."
            ),
        },
        {
            "weight": scores["s_vel"],
            "driver": "Sprint Velocity Decline",
            "why": (
                f"Velocity dropped from {int(row['Sprint Velocity Previous'])} to "
                f"{int(row['Sprint Velocity Current'])} ({vel_drop:.0f}% decline). "
                f"This signals team strain, blockers, or scope creep."
            ),
            "action": (
                "Hold a focused retrospective to identify root cause. "
                "Check for hidden technical debt, unclear requirements, or team bandwidth issues."
            ),
        },
        {
            "weight": scores["s_delay"],
            "driver": "Release Schedule Slippage",
            "why": (
                f"A {int(row['Release Delay (days)'])}-day release delay cascades: stakeholder "
                f"commitments missed, downstream teams blocked, and market timing at risk."
            ),
            "action": (
                "Re-baseline the schedule with the team immediately. Identify the single biggest "
                "blocker and escalate it. Communicate a revised date to stakeholders today."
            ),
        },
    ]

    return sorted(candidates, key=lambda x: x["weight"], reverse=True)[:3]


# ─────────────────────────────────────────────
# EXECUTIVE SUMMARY
# ─────────────────────────────────────────────

def get_executive_summary(row, scores):
    cat, _, _ = risk_category(scores["overall"])
    if cat == "High":
        return (
            f"This delivery is in a critical state. The combination of "
            f"{int(row['Critical Defects Count'])} critical defects, a "
            f"{row['Test Pass Percentage']:.0f}% pass rate, and "
            f"{int(row['Release Delay (days)'])} days of slippage creates compounding risk. "
            f"Immediate management intervention is required."
        )
    elif cat == "Medium":
        return (
            "This delivery shows warning signs that require active monitoring. "
            "Quality and schedule indicators are trending in a concerning direction. "
            "Proactive intervention now can prevent escalation to high risk."
        )
    else:
        return (
            "This delivery is on a healthy trajectory. Key risk indicators are within "
            "acceptable bounds. Continue current practices and maintain vigilance "
            "as scope or complexity increases."
        )


# ─────────────────────────────────────────────
# WHAT-IF ENGINE
# ─────────────────────────────────────────────

def compute_whatif(row, extra_qa, resolved_critical, automation_boost):
    modified = row.copy()
    modified["Critical Defects Count"] = max(0, row["Critical Defects Count"] - resolved_critical)
    modified["Automation Coverage Percentage"] = min(100, row["Automation Coverage Percentage"] + automation_boost)
    modified["Sprint Velocity Current"] = row["Sprint Velocity Current"] + extra_qa * 5
    return compute_risk_scores(modified)


# ─────────────────────────────────────────────
# DATA LOADING & ENRICHMENT
# ─────────────────────────────────────────────

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
        scores  = compute_risk_scores(row)
        cat, icon, css     = risk_category(scores["overall"])
        q_cat, q_icon, q_css = risk_category(scores["quality"])
        s_cat, s_icon, s_css = risk_category(scores["schedule"])
        e_cat, e_icon, e_css = risk_category(scores["execution"])
        drivers = get_top_drivers_and_actions(row, scores)
        summary = get_executive_summary(row, scores)
        results.append({
            **row.to_dict(),
            **scores,
            "category": cat,   "icon": icon,   "css": css,
            "q_cat": q_cat,    "q_icon": q_icon, "q_css": q_css,
            "s_cat": s_cat,    "s_icon": s_icon, "s_css": s_css,
            "e_cat": e_cat,    "e_icon": e_icon, "e_css": e_css,
            "drivers": drivers,
            "summary": summary,
        })
    return pd.DataFrame(results)
