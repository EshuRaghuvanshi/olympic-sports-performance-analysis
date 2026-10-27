# Olympic Analytics: Comprehensive Data Dictionary

## 1. Overview
The Global Olympic Sports Performance Analysis platform integrates historical Olympic Games data spanning 1992 through 2026 across both Summer and Winter editions. The schema models athletes, event outcomes, sports investments, regional efficiency metrics, and host nation advantages.

---

## 2. Table Schemas

### Table 1: `athletes`
Stores biographical, physical, and demographic attributes of Olympic athletes across all 50 analyzed sports.

| Column Name | Data Type | Constraint | Description | Example Values |
|---|---|---|---|---|
| `Athlete_ID` | INTEGER | PRIMARY KEY | Unique identifier for each Olympic competitor | `10001`, `10425` |
| `Athlete_Name` | VARCHAR(100) | NOT NULL | Full name of the athlete | `Michael Smith`, `Ling Wang` |
| `Gender` | VARCHAR(10) | NOT NULL | Athlete gender category (`Male` / `Female`) | `Male`, `Female` |
| `Age` | INTEGER | CHECK (Age >= 14) | Age of athlete at time of competition | `24`, `28` |
| `Height_cm` | INTEGER | NULLABLE | Athlete height in centimeters | `185`, `172` |
| `Weight_kg` | INTEGER | NULLABLE | Athlete weight in kilograms | `78`, `64` |
| `Country_Code` | VARCHAR(3) | FOREIGN KEY | 3-letter IOC Country Code | `USA`, `CHN`, `GBR` |
| `Country_Name` | VARCHAR(100) | NOT NULL | Full country designation | `United States`, `China` |
| `Region` | VARCHAR(50) | NOT NULL | Continental Olympic grouping | `North America`, `Europe/Asia`, `South America` |
| `Sport_Category` | VARCHAR(80) | NOT NULL | Primary sport classification | `Rowing`, `Shooting`, `Aquatics - Swimming` |
| `Primary_Discipline` | VARCHAR(100) | NOT NULL | Specific event discipline | `Single Sculls`, `10m Air Rifle` |
| `Season` | VARCHAR(10) | NOT NULL | Olympic Games season (`Summer` / `Winter`) | `Summer`, `Winter` |

---

### Table 2: `medal_results`
Stores event-level medal results across all Olympic editions from 1992 to 2026.

| Column Name | Data Type | Constraint | Description | Example Values |
|---|---|---|---|---|
| `Medal_ID` | INTEGER | PRIMARY KEY | Unique transaction record for each awarded medal | `50001`, `51240` |
| `Year` | INTEGER | NOT NULL | Olympic Games calendar year | `1992`, `2000`, `2020`, `2026` |
| `Season` | VARCHAR(10) | NOT NULL | Seasonal designation | `Summer`, `Winter` |
| `Host_City` | VARCHAR(100) | NOT NULL | Host metropolitan city | `Barcelona`, `Tokyo`, `Milano-Cortina` |
| `Host_Country` | VARCHAR(100) | NOT NULL | Sovereign nation hosting the Games | `Spain`, `Japan`, `Italy` |
| `Country_Code` | VARCHAR(3) | FOREIGN KEY | IOC Country code of podium finisher | `USA`, `JPN`, `CHN` |
| `Country_Name` | VARCHAR(100) | NOT NULL | Sovereign nation of podium finisher | `United States`, `Japan` |
| `Region` | VARCHAR(50) | NOT NULL | Continental grouping | `Europe/Asia`, `South America` |
| `Sport_Category` | VARCHAR(80) | NOT NULL | Major sport category | `Rowing`, `Shooting`, `Alpine Skiing` |
| `Discipline` | VARCHAR(100) | NOT NULL | Specific competitive discipline | `Single Sculls`, `100m Sprint` |
| `Event_Gender` | VARCHAR(10) | NOT NULL | Competitive division gender | `Male`, `Female` |
| `Medal` | VARCHAR(10) | NOT NULL | Podium finish tier (`Gold`, `Silver`, `Bronze`) | `Gold`, `Silver`, `Bronze` |
| `Athlete_ID` | INTEGER | FOREIGN KEY | Reference to participating athlete | `10012` |
| `Athlete_Name` | VARCHAR(100) | NOT NULL | Name of podium finisher | `Emma Novak` |

---

### Table 3: `country_sports_investment`
Longitudinal record of national sports agency budgets, high-performance allocations, and medal counts.

| Column Name | Data Type | Constraint | Description | Example Values |
|---|---|---|---|---|
| `Country_Code` | VARCHAR(3) | FOREIGN KEY | IOC Country code | `USA`, `SVK`, `ETH` |
| `Country_Name` | VARCHAR(100) | NOT NULL | Country name | `Slovakia`, `Ethiopia` |
| `Region` | VARCHAR(50) | NOT NULL | Geographic region | `Europe/Asia`, `Africa` |
| `Year` | INTEGER | NOT NULL | Olympic cycle year | `1992`, `2020`, `2026` |
| `Sports_Investment_USD_M` | FLOAT | NOT NULL | Total national sports investment ($ Millions USD) | `485.0`, `14.5` |
| `High_Performance_Budget_USD_M` | FLOAT | NOT NULL | Targeted elite athlete development budget ($M) | `315.25`, `9.42` |
| `Medals_Total` | INTEGER | NOT NULL | Total medals won by nation in edition | `75`, `4` |
| `Gold_Medals` | INTEGER | NOT NULL | Total Gold medals won | `26`, `2` |
| `Silver_Medals` | INTEGER | NOT NULL | Total Silver medals won | `25`, `1` |
| `Bronze_Medals` | INTEGER | NOT NULL | Total Bronze medals won | `24`, `1` |
| `Medal_Efficiency_Pct` | FLOAT | NOT NULL | Medals per unit investment efficiency percentage | `49.64`, `145.2` |
| `Cost_Per_Medal_M` | FLOAT | NOT NULL | Estimated cost per medal won ($M USD) | `6.47`, `3.62` |

---

### Table 4: `regional_efficiency`
Aggregated efficiency benchmarks across the 5 global Olympic continental zones.

| Column Name | Data Type | Constraint | Description | Benchmark Value |
|---|---|---|---|---|
| `Region` | VARCHAR(50) | PRIMARY KEY | Continental federation grouping | `South America`, `Europe/Asia` |
| `Average_Medal_Efficiency_Pct` | FLOAT | NOT NULL | Average medal efficiency percentage | **South America: 49.64%**, **Europe/Asia: 45.98%** |
| `Total_Investment_USD_M` | FLOAT | NOT NULL | Cumulative sports investment ($M USD) | `1720.0`, `28400.0` |
| `Total_Medals` | INTEGER | NOT NULL | Cumulative medals awarded | `112`, `2210` |
| `Athlete_Count` | INTEGER | NOT NULL | Total registered athlete pool | `420`, `2450` |
| `Medals_Per_Athlete` | FLOAT | NOT NULL | Podiums per registered athlete | `0.267`, `0.902` |

---

### Table 5: `host_performance`
Analysis of host nation medal surges comparing host year output against baseline averages.

| Column Name | Data Type | Description | Key Target Values |
|---|---|---|---|
| `Host_Country` | VARCHAR(100) | Name of hosting nation | `Japan`, `United States`, `China` |
| `Country_Code` | VARCHAR(3) | IOC Country Code | `JPN`, `USA`, `CHN` |
| `Host_Year` | INTEGER | Year country hosted the Olympic Games | `2020` (Tokyo), `1996` (Atlanta), `2008` (Beijing) |
| `Host_City` | VARCHAR(100) | Metropolitan host site | `Tokyo`, `Atlanta`, `Beijing` |
| `Host_Medals` | INTEGER | **Medals won while hosting** | **Japan: 105**, **USA: 100**, **China: 93** |
| `Non_Host_Avg_Medals` | FLOAT | Average medals won in away Games | `6.67` (JPN), `70.55` (USA), `67.0` (CHN) |
| `Host_Advantage_Pct` | FLOAT | Percentage surge above away baseline | `+1475.0%`, `+41.74%`, `+38.81%` |
| `Global_Rank_When_Hosting` | INTEGER | Rank on medal table during home Games | `1` (JPN 2020), `1` (USA 1996), `1` (CHN 2008) |

---

### Table 6: `sport_category_metrics`
Per-sport efficiency metrics demonstrating athlete-to-medal yield.

| Column Name | Data Type | Description | Key Target Values |
|---|---|---|---|
| `Sport_Category` | VARCHAR(80) | Categorical discipline family | **Rowing**, **Shooting**, etc. |
| `Season` | VARCHAR(10) | Seasonality (`Summer` / `Winter`) | `Summer` |
| `Total_Medals` | INTEGER | Cumulative medals won in sport | `166` (Rowing), `175` (Shooting) |
| `Athlete_Count` | INTEGER | Total competitors fielded | `24` (Rowing), `26` (Shooting) |
| `Avg_Medals_Per_Athlete` | FLOAT | **Podium yield per accredited athlete** | **Rowing: 6.916**, **Shooting: 6.731** |
| `Gold_Medals` | INTEGER | Gold podium count | `58`, `61` |
| `Silver_Medals` | INTEGER | Silver podium count | `55`, `58` |
| `Bronze_Medals` | INTEGER | Bronze podium count | `53`, `56` |
| `Disciplines_Count` | INTEGER | Unique medal event disciplines | `4` (Rowing), `5` (Shooting) |
