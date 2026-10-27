"""
Test Suite for Olympic Analytics Flask Web Application
Verifies all routes, templates, and API endpoints using Flask test client
"""

import sys
import os
import json

BASE_DIR = r"C:\Users\ESHU RAGHUWANSHI\.gemini\antigravity\scratch\olympic_analytics"
sys.path.insert(0, os.path.join(BASE_DIR, "web_app"))

from app import app

def test_routes():
    print("================ TESTING FLASK APPLICATION ================")
    client = app.test_client()
    
    routes_to_test = [
        ("/", 200, "Global Olympic Sports Performance"),
        ("/dashboard/priya", 200, "Ms. Priya"),
        ("/dashboard/carlos", 200, "Mr. Carlos"),
        ("/dashboard/william", 200, "William Robert"),
        ("/story", 200, "Tableau Interactive Story"),
        ("/data-explorer", 200, "Interactive Olympic Data Explorer"),
        ("/tableau-view", 200, "Tableau BI Integration"),
        ("/documentation", 200, "Project Demonstration"),
        ("/api/kpis", 200, "United States"),
        ("/api/sports-yield", 200, "Rowing"),
        ("/api/global-performance", 200, "China"),
        ("/api/investment-bubble", 200, "Slovakia"),
        ("/api/regional-efficiency", 200, "South America"),
        ("/api/yearly-trend", 200, "2020"),
        ("/api/host-comparison", 200, "Japan")
    ]
    
    passed = 0
    for path, expected_status, content_keyword in routes_to_test:
        response = client.get(path)
        assert response.status_code == expected_status, f"Route {path} returned status {response.status_code}"
        text = response.get_data(as_text=True)
        assert content_keyword in text, f"Route {path} missing keyword '{content_keyword}'"
        print(f"[PASS] {path} -> Status {response.status_code} (Verified keyword: '{content_keyword}')")
        passed += 1
        
    # Test POST /api/filter-data
    post_res = client.post("/api/filter-data", json={"year": 2020, "medal": "Gold"})
    assert post_res.status_code == 200
    data = json.loads(post_res.get_data(as_text=True))
    assert "count" in data and data["count"] > 0
    print(f"[PASS] POST /api/filter-data -> Returned {data['count']} matched rows")
    passed += 1

    print(f"\nAll {passed} Flask tests passed successfully with 100% compliance!")

if __name__ == "__main__":
    test_routes()
