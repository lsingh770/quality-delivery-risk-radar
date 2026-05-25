![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

# 🎯 Quality & Delivery Risk Radar  
[Click here to Experience](https://quality-delivery-risk-radar-dgtexkpghkshqqro8ppjcj.streamlit.app/)
### A Decision-Intelligence Tool for Engineering & Delivery Managers

---

## Problem Statement

In most technology organizations, delivery managers and engineering leads are **drowning in data but starving for insight**.

Every sprint, teams generate enormous amounts of execution data — defect counts, test results, velocity metrics, release timelines.  
But this data lives in **disconnected tools**:

- Jira for defects  
- TestRail for test results  
- Confluence for sprint reports  
- Spreadsheets for release tracking  

What’s missing is a **single, synthesized answer** to the most important weekly question a manager needs to ask:

> **“Are we at risk of failing this delivery — and what should I do about it right now?”**

---

## Why This Is a Serious Problem

Failing to answer this question early has well-documented consequences:

- **Late defect discovery is expensive**  
  Defects found in production cost **10–100× more** to fix than those caught during development.

- **Velocity decay goes unnoticed**  
  A drop from 45 to 28 story points over two sprints is a clear warning signal — but often gets buried in daily standups.

- **Managers waste time gathering data**  
  Delivery managers spend **40–60% of their time collecting status** instead of making decisions.

- **Risk escalation is reactive**  
  By the time a project turns “red” in a steering committee, the window for meaningful corrective action has already closed.

---

## Why Existing Tools Don’t Solve This

| Tool | What it does | What it misses |
|-----|-------------|----------------|
| Jira / Azure DevOps | Tracks defects and sprints | No cross-signal risk synthesis |
| TestRail / Zephyr | Tracks test results | Siloed, no delivery context |
| Power BI / Tableau | Visualizes data | Requires manual modeling |
| Excel Dashboards | Flexible | Not real-time, no scoring logic |
| DORA Metrics Tools | Engineering throughput | Not manager-facing, no actions |

**None of these tools answer the manager’s core question.**  
They all require the manager to become a data analyst first.

---

## The Solution

**Quality & Delivery Risk Radar** is a **single-file Python application** that ingests a standard **CSV / Excel export** of project metrics and produces an **executive-grade risk dashboard in under 60 seconds**.

It converts raw engineering signals into **three actionable outputs**:

1. **Risk score (0–100)** with traffic-light categorization for each project  
2. **Risk breakdown** across three business dimensions:
   - Quality  
   - Schedule  
   - Execution  
3. **Plain-English management actions** tied directly to the top risk drivers

This is **not an analytics tool**.  
It is a **decision-support tool**.

---

## Questions the Tool Answers

Every screen is designed to answer one of three critical Monday-morning questions:

- **“Are we at risk?”**  
  → *Portfolio Summary*

- **“Why are we at risk?”**  
  → *Project Deep Dive*

- **“What if I intervene?”**  
  → *What-If Analysis*

---

## What Problem This Tool Solves

### For Engineering Managers
- Eliminates manual synthesis of defects, test results, and velocity
- Produces a consistent, objective project health view every sprint

### For Delivery Managers
- Acts as an **early warning system**, not a post-mortem
- Enables intervention at **Medium Risk**, when fixes are still cheap

### For Program Managers
- Provides a **single portfolio view** across multiple deliveries
- Replaces multiple status reports with one ranked, comparable dashboard

### For Consultants
- Offers a **structured, defensible risk framework**
- Can be presented to clients as a **repeatable methodology**, not opinion

---

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
quality-delivery-risk-radar/
│
├── app.py              ← Entry point — page config, loads styles, orchestrates tabs
├── scoring.py          ← Risk scoring engine — all business logic, zero UI
├── components.py       ← UI layer — all HTML templates and Streamlit rendering
├── styles.css          ← Stylesheet — all visual styling, zero Python
│
├── sample_data.csv     ← 10-project starter dataset
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```
### Design Principles
- **Strict separation of concerns**  
  Business logic, presentation, and orchestration are intentionally decoupled.
- **Testable core logic**  
  `scoring.py` contains no UI dependencies and can be unit-tested independently.
- **UI flexibility**  
  All visual changes are isolated to `components.py` and `styles.css`.
- **Single-responsibility files**  
  Each file does exactly one thing — no hidden coupling.


**Tech stack:**
- Python 3.8+
- Streamlit (UI framework)
- Pandas (data processing)
- Pure rule-based scoring (no ML, fully transparent)

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
