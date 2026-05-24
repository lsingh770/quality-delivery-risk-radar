# Quality & Delivery Risk Radar — MVP

A manager-friendly decision-support tool that converts engineering execution signals into **business risk insights** and **recommended actions** — built for delivery managers, not developers.

---

## Quick Start

### 1. Install dependencies

```bash
pip install streamlit pandas openpyxl
```

### 2. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## How to Use

### Option A — Try with Sample Data
The app loads `sample_data.csv` automatically on startup. Just open it and explore.

### Option B — Upload Your Own Data
Click **Browse files** in the sidebar and upload your CSV or Excel file.

**Required columns** (exact names):

| Column | Description |
|---|---|
| Project Name | Unique project identifier |
| Sprint / Release Name | Sprint or release label |
| Open Defects Count | Total open defects |
| Critical Defects Count | P1/Critical defects |
| High Defects Count | P2/High defects |
| Test Pass Percentage | % of tests passing (0–100) |
| Automation Coverage Percentage | % of test suite automated (0–100) |
| Sprint Velocity Current | Story points delivered this sprint |
| Sprint Velocity Previous | Story points delivered last sprint |
| Release Delay (days) | Days behind original schedule |
| Team Size | Number of engineers on the team |

---

## Risk Scoring Logic

### Why each metric matters (business framing)

| Signal | Business Impact | Weight |
|---|---|---|
| **Critical Defects** | Direct customer-facing failures; escalation risk | 25% |
| **Test Pass Rate** | Release confidence indicator; UAT readiness | 18% |
| **Velocity Drop** | Team strain, blockers, or scope creep signal | 18% |
| **Release Delay** | Missed stakeholder commitments; downstream cascade | 15% |
| **High Defects** | Future critical defect pipeline; technical debt | 12% |
| **Automation Coverage** | Regression safety net; sustainable delivery speed | 12% |

### Risk Categories

| Score | Category | Meaning |
|---|---|---|
| 65–100 | 🔴 High Risk | Immediate management intervention required |
| 35–64 | 🟠 Medium Risk | Active monitoring; proactive action needed |
| 0–34 | 🟢 Low Risk | On track; maintain current practices |

### Breakdown Dimensions

**Quality Risk** — Driven by critical/high defect density and test pass rate. Answers: *"Can we ship something customers won't break?"*

**Schedule Risk** — Driven by release delay and velocity trend. Answers: *"Will we deliver on time?"*

**Execution Risk** — Driven by automation coverage, velocity, and open defect volume. Answers: *"Can the team sustain this pace?"*

---

## Dashboard Features

### 📊 Portfolio Summary
- At-a-glance risk table across all projects
- Color-coded risk scores (Quality / Schedule / Execution)
- Velocity trend indicator
- Bar chart of overall risk distribution

### 🔍 Project Deep Dive
- Full risk breakdown with plain-English explanations
- Top 3 risk drivers with **business impact framing**
- Recommended management actions for each driver
- Key metrics at a glance

### 🔮 What-If Analysis
- Model impact of interventions before committing:
  - Add QA engineers → velocity proxy improvement
  - Resolve critical defects → quality risk reduction
  - Improve automation coverage → execution risk improvement
- Side-by-side baseline vs. projected comparison
- Risk category change detection

---

## Architecture

```
risk_radar/
├── app.py           ← Single-file Streamlit application
├── sample_data.csv  ← Example data with 10 projects
└── README.md        ← This file
```

**Tech stack:**
- Python 3.8+
- Streamlit (UI framework)
- Pandas (data processing)
- Pure rule-based scoring (no ML, fully transparent)

**All scoring logic is in `app.py`** under clearly labeled functions — editable by any Python developer without ML knowledge.

---

## Customizing Risk Weights

Edit the `WEIGHTS` dictionary at the top of `app.py`:

```python
WEIGHTS = {
    "critical_defects":     0.25,   # ← Adjust these
    "high_defects":         0.12,
    "test_pass":            0.18,
    "automation_coverage":  0.12,
    "velocity_drop":        0.18,
    "release_delay":        0.15,
}
```

Weights must sum to 1.0.

---

## Consulting Use

This tool follows the **Data → Insight → Decision** flow:

1. **Data**: Raw engineering metrics (defects, velocity, coverage)
2. **Insight**: Risk scores + plain-English driver explanations
3. **Decision**: Ranked recommended actions with business justification

It can be presented as a consulting deliverable by exporting the portfolio summary view as a screenshot or by building a PDF export on top of the existing data pipeline.

---

*Built as an MVP decision-support tool. Logic is transparent, editable, and consultant-friendly.*
