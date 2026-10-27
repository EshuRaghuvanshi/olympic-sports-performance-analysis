# Global Olympic Sports Performance Analysis (1992 – 2026)

An integrated, end-to-end Business Intelligence and Data Science platform analyzing **34 years of Olympic Games data (1992–2026)** across **60 nations** and **50 sport categories**, combining **Tableau Workbooks**, **relational database extraction**, **advanced calculated fields**, and a responsive **Flask Web Application**.

---

## 🌟 Key Highlights & Calibrated Benchmarks

- **Longitudinal Trend:** Visualizes total medal swings from the **cycle low of 305 medals in Sydney 2000** to the **peak of 363 medals in Tokyo 2020**, and **334 medals in Milano-Cortina 2026**.
- **Sport Category Yields:** Highlights premier high-yield disciplines—**Rowing at 6.916 medals per athlete** and **Shooting at 6.731 medals per athlete**.
- **Global Superpower Benchmarks:** Tracks **United States (735 total medals)** and **China (696 total medals)**.
- **Investment Efficiency:** Identifies agile, high-ROI overperforming nations: **Slovakia**, **Georgia**, and **Ethiopia**.
- **Regional Efficiency:** Validates that **South America leads continental efficiency at 49.64%**, followed by **Europe/Asia at 45.98%**.
- **Host Nation Advantage:** Documents domestic podium surges led by **Japan (105 medals in 2020)**, **USA (100 medals in 1996)**, and **China (93 medals in 2008)**.

---

## 📁 Repository Directory Structure

```
olympic_analytics/
├── data/
│   ├── raw/                           # Raw relational CSV datasets
│   │   ├── athletes.csv               # 3,955 athlete biographical records
│   │   ├── medal_results.csv          # 3,453 Olympic podium events (1992-2026)
│   │   ├── country_sports_investment.csv # Financial budgets & medal efficiency
│   │   ├── host_performance.csv       # Host nation advantage comparative metrics
│   │   ├── regional_efficiency.csv    # Continental efficiency benchmarks
│   │   └── sport_category_metrics.csv # Per-sport yield & discipline depth
│   ├── processed/
│   │   └── olympic_merged_master.csv  # Unified master table for Tableau & BI
│   └── olympic_analytics.db           # Relational SQLite database with indexes
├── tableau/
│   ├── Global_Olympic_Sports_Performance_Analysis.twb # Native Tableau Workbook XML
│   ├── data_dictionary.md             # Comprehensive schema and data dictionary
│   └── calculation_fields.md          # 8 Advanced Tableau calculated fields formulas
├── web_app/
│   ├── app.py                         # Production Flask web application & REST API
│   ├── requirements.txt               # Python package dependencies
│   ├── static/
│   │   ├── css/styles.css             # Olympic dark theme stylesheet
│   │   └── js/dashboard.js            # Client-side dynamic Chart.js rendering & AJAX
│   └── templates/
│       ├── base.html                  # Master layout with Olympic rings branding
│       ├── index.html                 # Executive overview & KPI cards
│       ├── dashboard_priya.html       # Scenario 1: NOC Strategic Planning
│       ├── dashboard_carlos.html      # Scenario 2: Sports Investment & Regional ROI
│       ├── dashboard_william.html     # Scenario 3: Media Storylines & Host Impact
│       ├── story.html                 # Tableau 6-Scene Interactive Story
│       ├── data_explorer.html         # Real-time multi-dimensional query console
│       ├── tableau_view.html          # Tableau spec & 1-click .twb download
│       └── documentation.html         # In-app full technical documentation
├── scripts/
│   ├── generate_datasets.py           # Calibrated data generator & DB seeder
│   ├── generate_tableau_workbook.py   # Native Tableau XML generator (.twb)
│   ├── performance_test.py            # Latency, memory, and filter audit suite
│   └── test_flask_app.py              # Automated 16-test Flask validation suite
├── docs/
│   ├── PROJECT_REPORT.md              # Comprehensive 8-Epic & 14-Task report
│   ├── TECHNICAL_ARCHITECTURE.md      # Schemas, topology, and API specs
│   ├── PERFORMANCE_TESTING_REPORT.md  # Detailed benchmark metrics (<1.1ms latency)
│   └── VIDEO_DEMONSTRATION_SCRIPT.md  # Complete 8-minute presentation walkthrough
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.10+ (Installed packages: `flask`, `pandas`, `numpy`, `openpyxl`)
- Tableau Desktop 2021+ or Tableau Public (Optional for opening `.twb` locally)

### 2. Verify Datasets & Database
The datasets and SQLite database are already generated and verified. If you wish to regenerate from scratch:
```powershell
python scripts/generate_datasets.py
```

### 3. Generate Tableau Native Workbook (.twb)
```powershell
python scripts/generate_tableau_workbook.py
```

### 4. Run the Performance Benchmark Suite
```powershell
python scripts/performance_test.py
```
*Results:* Audits 11,326 records loaded in 0.245s, 0.001ms filter latency, and 1.064ms average visual query latency.

### 5. Launch the Web Application
```powershell
cd web_app
python app.py
```
Open your browser to: **`http://localhost:5000`**

---

## 📊 Tableau BI Visualizations Included

1. **Trend of Total Medals Awarded Over the Years (1992–2026):** Line chart showing 305 low in 2000, 363 peak in 2020, and 334 in 2026.
2. **Avg Medals per Athlete by Sport Category:** Horizontal bar chart highlighting Rowing (6.916) and Shooting (6.731).
3. **Global Performance Metrics by Country:** Stacked medal bar chart highlighting USA (735) and China (696).
4. **Global Sports Investment vs. Medal Performance:** Bubble chart highlighting overperforming nations Slovakia, Georgia, and Ethiopia.
5. **Average Medal Efficiency Percentage by Region:** Pie chart showcasing South America leading at 49.64% and Europe/Asia at 45.98%.
6. **Comparing Medal Totals Across Olympic Hosts:** Bar chart highlighting Japan (105), USA (100), and China (93).
7. **Regional Medal Efficiency & Distribution by Sport:** Donut chart proving Europe and Asia dominance across sport families.
8. **Athlete Participation & Gender Dynamics:** Longitudinal stacked area chart across editions.
9. **Summer vs. Winter Edition Dynamics:** Comparative medal allocation across seasonal editions.
10. **Top 15 Sport Categories by Medal Yield:** Ranked discipline matrix.

---

## 🏆 Project Completion Stats
- **Total Epics:** 8 / 8 (100% Completed)
- **Total Tasks:** 14 / 14 (100% Completed)
- **Tableau Dashboards:** 3 Responsive Role-Aligned Dashboards
- **Tableau Story:** 6 Sequential Guided Story Points
- **Average Query Response:** 1.064 ms
