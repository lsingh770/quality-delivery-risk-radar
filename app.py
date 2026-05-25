"""
Quality & Delivery Risk Radar
Entry point — orchestrates UI and data flow only.
Business logic → scoring.py
UI components  → components.py
Styling        → styles.css
"""

import os
import streamlit as st
import pandas as pd

from scoring    import load_and_validate, enrich_df, compute_risk_scores, compute_whatif
from components import (
    render_hero_header,
    render_controls,
    render_metric_cards,
    render_portfolio_table_header,
    render_portfolio_row,
    render_deep_dive,
    render_whatif_header,
    render_whatif_result,
    render_empty_state,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Quality & Delivery Risk Radar",
    page_icon="🎯",
    layout="wide",
)

# ─────────────────────────────────────────────
# LOAD STYLES
# ─────────────────────────────────────────────
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ─────────────────────────────────────────────
# HEADER & CONTROLS
# ─────────────────────────────────────────────
render_hero_header()

sample_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
uploaded_file, risk_filter, sort_by = render_controls(sample_path)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
df_raw, error_msg = None, None

if uploaded_file:
    df_raw, error_msg = load_and_validate(uploaded_file)
    if error_msg:
        st.error(f"⚠️ File Error: {error_msg}")
else:
    df_raw = pd.read_csv(sample_path)

# ─────────────────────────────────────────────
# MAIN DASHBOARD
# ─────────────────────────────────────────────
if df_raw is not None and not df_raw.empty:
    df = enrich_df(df_raw)

    # Filter & sort
    df_filtered = df[df["category"].isin(risk_filter)]
    sort_map = {
        "Overall Risk ↓":  ("overall",       False),
        "Overall Risk ↑":  ("overall",       True),
        "Project Name":    ("Project Name",  True),
        "Quality Risk ↓":  ("quality",       False),
        "Schedule Risk ↓": ("schedule",      False),
    }
    col, asc = sort_map.get(sort_by, ("overall", False))
    df_filtered = df_filtered.sort_values(col, ascending=asc)

    # Summary cards
    render_metric_cards(
        n_high   = (df["category"] == "High").sum(),
        n_medium = (df["category"] == "Medium").sum(),
        n_low    = (df["category"] == "Low").sum(),
        avg_risk = df["overall"].mean(),
    )

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊  Portfolio Summary", "🔍  Project Deep Dive", "🔮  What-If Analysis"])

    # ── TAB 1: PORTFOLIO SUMMARY ──
    with tab1:
        render_portfolio_table_header()
        for _, row in df_filtered.iterrows():
            render_portfolio_row(row)

        st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
        st.markdown("**Portfolio Risk Distribution**")
        chart_df = df_filtered[["Project Name", "overall"]].set_index("Project Name")
        st.bar_chart(chart_df, height=220, use_container_width=True)

    # ── TAB 2: PROJECT DEEP DIVE ──
    with tab2:
        project_names = df_filtered["Project Name"].tolist()
        if not project_names:
            st.info("No projects match the current filters.")
        else:
            selected = st.selectbox("Select Project", project_names)
            row = df_filtered[df_filtered["Project Name"] == selected].iloc[0]
            render_deep_dive(row)

    # ── TAB 3: WHAT-IF ANALYSIS ──
    with tab3:
        render_whatif_header()

        wi_project = st.selectbox("Choose Project to Model", df["Project Name"].tolist(), key="wi_select")
        wi_row     = df[df["Project Name"] == wi_project].iloc[0]
        baseline   = compute_risk_scores(wi_row)

        wc1, wc2, wc3 = st.columns(3)
        with wc1:
            extra_qa = st.slider("Add QA Engineers", 0, 5, 0,
                                 help="Each QA engineer adds ~5 velocity points")
        with wc2:
            max_crit     = max(1, int(wi_row["Critical Defects Count"]))
            resolve_crit = st.slider("Resolve Critical Defects", 0, max_crit, 0,
                                     help="How many critical defects can you resolve?")
            if int(wi_row["Critical Defects Count"]) == 0:
                st.caption("No critical defects — nothing to resolve ✅")
        with wc3:
            auto_boost = st.slider("Automation Coverage (%+)", 0, 30, 0,
                                   help="Expected automation coverage improvement")

        projected = compute_whatif(wi_row, extra_qa, resolve_crit, auto_boost)
        render_whatif_result(wi_project, baseline, projected, wi_row["category"])

        if extra_qa == 0 and resolve_crit == 0 and auto_boost == 0:
            st.info("👆 Adjust the sliders above to model different intervention scenarios.")

else:
    render_empty_state()
