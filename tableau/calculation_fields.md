# Tableau Calculated Fields Specification

This document details the exact calculated fields configured in Tableau Desktop / Tableau Public for the **Global Olympic Sports Performance Analysis (1992 - 2026)** project.

---

### 1. `Avg Medals per Athlete`
- **Formula**:
  ```tableau
  COUNT([Medal_ID]) / COUNTD([Athlete_ID])
  ```
- **Data Type**: Float (Quantitative Measure)
- **Dashboard / Worksheet**: Dashboard 1 (Priya's Scenario) -> `Avg_Medals_Per_Athlete_Sport`
- **Strategic Purpose**: Evaluates the podium productivity per athlete accredited in each sport category. Identifies high-yield sports like **Rowing (6.916)** and **Shooting (6.731)** where a small, elite contingent yields multiple podium opportunities across single, double, and team heats.

---

### 2. `Weighted Medal Score`
- **Formula**:
  ```tableau
  (ZN(SUM(IF [Medal] = "Gold" THEN 3 ELSE 0 END))) + 
  (ZN(SUM(IF [Medal] = "Silver" THEN 2 ELSE 0 END))) + 
  (ZN(SUM(IF [Medal] = "Bronze" THEN 1 ELSE 0 END)))
  ```
- **Data Type**: Integer (Quantitative Measure)
- **Dashboard / Worksheet**: Dashboard 1 & 2 -> `Investment_Vs_Medal_Performance`, `Global_Performance_By_Country`
- **Strategic Purpose**: Solves the traditional medal table dilemma (ranking solely by Gold vs ranking by Total Medals) by applying an Olympic weighted index: 3 points for Gold, 2 for Silver, and 1 for Bronze.

---

### 3. `Medal Efficiency Index (%)`
- **Formula**:
  ```tableau
  (SUM([Medals_Total]) / MAX(1.0, SUM([Sports_Investment_USD_M]))) * 100
  ```
- **Data Type**: Float (Percentage Measure)
- **Dashboard / Worksheet**: Dashboard 2 (Carlos's Scenario) -> `Investment_Vs_Medal_Performance`
- **Strategic Purpose**: Assesses national sports capital ROI. Surfaces agile overperformers such as **Slovakia**, **Georgia**, and **Ethiopia**, whose medal yields per million dollars invested drastically surpass legacy superpowers.

---

### 4. `Cost Per Medal ($M USD)`
- **Formula**:
  ```tableau
  SUM([Sports_Investment_USD_M]) / MAX(1, SUM([Medals_Total]))
  ```
- **Data Type**: Currency / Float
- **Dashboard / Worksheet**: Dashboard 2 -> Metric KPI Card
- **Strategic Purpose**: Calculates the financial investment required to produce a single Olympic medal finish. Enables funding bodies to identify capital-efficient programs for grant allocation.

---

### 5. `Host Advantage Factor (%)`
- **Formula**:
  ```tableau
  (ATTR([Host_Medals]) - ATTR([Non_Host_Avg_Medals])) / ATTR([Non_Host_Avg_Medals]) * 100
  ```
- **Data Type**: Float (Percentage Measure)
- **Dashboard / Worksheet**: Dashboard 3 (William's Scenario) -> `Comparing_Medal_Totals_Hosts`
- **Strategic Purpose**: Quantifies the percentage boost in medal output experienced by host nations during their home Games:
  - **Japan (Tokyo 2020)**: 105 Medals (+1475.0% surge vs away baseline of 6.67)
  - **United States (Atlanta 1996)**: 100 Medals (+41.74% surge vs baseline of 70.55)
  - **China (Beijing 2008)**: 93 Medals (+38.81% surge vs baseline of 67.0)

---

### 6. `Host Nation Flag`
- **Formula**:
  ```tableau
  IF [Country_Name] = [Host_Country] THEN "Host Nation" ELSE "Visiting Nation" END
  ```
- **Data Type**: String (Nominal Dimension)
- **Dashboard / Worksheet**: Dashboard 3 -> Color shelf on Host Analysis charts
- **Strategic Purpose**: Segment event outcomes by home vs away competitor status to isolate psychological, scheduling, and local crowd advantages.

---

### 7. `Medal Efficiency Tier`
- **Formula**:
  ```tableau
  IF [Average_Medal_Efficiency_Pct] >= 48.0 THEN "Top Tier (>=48%)"
  ELSEIF [Average_Medal_Efficiency_Pct] >= 40.0 THEN "Middle Tier (40-48%)"
  ELSE "Emerging Tier (<40%)"
  END
  ```
- **Data Type**: String (Nominal Dimension)
- **Dashboard / Worksheet**: Dashboard 2 -> Regional Efficiency distribution
- **Strategic Purpose**: Segments continental Olympic zones: South America classified as **Top Tier (49.64%)**, Europe/Asia as **Middle Tier (45.98%)**, and others into target development tiers.

---

### 8. `Decade Classification`
- **Formula**:
  ```tableau
  IF [Year] < 2000 THEN "1990s"
  ELSEIF [Year] < 2010 THEN "2000s"
  ELSEIF [Year] < 2020 THEN "2010s"
  ELSE "2020s"
  END
  ```
- **Data Type**: String (Discrete Dimension)
- **Dashboard / Worksheet**: Filter Shelves & Context Filters
- **Strategic Purpose**: Allows longitudinal slicing across modern Olympic eras, especially isolating 2000 (Low: 305 medals), 2020 (Peak: 363 medals), and 2026 (Milano-Cortina: 334 medals).
