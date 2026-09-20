# 🍬 Nassau Candy Distributor — End-to-End Business Analytics

An end-to-end **Data Analytics & Decision Support project** focused on product-line profitability, margin quality, cost structure, concentration risk, geographic dependency, and margin volatility for Nassau Candy Distributor.

The project combines **Python-based data cleaning and exploratory analysis**, phase-wise analytical reports, a **research paper**, and a deployed **Streamlit dashboard** for interactive business decision support.

## 🌐 Live Project

- **Live Streamlit Dashboard:** https://candy-analysis-dashboard.streamlit.app/
- **GitHub Repository:** https://github.com/Prasanta-ai/nassau-candy-end-to-end-analytics
- **Google Colab Analysis:** https://colab.research.google.com/drive/13ik-v3fcDlTMK70DIWwkud-jEM-ETgHc?usp=sharing

---

## 📌 Project Overview

Sales alone do not indicate whether a product is financially healthy. A product can generate strong revenue while consuming most of that revenue through cost, while a high-margin product may contribute very little absolute profit because of low sales volume.

This project evaluates:

- Revenue
- Cost
- Gross Profit
- Gross Margin
- Profit per Unit
- Revenue Contribution
- Profit Contribution
- Cost Ratio
- Product and Division Performance
- Pareto / Concentration Risk
- Geographic Dependency
- Cost & Margin Risk
- Margin Volatility

The final analytical outputs are operationalized through an interactive Streamlit dashboard.

---

## 🎯 Business Objectives

1. Identify the most profitable products and divisions.
2. Compare sales scale with actual profit contribution.
3. Measure revenue and profit concentration across the portfolio.
4. Identify state/region dependency.
5. Detect cost-heavy and margin-poor products.
6. Flag products for repricing, cost renegotiation, or discontinuation review.
7. Measure margin stability.
8. Deliver the findings through an interactive dashboard.

---

## 📊 Dataset Summary

| Metric | Value |
|---|---:|
| Transaction Rows | 10,194 |
| Unique Orders | 8,549 |
| Unique Customers | 5,044 |
| Products | 15 |
| Divisions | 3 |
| Regions | 4 |
| States / Provinces | 59 |
| Analysis Period | 2024-01-02 to 2025-12-31 |
| Total Sales | $141,783.63 |
| Total Cost | $48,340.83 |
| Total Gross Profit | $93,442.80 |
| Overall Gross Margin | 65.91% |

---

## 🧰 Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Google Colab
- VS Code
- Git & GitHub

---

## 🔄 Project Workflow

```text
Raw Dataset
    ↓
Phase 1 — Data Understanding
    ↓
Phase 2 — Data Cleaning & Validation
    ↓
Phase 3.1 — Profitability Metric Calculation
    ↓
Phase 3.2 — Product-Level Profitability Analysis
    ↓
Phase 3.3 — Division-Level Performance Analysis
    ↓
Phase 3.4 — Product Pareto Analysis
    ↓
Phase 3.4 — State / Region Concentration & Dependency
    ↓
Phase 3.5 — Cost Structure Diagnostics
    ↓
Margin Volatility Analysis
    ↓
Research Paper
    ↓
Streamlit Decision-Support Dashboard
    ↓
GitHub Version Control & Deployment
```

---

## 📐 Core KPIs

```text
Gross Margin (%) = Gross Profit / Sales × 100
Profit per Unit = Gross Profit / Units
Revenue Contribution (%) = Product Sales / Total Sales × 100
Profit Contribution (%) = Product Gross Profit / Total Gross Profit × 100
Cost Ratio (%) = Cost / Sales × 100
Margin Volatility = Standard Deviation of periodic Gross Margin
```

---

## 🔎 Major Analytical Findings

### Overall Profitability

- **Total Sales:** $141,783.63
- **Total Cost:** $48,340.83
- **Total Gross Profit:** $93,442.80
- **Overall Gross Margin:** 65.91%

### Chocolate Division

Chocolate generated approximately:

- **92.88% of total revenue**
- **95.06% of total gross profit**
- **67.45% gross margin**

### Product Concentration

Only **5 of 15 products (33.33%)** are required to cross the 80% contribution threshold.

Together, those five products generate approximately:

- **92.88% of total revenue**
- **95.06% of total gross profit**

All five are Chocolate products.

### Geographic Concentration

Only **16 of 59 states/provinces (27.12%)** account for approximately:

- **80.03% of revenue**
- **80.14% of gross profit**

California is the largest individual geographic market.

### Cost Structure Diagnostics

Portfolio-relative thresholds:

| Threshold | Value |
|---|---:|
| Q1 Gross Margin | 48.33% |
| Q3 Cost Ratio | 51.67% |
| Q1 Sales | $69.00 |
| Median Sales | $597.50 |
| Q1 Gross Profit | $40.36 |

Four products are simultaneously cost-heavy and margin-poor:

- Kazookles
- Fun Dip
- SweeTARTS
- Nerds

### Kazookles

- **Cost Ratio:** 92.31%
- **Gross Margin:** 7.69%
- **Profit per Unit:** $0.25
- **Recommended Action:** Repricing + Cost Renegotiation

### Discontinuation Review Candidates

- Fun Dip
- SweeTARTS
- Nerds

### Margin Stability

The supplied volatility summary indicates:

- **Average margin:** approximately 65.91%
- **Margin volatility SD:** approximately 0.31 percentage points

The supplied volatility report is based on **12 month-of-year buckets across the two-year period**, so it should be interpreted as seasonal month-of-year variation rather than a 24-point chronological time series.

---

## 🖥️ Streamlit Dashboard

### Executive Overview
- Revenue
- Gross Profit
- Gross Margin
- Total Cost
- Units
- Unique Orders
- Top products by gross profit

### Product Profitability
- Product margin leaderboard
- Profit contribution
- Margin-risk threshold
- Product search
- Product-level financial table

### Division Performance
- Revenue vs Gross Profit
- Margin distribution
- Revenue contribution
- Profit contribution
- Revenue-profit gap

### Profit Concentration
- Revenue Pareto
- Profit Pareto
- 80% contribution threshold
- State / province concentration
- Regional dependency

### Cost & Margin Diagnostics
- Quantile-based risk thresholds
- Cost vs Sales scatter
- Cost Ratio vs Gross Margin
- Repricing flags
- Cost renegotiation flags
- Discontinuation review flags

### Margin Volatility
- Average monthly margin
- Standard deviation
- Minimum / maximum margin
- Company margin trend
- Division volatility trend

### Reports & Downloads
- Phase-wise analytical reports
- Downloadable CSV reports
- Downloadable filtered dataset

---

## 🎛️ Dashboard Controls

- Date Range
- Division Filter
- Product Search
- Margin Threshold Slider
- Dashboard Module Selector

The interactive margin threshold is used for exploratory visualization and does **not** replace the approved quantile-based cost-diagnostic rules.

---

## 📁 Repository Structure

```text
nassau-candy-end-to-end-analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── Nassau_Candy_Distributor.csv
│   └── processed/
│       └── Cleaned_Nassau_Candy_Distributor_Dataset.csv
│
├── notebooks/
│   └── Nassau_Candy_Complete_EDA_Analysis.ipynb
│
├── reports/
│   ├── phase_1/
│   │   └── phase_1_data_understanding_report.csv
│   ├── phase_2/
│   │   └── Phase_2_Data_Quality_Report.csv
│   ├── profitability/
│   │   └── Phase_3.1_Profitability_Matric_Calculation_Report.csv
│   │   └── Phase_3.2_Product_Level_Profitability_Analysis.csv
│   │   └── Phase_3.3_Division_Level_Performance_Analysis.csv
│   ├── pareto/
│   │   └── Phase_3.4_Preto_Analysis_Summary_Report.csv
│   │   └── Profit_Pareto_Report.csv
│   │   └── Revenue_Pareto_Report.csv
│   ├── geographic/
│   │   └── Phase_3.4_State Concentration & Over-Dependency Analysis_Summary.csv
│   │   └── Region_Concentration_Analysis.csv
│   │   └── State_Concentration_Analysis.csv
│   ├── cost_diagnostics/
│   │   └── Cost_Diagnostics_Summary.csv
│   │   └── Cost_Structure_Diagnostics.csv
│   └── margin_volatility/
│       └── Division_Margin_Volatility_Report.csv
│       └── Margin_Volatility_Analysis_Summary.csv
│       └── Monthly_Company_Margin.csv
│       └── Product_Margin_Volatility_Report.csv
│
├── charts/
│
└── research_paper/
    └── Nassau_Candy_Research_Paper.pdf
```

---

## 🚀 Run the Dashboard Locally

```bash
git clone https://github.com/Prasanta-ai/nassau-candy-end-to-end-analytics.git
cd nassau-candy-end-to-end-analytics
pip install -r requirements.txt
streamlit run app.py
```

---

## 📓 Analysis Notebook

The complete Python cleaning and analysis workflow is available in the `notebooks/` directory and in the Google Colab link above.

It covers:

- Data understanding
- Data cleaning
- Data-quality validation
- Profitability calculations
- Product analysis
- Division analysis
- Pareto analysis
- Geographic dependency
- Cost structure diagnostics
- Margin volatility
- Analytical report generation

---

## 📄 Research Paper

**A Data-Driven Framework for Product-Line Profitability, Margin Risk, and Portfolio Decision Support: A Case Study of Nassau Candy Distributor**

Repository location:

```text
research_paper/Nassau_Candy_Research_Paper.pdf
```

---

## ⚠️ Data & Methodology Notes

- `Order Date` is used for time-based analysis.
- Archived `Ship Date` / `Shipping Days` fields contain implausible durations and are not used for profitability or operational conclusions.
- Cost-diagnostic thresholds are **portfolio-relative quantiles**, not external industry standards.
- Geographic high-load indicators reflect order/unit concentration and should not be interpreted as proof of physical logistics congestion.
- Gross profit represents product-level contribution and does not include every possible operating expense.

---

## 💼 Business Recommendations

- Protect the five core Chocolate products because they drive the majority of company profit.
- Review pricing and supplier cost for **Kazookles**.
- Conduct portfolio viability reviews for **Fun Dip, SweeTARTS, and Nerds**.
- Develop additional profitable products outside the dominant Chocolate portfolio.
- Reduce geographic dependency through profitable expansion while protecting service quality in major markets.
- Use the Streamlit dashboard as a recurring management-review tool.

---

## 👤 Author

**Prasanta Das**  
Department of Information Technology  
St. Thomas' College of Engineering and Technology, Kolkata  
Data Analyst Intern — Unified Mentor

---

## ⭐ Project Highlights

**Data Cleaning → EDA → Financial KPI Analysis → Product & Division Profitability → Pareto Analysis → Geographic Dependency → Cost Diagnostics → Margin Volatility → Business Recommendations → Research Paper → Interactive Streamlit Dashboard → GitHub Deployment**

If you find the project useful, consider giving the repository a ⭐.
