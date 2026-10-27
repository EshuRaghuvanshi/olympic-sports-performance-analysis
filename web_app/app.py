"""
Global Olympic Sports Performance Analysis (1992 - 2026)
Flask Web Application with Interactive BI Dashboards, Story Scenes, and Data Explorer
"""

import os
import json
import sqlite3
import pandas as pd
from flask import Flask, render_template, jsonify, request, send_file

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_CSV = os.path.join(DATA_DIR, "processed", "olympic_merged_master.csv")
DB_PATH = os.path.join(DATA_DIR, "olympic_analytics.db")
TWB_PATH = os.path.join(BASE_DIR, "tableau", "Global_Olympic_Sports_Performance_Analysis.twb")

# Helper to get DB connection
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    """Executive Overview & Metric Cards"""
    conn = get_db()
    total_medals = conn.execute("SELECT COUNT(*) FROM medal_results").fetchone()[0]
    total_athletes = conn.execute("SELECT COUNT(*) FROM athletes").fetchone()[0]
    total_countries = conn.execute("SELECT COUNT(DISTINCT Country_Code) FROM medal_results").fetchone()[0]
    total_sports = conn.execute("SELECT COUNT(DISTINCT Sport_Category) FROM medal_results").fetchone()[0]
    conn.close()
    
    kpis = {
        "total_medals": f"{total_medals:,}",
        "total_athletes": f"{total_athletes:,}",
        "total_countries": total_countries,
        "total_sports": total_sports,
        "years_span": "1992 - 2026",
        "top_nation": "United States (735 Medals)",
        "top_efficiency_region": "South America (49.64%)",
        "peak_year": "Tokyo 2020 (363 Medals)"
    }
    return render_template("index.html", kpis=kpis, active_page="overview")

@app.route("/dashboard/priya")
def dashboard_priya():
    """Scenario 1: Ms. Priya - NOC Performance Strategist"""
    return render_template("dashboard_priya.html", active_page="priya")

@app.route("/dashboard/carlos")
def dashboard_carlos():
    """Scenario 2: Mr. Carlos - Sports Investment Analyst"""
    return render_template("dashboard_carlos.html", active_page="carlos")

@app.route("/dashboard/william")
def dashboard_william():
    """Scenario 3: William Robert - Broadcast Journalist & Storyteller"""
    return render_template("dashboard_william.html", active_page="william")

@app.route("/story")
def story():
    """Tableau Story: 6 Sequential Narrative Scenes"""
    return render_template("story.html", active_page="story")

@app.route("/data-explorer")
def data_explorer():
    """Interactive Data Exploration Table with Dynamic Slicers"""
    conn = get_db()
    years = [r[0] for r in conn.execute("SELECT DISTINCT Year FROM medal_results ORDER BY Year").fetchall()]
    regions = [r[0] for r in conn.execute("SELECT DISTINCT Region FROM medal_results ORDER BY Region").fetchall()]
    sports = [r[0] for r in conn.execute("SELECT DISTINCT Sport_Category FROM medal_results ORDER BY Sport_Category").fetchall()]
    conn.close()
    return render_template("data_explorer.html", years=years, regions=regions, sports=sports, active_page="data")

@app.route("/tableau-view")
def tableau_view():
    """Tableau Workbook Specification & Embedded Architecture"""
    return render_template("tableau_view.html", active_page="tableau")

@app.route("/documentation")
def documentation():
    """Full End-to-End Documentation & Development Procedure"""
    return render_template("documentation.html", active_page="docs")

# ================= REST API ENDPOINTS =================

@app.route("/api/kpis")
def api_kpis():
    conn = get_db()
    total_medals = conn.execute("SELECT COUNT(*) FROM medal_results").fetchone()[0]
    total_athletes = conn.execute("SELECT COUNT(*) FROM athletes").fetchone()[0]
    conn.close()
    return jsonify({
        "total_medals": total_medals,
        "total_athletes": total_athletes,
        "top_performer": "United States (735)",
        "runner_up": "China (696)",
        "rowing_yield": 6.916,
        "shooting_yield": 6.731,
        "peak_year_medals": 363,
        "low_year_medals": 305
    })

@app.route("/api/sports-yield")
def api_sports_yield():
    """Sports Category Yield: Avg Medals Per Athlete (Rowing: 6.916, Shooting: 6.731)"""
    conn = get_db()
    rows = conn.execute("""
        SELECT Sport_Category, Total_Medals, Athlete_Count, Avg_Medals_Per_Athlete, Season
        FROM sport_category_metrics
        ORDER BY Avg_Medals_Per_Athlete DESC
    """).fetchall()
    conn.close()
    
    categories = [r["Sport_Category"] for r in rows]
    yields = [r["Avg_Medals_Per_Athlete"] for r in rows]
    total_medals = [r["Total_Medals"] for r in rows]
    athletes = [r["Athlete_Count"] for r in rows]
    
    return jsonify({
        "categories": categories,
        "yields": yields,
        "total_medals": total_medals,
        "athletes": athletes
    })

@app.route("/api/global-performance")
def api_global_performance():
    """Global Performance Metrics by Country: USA 735, CHN 696"""
    conn = get_db()
    rows = conn.execute("""
        SELECT Country_Name, Country_Code, Region,
               COUNT(*) as Total_Medals,
               SUM(CASE WHEN Medal='Gold' THEN 1 ELSE 0 END) as Gold,
               SUM(CASE WHEN Medal='Silver' THEN 1 ELSE 0 END) as Silver,
               SUM(CASE WHEN Medal='Bronze' THEN 1 ELSE 0 END) as Bronze
        FROM medal_results
        GROUP BY Country_Name
        ORDER BY Total_Medals DESC
        LIMIT 20
    """).fetchall()
    conn.close()
    
    countries = [r["Country_Name"] for r in rows]
    gold = [r["Gold"] for r in rows]
    silver = [r["Silver"] for r in rows]
    bronze = [r["Bronze"] for r in rows]
    total = [r["Total_Medals"] for r in rows]
    
    return jsonify({
        "countries": countries,
        "gold": gold,
        "silver": silver,
        "bronze": bronze,
        "total": total
    })

@app.route("/api/investment-bubble")
def api_investment_bubble():
    """Global Sports Investment vs. Medal Performance (Highlighting SVK, GEO, ETH)"""
    conn = get_db()
    rows = conn.execute("""
        SELECT Country_Code, Country_Name, Region,
               SUM(Sports_Investment_USD_M) as Total_Investment,
               SUM(Medals_Total) as Total_Medals,
               AVG(Medal_Efficiency_Pct) as Avg_Efficiency,
               AVG(Cost_Per_Medal_M) as Avg_Cost_Per_Medal
        FROM country_sports_investment
        GROUP BY Country_Code
        ORDER BY Total_Medals DESC
    """).fetchall()
    conn.close()
    
    data = []
    for r in rows:
        is_highlight = r["Country_Code"] in ["SVK", "GEO", "ETH"]
        data.append({
            "country_code": r["Country_Code"],
            "country_name": r["Country_Name"],
            "region": r["Region"],
            "investment": round(r["Total_Investment"], 1),
            "medals": r["Total_Medals"],
            "efficiency": round(r["Avg_Efficiency"], 2),
            "cost_per_medal": round(r["Avg_Cost_Per_Medal"], 2),
            "is_highlight": is_highlight
        })
    return jsonify(data)

@app.route("/api/regional-efficiency")
def api_regional_efficiency():
    """Average Medal Efficiency Percentage by Region (South America: 49.64%, Europe/Asia: 45.98%)"""
    conn = get_db()
    rows = conn.execute("""
        SELECT Region, Average_Medal_Efficiency_Pct, Total_Investment_USD_M, Total_Medals, Athlete_Count
        FROM regional_efficiency
        ORDER BY Average_Medal_Efficiency_Pct DESC
    """).fetchall()
    conn.close()
    
    regions = [r["Region"] for r in rows]
    efficiencies = [r["Average_Medal_Efficiency_Pct"] for r in rows]
    medals = [r["Total_Medals"] for r in rows]
    investment = [r["Total_Investment_USD_M"] for r in rows]
    
    return jsonify({
        "regions": regions,
        "efficiencies": efficiencies,
        "medals": medals,
        "investment": investment
    })

@app.route("/api/yearly-trend")
def api_yearly_trend():
    """Trend of Total Medals Awarded Over the Years (Low: 305 in 2000, Peak: 363 in 2020, 334 in 2026)"""
    conn = get_db()
    rows = conn.execute("""
        SELECT Year, Season, Host_City, Host_Country, COUNT(*) as Total_Medals
        FROM medal_results
        GROUP BY Year
        ORDER BY Year ASC
    """).fetchall()
    conn.close()
    
    years = [r["Year"] for r in rows]
    totals = [r["Total_Medals"] for r in rows]
    editions = [f"{r['Host_City']} {r['Year']} ({r['Season']})" for r in rows]
    
    return jsonify({
        "years": years,
        "totals": totals,
        "editions": editions
    })

@app.route("/api/host-comparison")
def api_host_comparison():
    """Comparing Medal Totals Across Olympic Hosts (Japan: 105, USA: 100, China: 93)"""
    conn = get_db()
    rows = conn.execute("""
        SELECT Host_Country, Host_Year, Host_City, Host_Medals, Non_Host_Avg_Medals, Host_Advantage_Pct
        FROM host_performance
        ORDER BY Host_Medals DESC
    """).fetchall()
    conn.close()
    
    hosts = [f"{r['Host_Country']} ({r['Host_Year']})" for r in rows]
    host_medals = [r["Host_Medals"] for r in rows]
    non_host_avg = [r["Non_Host_Avg_Medals"] for r in rows]
    advantage_pct = [r["Host_Advantage_Pct"] for r in rows]
    
    return jsonify({
        "hosts": hosts,
        "host_medals": host_medals,
        "non_host_avg": non_host_avg,
        "advantage_pct": advantage_pct
    })

@app.route("/api/filter-data", methods=["POST"])
def api_filter_data():
    """Dynamic Filter Endpoint for Data Explorer"""
    req = request.get_json() or {}
    year = req.get("year")
    region = req.get("region")
    sport = req.get("sport")
    medal = req.get("medal")
    limit = int(req.get("limit", 100))
    
    query = "SELECT * FROM olympic_master_view WHERE 1=1"
    params = []
    
    if year and year != "ALL":
        query += " AND Year = ?"
        params.append(int(year))
    if region and region != "ALL":
        query += " AND Region = ?"
        params.append(region)
    if sport and sport != "ALL":
        query += " AND Sport_Category = ?"
        params.append(sport)
    if medal and medal != "ALL":
        query += " AND Medal = ?"
        params.append(medal)
        
    query += f" ORDER BY Year DESC, Medal_ID ASC LIMIT {limit}"
    
    conn = get_db()
    cursor = conn.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    return jsonify({"count": len(rows), "data": rows})

@app.route("/download/twb")
def download_twb():
    """Download the native Tableau Workbook file"""
    return send_file(TWB_PATH, as_attachment=True, download_name="Global_Olympic_Sports_Performance_Analysis.twb")

@app.route("/download/master-csv")
def download_master_csv():
    """Download the cleaned master processed dataset"""
    return send_file(PROCESSED_CSV, as_attachment=True, download_name="olympic_merged_master.csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
