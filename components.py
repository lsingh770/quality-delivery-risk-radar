"""
components.py
All UI rendering functions — HTML templates and Streamlit component calls.
No business logic lives here. Only presentation.
"""

import streamlit as st


# ─────────────────────────────────────────────
# COLOUR HELPERS
# ─────────────────────────────────────────────

def color_for_score(score):
    if score >= 65: return "#e53e3e"
    if score >= 35: return "#dd6b20"
    return "#276749"


# ─────────────────────────────────────────────
# HTML SNIPPETS
# ─────────────────────────────────────────────

def score_bar_html(score):
    color = color_for_score(score)
    return (
        f"<div class='score-bar-wrap'>"
        f"<span style='font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;color:{color};'>{score}</span>"
        f"<div class='score-bar-track'>"
        f"<div class='score-bar-fill' style='width:{score}%;background:{color};'></div>"
        f"</div></div>"
    )

def risk_badge_html(category, css_class):
    icons = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
    return f'<span class="risk-badge {css_class}">{icons[category]} {category}</span>'


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────

def render_hero_header():
    st.markdown("""
    <div class="hero-header">
        <div class="hero-badge">Decision Intelligence</div>
        <div class="hero-title">Quality &amp; Delivery Risk Radar</div>
        <div class="hero-subtitle">
            Converts engineering execution signals into business risk insights and recommended
            actions — built for delivery managers, not developers.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TOP CONTROLS BAR
# ─────────────────────────────────────────────

def render_controls(sample_csv_path):
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2.5, 2, 2, 1.2])

    with ctrl1:
        uploaded_file = st.file_uploader(
            "Upload CSV / Excel",
            type=["csv", "xlsx", "xls"],
            help="Upload your project metrics file",
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
        with open(sample_csv_path, "rb") as f:
            st.download_button(
                "⬇ Sample CSV",
                data=f,
                file_name="risk_radar_sample.csv",
                mime="text/csv",
            )

    st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:0.5rem 0 1.5rem;'>",
                unsafe_allow_html=True)

    return uploaded_file, risk_filter, sort_by


# ─────────────────────────────────────────────
# SUMMARY METRIC CARDS
# ─────────────────────────────────────────────

def render_metric_cards(n_high, n_medium, n_low, avg_risk):
    avg_class = "red" if avg_risk >= 65 else "orange" if avg_risk >= 35 else "green"
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
            <div class="metric-value {avg_class}">{avg_risk:.0f}</div>
            <div class="metric-sub">Out of 100</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 1 — PORTFOLIO SUMMARY
# ─────────────────────────────────────────────

def render_portfolio_table_header():
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


def render_portfolio_row(row):
    vel_change = row["Sprint Velocity Current"] - row["Sprint Velocity Previous"]
    vel_icon   = "▲" if vel_change >= 0 else "▼"
    vel_color  = "#276749" if vel_change >= 0 else "#e53e3e"

    col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1.6, 1.4, 1.4, 1.4, 1.4])

    with col1:
        st.markdown(f"""
        <div style="padding:0.6rem 0;">
            <div style="font-family:Syne,sans-serif;font-weight:700;font-size:1.2rem;
                        color:#1a1d2e;margin-bottom:0.15rem;">
                {row['Project Name']}
            </div>
            <div style="font-size:0.85rem;color:#9ca3af;">{row['Sprint / Release Name']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(risk_badge_html(row["category"], row["css"]), unsafe_allow_html=True)
        st.markdown(score_bar_html(row["overall"]), unsafe_allow_html=True)

    with col3:
        q_color = color_for_score(row["quality"])
        st.markdown(f"""
        <div style="padding:0.6rem 0;">
            <div style="font-size:0.7rem;color:#9ca3af;text-transform:uppercase;
                        letter-spacing:0.08em;margin-bottom:3px;">Quality</div>
            <div style="font-family:Syne,sans-serif;font-size:1.1rem;
                        font-weight:700;color:{q_color};">{row['quality']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        s_color = color_for_score(row["schedule"])
        st.markdown(f"""
        <div style="padding:0.6rem 0;">
            <div style="font-size:0.7rem;color:#9ca3af;text-transform:uppercase;
                        letter-spacing:0.08em;margin-bottom:3px;">Schedule</div>
            <div style="font-family:Syne,sans-serif;font-size:1.1rem;
                        font-weight:700;color:{s_color};">{row['schedule']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        e_color = color_for_score(row["execution"])
        st.markdown(f"""
        <div style="padding:0.6rem 0;">
            <div style="font-size:0.7rem;color:#9ca3af;text-transform:uppercase;
                        letter-spacing:0.08em;margin-bottom:3px;">Execution</div>
            <div style="font-family:Syne,sans-serif;font-size:1.1rem;
                        font-weight:700;color:{e_color};">{row['execution']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div style="padding:0.6rem 0;">
            <div style="font-size:0.7rem;color:#9ca3af;text-transform:uppercase;
                        letter-spacing:0.08em;margin-bottom:3px;">Velocity</div>
            <div style="font-family:Syne,sans-serif;font-size:1.1rem;
                        font-weight:700;color:{vel_color};">{vel_icon} {abs(int(vel_change))}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #f3f4f6;margin:0;'>",
                unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 2 — PROJECT DEEP DIVE
# ─────────────────────────────────────────────

def render_deep_dive(row):
    cat_color = color_for_score(row["overall"])

    # Header
    col_name, col_score = st.columns([3, 1])
    with col_name:
        st.markdown(f"### {row['Project Name']}")
        st.caption(f"{row['Sprint / Release Name']}  ·  Team of {int(row['Team Size'])}")
    with col_score:
        st.markdown(
            f"<div style='text-align:right'>"
            f"{risk_badge_html(row['category'], row['css'])}"
            f"<div style='font-family:Syne,sans-serif;font-size:2.2rem;font-weight:800;"
            f"color:{cat_color};line-height:1.2;'>{row['overall']}"
            f"<span style='font-size:0.9rem;color:#9ca3af;'>/100</span></div></div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # Risk breakdown
    st.markdown("**Risk Breakdown**")
    rb1, rb2, rb3 = st.columns(3)
    with rb1:
        q_color = color_for_score(row["quality"])
        st.markdown(
            f"<div class='breakdown-item'>"
            f"<div class='breakdown-label'>Quality Risk</div>"
            f"<div class='breakdown-score' style='color:{q_color};'>{row['quality']}</div>"
            f"<div class='breakdown-explain'>Defect density &amp; test confidence</div>"
            f"{score_bar_html(row['quality'])}</div>",
            unsafe_allow_html=True,
        )
    with rb2:
        s_color = color_for_score(row["schedule"])
        st.markdown(
            f"<div class='breakdown-item'>"
            f"<div class='breakdown-label'>Schedule Risk</div>"
            f"<div class='breakdown-score' style='color:{s_color};'>{row['schedule']}</div>"
            f"<div class='breakdown-explain'>Delay exposure &amp; velocity trend</div>"
            f"{score_bar_html(row['schedule'])}</div>",
            unsafe_allow_html=True,
        )
    with rb3:
        e_color = color_for_score(row["execution"])
        st.markdown(
            f"<div class='breakdown-item'>"
            f"<div class='breakdown-label'>Execution Risk</div>"
            f"<div class='breakdown-score' style='color:{e_color};'>{row['execution']}</div>"
            f"<div class='breakdown-explain'>Automation gaps &amp; delivery capacity</div>"
            f"{score_bar_html(row['execution'])}</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # Executive summary
    st.markdown(
        f"<div class='insight-box'>"
        f"<div class='insight-label'>Executive Summary</div>"
        f"<p class='insight-text'>{row['summary']}</p></div>",
        unsafe_allow_html=True,
    )

    # Key metrics
    st.markdown("**Key Metrics**")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    metrics = [
        (m1, "Critical Defects",  int(row["Critical Defects Count"]),           ""),
        (m2, "High Defects",      int(row["High Defects Count"]),                ""),
        (m3, "Test Pass %",       f"{row['Test Pass Percentage']:.0f}%",         ""),
        (m4, "Automation %",      f"{row['Automation Coverage Percentage']:.0f}%", ""),
        (m5, "Velocity",          f"{int(row['Sprint Velocity Current'])} / {int(row['Sprint Velocity Previous'])}", "curr/prev"),
        (m6, "Delay (days)",      int(row["Release Delay (days)"]),              ""),
    ]
    for col, label, val, sub in metrics:
        with col:
            st.metric(label, val, sub if sub else None)

    # Risk drivers
    st.markdown("**Top Risk Drivers & Recommended Actions**")
    for i, d in enumerate(row["drivers"], 1):
        with st.expander(f"Driver {i}: {d['driver']}", expanded=(i == 1)):
            st.error(f"⚠ **Why This Matters**\n\n{d['why']}", icon=None)
            st.info(f"→ **Recommended Action**\n\n{d['action']}", icon=None)


# ─────────────────────────────────────────────
# TAB 3 — WHAT-IF ANALYSIS
# ─────────────────────────────────────────────

def render_whatif_header():
    st.markdown("""
    <div style="font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
                color:#1a1d2e;margin-bottom:0.3rem;">
        What-If Scenario Modeler
    </div>
    <div style="font-size:0.83rem;color:#6b7280;margin-bottom:1.5rem;">
        Simulate the risk impact of management interventions before committing resources.
    </div>
    """, unsafe_allow_html=True)


def render_whatif_result(wi_project, baseline, projected, base_cat):
    from scoring import risk_category

    proj_cat, proj_icon, _ = risk_category(projected["overall"])

    delta_overall  = projected["overall"]  - baseline["overall"]
    delta_quality  = projected["quality"]  - baseline["quality"]
    delta_schedule = projected["schedule"] - baseline["schedule"]
    delta_exec     = projected["execution"]- baseline["execution"]

    def delta_str(d):
        if d < 0: return f"<span style='color:#276749;font-weight:600;'>▼ {abs(d)} improvement</span>"
        if d > 0: return f"<span style='color:#e53e3e;font-weight:600;'>▲ {abs(d)} worse</span>"
        return "<span style='color:#9ca3af;'>No change</span>"

    category_change = ""
    if base_cat != proj_cat:
        category_change = (
            f"<div class='insight-box' style='margin-top:1.2rem;'>"
            f"<div class='insight-label'>Risk Category Change</div>"
            f"<p class='insight-text'>{base_cat} Risk → {proj_cat} Risk &nbsp;{proj_icon}</p>"
            f"</div>"
        )

    st.markdown(f"""
    <div class="detail-card" style="margin-top:1rem;">
        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                    color:#9ca3af;margin-bottom:1rem;font-weight:600;">
            Scenario Impact: {wi_project}
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;">
            <div>
                <div style="font-size:0.72rem;color:#9ca3af;margin-bottom:0.3rem;
                            text-transform:uppercase;letter-spacing:0.08em;">Overall Risk</div>
                <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;
                            color:{color_for_score(projected['overall'])};">{projected['overall']}</div>
                <div style="font-size:0.78rem;color:#9ca3af;">was {baseline['overall']}</div>
                <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_overall)}</div>
            </div>
            <div>
                <div style="font-size:0.72rem;color:#9ca3af;margin-bottom:0.3rem;
                            text-transform:uppercase;letter-spacing:0.08em;">Quality Risk</div>
                <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;
                            color:{color_for_score(projected['quality'])};">{projected['quality']}</div>
                <div style="font-size:0.78rem;color:#9ca3af;">was {baseline['quality']}</div>
                <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_quality)}</div>
            </div>
            <div>
                <div style="font-size:0.72rem;color:#9ca3af;margin-bottom:0.3rem;
                            text-transform:uppercase;letter-spacing:0.08em;">Schedule Risk</div>
                <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;
                            color:{color_for_score(projected['schedule'])};">{projected['schedule']}</div>
                <div style="font-size:0.78rem;color:#9ca3af;">was {baseline['schedule']}</div>
                <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_schedule)}</div>
            </div>
            <div>
                <div style="font-size:0.72rem;color:#9ca3af;margin-bottom:0.3rem;
                            text-transform:uppercase;letter-spacing:0.08em;">Execution Risk</div>
                <div style="font-family:Syne,sans-serif;font-size:1.8rem;font-weight:800;
                            color:{color_for_score(projected['execution'])};">{projected['execution']}</div>
                <div style="font-size:0.78rem;color:#9ca3af;">was {baseline['execution']}</div>
                <div style="font-size:0.78rem;margin-top:4px;">{delta_str(delta_exec)}</div>
            </div>
        </div>
        {category_change}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# EMPTY STATE
# ─────────────────────────────────────────────

def render_empty_state():
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📂</div>
        <div class="upload-title">Upload your project data to get started</div>
        <div class="upload-sub">
            Supports CSV and Excel files · Use the Sample CSV button above to try instantly
        </div>
    </div>
    """, unsafe_allow_html=True)
