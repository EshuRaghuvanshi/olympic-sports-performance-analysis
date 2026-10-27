"""
Calibrated Dataset Generator for Global Olympic Sports Performance Analysis (1992 - 2026)
Guarantees exact scenario constraints:
- Yearly Medal Trend: Low of 305 in 2000, Peak of 363 in 2020, 334 in 2026, all other years strictly between 305 and 363.
- Global Performance Metrics: USA = 735 total medals, China = 696 total medals.
- Avg Medals per Athlete: Rowing = 6.916, Shooting = 6.731.
- Olympic Hosts Medal Totals: Japan = 105, USA = 100, China = 93.
- Regional Efficiency: South America = 49.64%, Europe/Asia = 45.98%.
- Overperformers in Sports Investment vs Medal Performance: Slovakia, Georgia, Ethiopia.
"""

import os
import random
import sqlite3
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

BASE_DIR = r"C:\Users\ESHU RAGHUWANSHI\.gemini\antigravity\scratch\olympic_analytics"
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "data", "olympic_analytics.db")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# 1. 10 Editions from 1992 to 2026 with exact yearly medal constraints
# Low of 305 in 2000, Peak of 363 in 2020, 334 in 2026; all others between 305 and 363
EDITIONS = [
    {"year": 1992, "season": "Summer", "city": "Barcelona", "country": "Spain", "country_code": "ESP", "total_medals": 315},
    {"year": 1996, "season": "Summer", "city": "Atlanta", "country": "United States", "country_code": "USA", "total_medals": 320},
    {"year": 2000, "season": "Summer", "city": "Sydney", "country": "Australia", "country_code": "AUS", "total_medals": 305}, # Benchmark Low: 305
    {"year": 2004, "season": "Summer", "city": "Athens", "country": "Greece", "country_code": "GRE", "total_medals": 328},
    {"year": 2008, "season": "Summer", "city": "Beijing", "country": "China", "country_code": "CHN", "total_medals": 345},
    {"year": 2012, "season": "Summer", "city": "London", "country": "Great Britain", "country_code": "GBR", "total_medals": 338},
    {"year": 2016, "season": "Summer", "city": "Rio de Janeiro", "country": "Brazil", "country_code": "BRA", "total_medals": 350},
    {"year": 2020, "season": "Summer", "city": "Tokyo", "country": "Japan", "country_code": "JPN", "total_medals": 363}, # Benchmark Peak: 363
    {"year": 2024, "season": "Summer", "city": "Paris", "country": "France", "country_code": "FRA", "total_medals": 355},
    {"year": 2026, "season": "Winter", "city": "Milano-Cortina", "country": "Italy", "country_code": "ITA", "total_medals": 334}, # Benchmark: 334
]

YEARS = [e["year"] for e in EDITIONS]
TOTAL_MEDALS_ACROSS_GAMES = sum(e["total_medals"] for e in EDITIONS) # 3453 medals

# 2. 60 Countries
COUNTRIES_DATA = [
    # Top Giants
    {"code": "USA", "name": "United States", "region": "North America", "investment": 4850, "target_medals": 735},
    {"code": "CHN", "name": "China", "region": "Europe/Asia", "investment": 4400, "target_medals": 696},
    {"code": "GBR", "name": "Great Britain", "region": "Europe/Asia", "investment": 2600, "target_medals": 185},
    {"code": "GER", "name": "Germany", "region": "Europe/Asia", "investment": 2900, "target_medals": 195},
    {"code": "RUS", "name": "Russia", "region": "Europe/Asia", "investment": 3200, "target_medals": 210},
    {"code": "AUS", "name": "Australia", "region": "Oceania", "investment": 2100, "target_medals": 140},
    {"code": "JPN", "name": "Japan", "region": "Europe/Asia", "investment": 2800, "target_medals": 165},
    {"code": "FRA", "name": "France", "region": "Europe/Asia", "investment": 2500, "target_medals": 135},
    {"code": "ITA", "name": "Italy", "region": "Europe/Asia", "investment": 2300, "target_medals": 120},
    {"code": "KOR", "name": "South Korea", "region": "Europe/Asia", "investment": 1900, "target_medals": 110},
    {"code": "NED", "name": "Netherlands", "region": "Europe/Asia", "investment": 1400, "target_medals": 95},
    {"code": "CAN", "name": "Canada", "region": "North America", "investment": 1800, "target_medals": 105},
    {"code": "CUB", "name": "Cuba", "region": "North America", "investment": 450, "target_medals": 75},
    {"code": "HUN", "name": "Hungary", "region": "Europe/Asia", "investment": 850, "target_medals": 70},
    # South America (High efficiency leader: 49.64%)
    {"code": "BRA", "name": "Brazil", "region": "South America", "investment": 420, "target_medals": 48},
    {"code": "ARG", "name": "Argentina", "region": "South America", "investment": 180, "target_medals": 22},
    {"code": "COL", "name": "Colombia", "region": "South America", "investment": 120, "target_medals": 18},
    {"code": "CHI", "name": "Chile", "region": "South America", "investment": 80, "target_medals": 9},
    {"code": "ECU", "name": "Ecuador", "region": "South America", "investment": 55, "target_medals": 8},
    {"code": "VEN", "name": "Venezuela", "region": "South America", "investment": 65, "target_medals": 9},
    {"code": "PER", "name": "Peru", "region": "South America", "investment": 45, "target_medals": 4},
    {"code": "URU", "name": "Uruguay", "region": "South America", "investment": 35, "target_medals": 3},
    # Overperforming Nations (Slovakia, Georgia, Ethiopia)
    {"code": "SVK", "name": "Slovakia", "region": "Europe/Asia", "investment": 110, "target_medals": 28},
    {"code": "GEO", "name": "Georgia", "region": "Europe/Asia", "investment": 85, "target_medals": 30},
    {"code": "ETH", "name": "Ethiopia", "region": "Africa", "investment": 75, "target_medals": 36},
    # Other African Nations
    {"code": "KEN", "name": "Kenya", "region": "Africa", "investment": 150, "target_medals": 45},
    {"code": "RSA", "name": "South Africa", "region": "Africa", "investment": 220, "target_medals": 24},
    {"code": "EGY", "name": "Egypt", "region": "Africa", "investment": 160, "target_medals": 16},
    {"code": "NGR", "name": "Nigeria", "region": "Africa", "investment": 120, "target_medals": 12},
    {"code": "MAR", "name": "Morocco", "region": "Africa", "investment": 100, "target_medals": 11},
    {"code": "ALG", "name": "Algeria", "region": "Africa", "investment": 80, "target_medals": 9},
    {"code": "UGA", "name": "Uganda", "region": "Africa", "investment": 45, "target_medals": 8},
    # European / Asian nations
    {"code": "ESP", "name": "Spain", "region": "Europe/Asia", "investment": 1100, "target_medals": 68},
    {"code": "SWE", "name": "Sweden", "region": "Europe/Asia", "investment": 850, "target_medals": 64},
    {"code": "NOR", "name": "Norway", "region": "Europe/Asia", "investment": 800, "target_medals": 75},
    {"code": "SUI", "name": "Switzerland", "region": "Europe/Asia", "investment": 850, "target_medals": 58},
    {"code": "POL", "name": "Poland", "region": "Europe/Asia", "investment": 650, "target_medals": 54},
    {"code": "UKR", "name": "Ukraine", "region": "Europe/Asia", "investment": 550, "target_medals": 62},
    {"code": "ROU", "name": "Romania", "region": "Europe/Asia", "investment": 420, "target_medals": 46},
    {"code": "DEN", "name": "Denmark", "region": "Europe/Asia", "investment": 520, "target_medals": 42},
    {"code": "NZL", "name": "New Zealand", "region": "Oceania", "investment": 580, "target_medals": 48},
    {"code": "CZE", "name": "Czech Republic", "region": "Europe/Asia", "investment": 460, "target_medals": 40},
    {"code": "TUR", "name": "Turkey", "region": "Europe/Asia", "investment": 480, "target_medals": 32},
    {"code": "GRE", "name": "Greece", "region": "Europe/Asia", "investment": 520, "target_medals": 30},
    {"code": "KAZ", "name": "Kazakhstan", "region": "Europe/Asia", "investment": 380, "target_medals": 31},
    {"code": "IRI", "name": "Iran", "region": "Europe/Asia", "investment": 320, "target_medals": 28},
    {"code": "JAM", "name": "Jamaica", "region": "North America", "investment": 120, "target_medals": 36},
    {"code": "CRO", "name": "Croatia", "region": "Europe/Asia", "investment": 240, "target_medals": 22},
    {"code": "SRB", "name": "Serbia", "region": "Europe/Asia", "investment": 210, "target_medals": 19},
    {"code": "BLR", "name": "Belarus", "region": "Europe/Asia", "investment": 260, "target_medals": 24},
    {"code": "AZE", "name": "Azerbaijan", "region": "Europe/Asia", "investment": 240, "target_medals": 22},
    {"code": "UZB", "name": "Uzbekistan", "region": "Europe/Asia", "investment": 190, "target_medals": 20},
    {"code": "BEL", "name": "Belgium", "region": "Europe/Asia", "investment": 550, "target_medals": 24},
    {"code": "AUT", "name": "Austria", "region": "Europe/Asia", "investment": 620, "target_medals": 28},
    {"code": "IRL", "name": "Ireland", "region": "Europe/Asia", "investment": 320, "target_medals": 16},
    {"code": "SLO", "name": "Slovenia", "region": "Europe/Asia", "investment": 180, "target_medals": 16},
    {"code": "MEX", "name": "Mexico", "region": "North America", "investment": 420, "target_medals": 18},
    {"code": "IND", "name": "India", "region": "Europe/Asia", "investment": 650, "target_medals": 20},
    {"code": "INA", "name": "Indonesia", "region": "Europe/Asia", "investment": 250, "target_medals": 14},
    {"code": "THA", "name": "Thailand", "region": "Europe/Asia", "investment": 200, "target_medals": 15},
]

# Ensure sum of non-USA/CHN targets exactly fills the remaining medals
current_sum = sum(c["target_medals"] for c in COUNTRIES_DATA)
diff_sum = TOTAL_MEDALS_ACROSS_GAMES - current_sum
print(f"Target sum: {current_sum}, Desired total: {TOTAL_MEDALS_ACROSS_GAMES}, Diff: {diff_sum}")

# Adjust non-key countries proportionally
adjustable = [c for c in COUNTRIES_DATA if c["code"] not in ["USA", "CHN", "JPN", "SVK", "GEO", "ETH"]]
while diff_sum != 0:
    for c in adjustable:
        if diff_sum == 0:
            break
        step = 1 if diff_sum > 0 else -1
        c["target_medals"] += step
        diff_sum -= step

print("Adjusted sum of all countries' target medals:", sum(c["target_medals"] for c in COUNTRIES_DATA))

# 3. 50 Olympic Sports Categories & Disciplines
SPORTS_LIST = [
    {"category": "Rowing", "disciplines": ["Single Sculls", "Double Sculls", "Coxless Pair", "Eight With Coxswain"], "season": "Summer"},
    {"category": "Shooting", "disciplines": ["10m Air Rifle", "50m Rifle 3 Positions", "25m Rapid Fire Pistol", "Trap", "Skeet"], "season": "Summer"},
    {"category": "Aquatics - Swimming", "disciplines": ["Freestyle 100m", "Freestyle 400m", "Backstroke 200m", "Butterfly 100m", "Medley Relay"], "season": "Summer"},
    {"category": "Athletics - Track", "disciplines": ["100m Sprint", "400m", "1500m", "10000m", "110m Hurdles", "4x100m Relay"], "season": "Summer"},
    {"category": "Athletics - Field", "disciplines": ["High Jump", "Long Jump", "Pole Vault", "Shot Put", "Javelin Throw"], "season": "Summer"},
    {"category": "Cycling - Track", "disciplines": ["Sprint", "Team Pursuit", "Keirin", "Omnium"], "season": "Summer"},
    {"category": "Cycling - Road", "disciplines": ["Road Race", "Individual Time Trial"], "season": "Summer"},
    {"category": "Gymnastics - Artistic", "disciplines": ["All-Around", "Floor Exercise", "Vault", "Uneven Bars", "Balance Beam"], "season": "Summer"},
    {"category": "Canoeing - Sprint", "disciplines": ["Kayak Single 1000m", "Canoe Double 500m", "Kayak Four 500m"], "season": "Summer"},
    {"category": "Fencing", "disciplines": ["Individual Foil", "Individual Epee", "Individual Sabre", "Team Foil"], "season": "Summer"},
    {"category": "Judo", "disciplines": ["Extra-Lightweight", "Half-Lightweight", "Middleweight", "Heavyweight"], "season": "Summer"},
    {"category": "Wrestling - Freestyle", "disciplines": ["57kg", "65kg", "74kg", "86kg", "97kg", "125kg"], "season": "Summer"},
    {"category": "Wrestling - Greco-Roman", "disciplines": ["60kg", "67kg", "77kg", "87kg", "97kg", "130kg"], "season": "Summer"},
    {"category": "Weightlifting", "disciplines": ["61kg", "73kg", "89kg", "102kg", "+102kg"], "season": "Summer"},
    {"category": "Boxing", "disciplines": ["Flyweight", "Featherweight", "Lightweight", "Middleweight", "Heavyweight"], "season": "Summer"},
    {"category": "Sailing", "disciplines": ["Laser", "49er", "Nacra 17", "Windsurfing iQFoil"], "season": "Summer"},
    {"category": "Equestrian", "disciplines": ["Dressage", "Eventing", "Jumping"], "season": "Summer"},
    {"category": "Archery", "disciplines": ["Individual Recurve", "Team Recurve", "Mixed Team"], "season": "Summer"},
    {"category": "Badminton", "disciplines": ["Men Singles", "Women Singles", "Men Doubles", "Mixed Doubles"], "season": "Summer"},
    {"category": "Table Tennis", "disciplines": ["Men Singles", "Women Singles", "Team Men", "Mixed Doubles"], "season": "Summer"},
    {"category": "Tennis", "disciplines": ["Men Singles", "Women Singles", "Men Doubles", "Mixed Doubles"], "season": "Summer"},
    {"category": "Taekwondo", "disciplines": ["Flyweight", "Featherweight", "Welterweight", "Heavyweight"], "season": "Summer"},
    {"category": "Triathlon", "disciplines": ["Individual Olympic Distance", "Mixed Relay"], "season": "Summer"},
    {"category": "Diving", "disciplines": ["3m Springboard", "10m Platform", "Synchronised 3m", "Synchronised 10m"], "season": "Summer"},
    {"category": "Artistic Swimming", "disciplines": ["Duet Free", "Team Free Routine"], "season": "Summer"},
    {"category": "Water Polo", "disciplines": ["Tournament Men", "Tournament Women"], "season": "Summer"},
    {"category": "Basketball", "disciplines": ["5x5 Tournament", "3x3 Tournament"], "season": "Summer"},
    {"category": "Volleyball", "disciplines": ["Indoor Volleyball", "Beach Volleyball"], "season": "Summer"},
    {"category": "Football", "disciplines": ["Tournament Men", "Tournament Women"], "season": "Summer"},
    {"category": "Handball", "disciplines": ["Tournament Men", "Tournament Women"], "season": "Summer"},
    {"category": "Field Hockey", "disciplines": ["Tournament Men", "Tournament Women"], "season": "Summer"},
    {"category": "Rugby Sevens", "disciplines": ["Tournament Men", "Tournament Women"], "season": "Summer"},
    {"category": "Modern Pentathlon", "disciplines": ["Individual Men", "Individual Women"], "season": "Summer"},
    {"category": "Skateboarding", "disciplines": ["Street", "Park"], "season": "Summer"},
    {"category": "Sport Climbing", "disciplines": ["Boulder & Lead", "Speed"], "season": "Summer"},
    {"category": "Surfing", "disciplines": ["Shortboard Men", "Shortboard Women"], "season": "Summer"},
    {"category": "Golf", "disciplines": ["Individual Stroke Play Men", "Individual Stroke Play Women"], "season": "Summer"},
    {"category": "BMX Cycling", "disciplines": ["BMX Racing", "BMX Freestyle"], "season": "Summer"},
    {"category": "Trampoline Gymnastics", "disciplines": ["Individual Men", "Individual Women"], "season": "Summer"},
    {"category": "Rhythmic Gymnastics", "disciplines": ["Individual All-Around", "Group All-Around"], "season": "Summer"},
    # Winter Sports (including 2026 Milano-Cortina)
    {"category": "Alpine Skiing", "disciplines": ["Downhill", "Super-G", "Giant Slalom", "Slalom", "Combined"], "season": "Winter"},
    {"category": "Biathlon", "disciplines": ["Sprint 10km", "Pursuit 12.5km", "Individual 20km", "Relay 4x7.5km"], "season": "Winter"},
    {"category": "Cross-Country Skiing", "disciplines": ["15km Classical", "30km Skiathlon", "50km Freestyle", "Sprint"], "season": "Winter"},
    {"category": "Figure Skating", "disciplines": ["Men Single", "Women Single", "Pair Skating", "Ice Dance", "Team Event"], "season": "Winter"},
    {"category": "Speed Skating", "disciplines": ["500m", "1000m", "1500m", "5000m", "Team Pursuit"], "season": "Winter"},
    {"category": "Short Track Speed Skating", "disciplines": ["500m", "1000m", "1500m", "5000m Relay"], "season": "Winter"},
    {"category": "Snowboard", "disciplines": ["Halfpipe", "Slopestyle", "Big Air", "Snowboard Cross"], "season": "Winter"},
    {"category": "Freestyle Skiing", "disciplines": ["Moguls", "Aerials", "Halfpipe", "Slopestyle", "Ski Cross"], "season": "Winter"},
    {"category": "Ice Hockey", "disciplines": ["Tournament Men", "Tournament Women"], "season": "Winter"},
    {"category": "Bobsleigh & Skeleton", "disciplines": ["Two-Man", "Four-Man", "Women Monobob", "Skeleton Individual"], "season": "Winter"},
]

# Set athlete counts: Rowing = 24, Shooting = 26
sport_athlete_counts = {}
for sport in SPORTS_LIST:
    cat = sport["category"]
    if cat == "Rowing":
        sport_athlete_counts[cat] = 24
    elif cat == "Shooting":
        sport_athlete_counts[cat] = 26
    elif "Aquatics" in cat or "Athletics" in cat:
        sport_athlete_counts[cat] = random.randint(180, 240)
    elif "Gymnastics" in cat or "Cycling" in cat:
        sport_athlete_counts[cat] = random.randint(90, 140)
    elif sport["season"] == "Winter":
        sport_athlete_counts[cat] = random.randint(60, 110)
    else:
        sport_athlete_counts[cat] = random.randint(45, 85)

first_names_male = ["James", "Michael", "David", "Wei", "Hiroshi", "Jean", "Marco", "Carlos", "Ole", "Dmitry", "Matej", "Kenenisa", "Luka", "Sanjay", "Johan", "Robert", "John"]
first_names_female = ["Emma", "Jennifer", "Ling", "Yuki", "Chloe", "Sofia", "Camila", "Marit", "Elena", "Zuzana", "Tirunesh", "Ana", "Priya", "Astrid", "Sarah", "Emily"]
last_names = ["Smith", "Johnson", "Wang", "Li", "Sato", "Takahashi", "Dubois", "Rossi", "Silva", "Hernandez", "Bjoerndalen", "Ivanov", "Novak", "Bekele", "Garcia", "Kim", "Park", "Muller", "Schmidt"]

athletes_records = []
athlete_id_counter = 10001
sport_to_athletes = {}

for sport in SPORTS_LIST:
    cat = sport["category"]
    disciplines = sport["disciplines"]
    season = sport["season"]
    count = sport_athlete_counts[cat]
    sport_to_athletes[cat] = []
    
    for _ in range(count):
        gender = random.choice(["Male", "Female"])
        first_name = random.choice(first_names_male if gender == "Male" else first_names_female)
        last_name = random.choice(last_names)
        country = random.choice(COUNTRIES_DATA)
        
        ath = {
            "Athlete_ID": athlete_id_counter,
            "Athlete_Name": f"{first_name} {last_name}",
            "Gender": gender,
            "Age": random.randint(19, 36),
            "Height_cm": random.randint(165, 198) if gender == "Male" else random.randint(155, 185),
            "Weight_kg": random.randint(62, 105) if gender == "Male" else random.randint(48, 82),
            "Country_Code": country["code"],
            "Country_Name": country["name"],
            "Region": country["region"],
            "Sport_Category": cat,
            "Primary_Discipline": random.choice(disciplines),
            "Season": season
        }
        athletes_records.append(ath)
        sport_to_athletes[cat].append(ath)
        athlete_id_counter += 1

athletes_df = pd.DataFrame(athletes_records)

# 4. Matrix of medals: country x year
# Constraints:
# sum across all countries for year y == EDITIONS[y].total_medals
# sum across all years for country c == c.target_medals
# USA in 1996 = 100
# China in 2008 = 93
# Japan in 2020 = 105

country_codes = [c["code"] for c in COUNTRIES_DATA]
c_targets = {c["code"]: c["target_medals"] for c in COUNTRIES_DATA}
y_targets = {e["year"]: e["total_medals"] for e in EDITIONS}

grid = {c: {y: 0 for y in YEARS} for c in country_codes}

# Fix host specials
grid["USA"][1996] = 100
grid["CHN"][2008] = 93
grid["JPN"][2020] = 105

# Remaining allocations
# USA (735 - 100 = 635)
usa_rem_years = [y for y in YEARS if y != 1996]
usa_dist = [70, 72, 75, 78, 80, 85, 75, 70, 30] # 635
for y, m in zip(usa_rem_years, usa_dist):
    grid["USA"][y] = m

# CHN (696 - 93 = 603)
chn_rem_years = [y for y in YEARS if y != 2008]
chn_dist = [52, 54, 58, 65, 78, 70, 82, 84, 60] # 603
for y, m in zip(chn_rem_years, chn_dist):
    grid["CHN"][y] = m

# JPN (165 - 105 = 60)
jpn_rem_years = [y for y in YEARS if y != 2020]
jpn_dist = [6, 6, 6, 7, 7, 7, 7, 8, 6] # 60
for y, m in zip(jpn_rem_years, jpn_dist):
    grid["JPN"][y] = m

# For other countries, populate iteratively while satisfying edition targets and country targets
other_countries = [c for c in country_codes if c not in ["USA", "CHN", "JPN"]]

# Calculate initial edition deficits
ed_deficits = {y: y_targets[y] - (grid["USA"][y] + grid["CHN"][y] + grid["JPN"][y]) for y in YEARS}
c_deficits = {c: c_targets[c] for c in other_countries}

# Proportional seeding
for c in other_countries:
    c_target = c_deficits[c]
    total_ed_deficit = sum(ed_deficits.values())
    for y in YEARS:
        val = int(round(c_target * (ed_deficits[y] / total_ed_deficit)))
        grid[c][y] = max(0, val)

# Exact adjustment algorithm (iterative proportional fitting / transport balance)
for _ in range(500):
    # Adjust across editions for each country
    for c in other_countries:
        cur_c_sum = sum(grid[c][y] for y in YEARS)
        c_diff = c_targets[c] - cur_c_sum
        if c_diff != 0:
            step = 1 if c_diff > 0 else -1
            # Pick year with largest edition discrepancy in the same direction
            years_sorted = sorted(YEARS, key=lambda y: (y_targets[y] - sum(grid[k][y] for k in country_codes)) * step, reverse=True)
            for y in years_sorted:
                if step > 0 or grid[c][y] > 0:
                    grid[c][y] += step
                    c_diff -= step
                    if c_diff == 0:
                        break

    # Adjust across countries for each edition
    for y in YEARS:
        cur_y_sum = sum(grid[k][y] for k in country_codes)
        y_diff = y_targets[y] - cur_y_sum
        if y_diff != 0:
            step = 1 if y_diff > 0 else -1
            c_sorted = sorted(other_countries, key=lambda c: (c_targets[c] - sum(grid[c][yr] for yr in YEARS)) * step, reverse=True)
            for c in c_sorted:
                if step > 0 or grid[c][y] > 0:
                    grid[c][y] += step
                    y_diff -= step
                    if y_diff == 0:
                        break

# Final check of country sums and edition sums
print("Final Edition Checks:")
for ed in EDITIONS:
    y = ed["year"]
    tot = sum(grid[c][y] for c in country_codes)
    print(f"  Year {y}: {tot} medals (Target was: {ed['total_medals']})")

print(f"USA Total Medals: {sum(grid['USA'].values())}")
print(f"CHN Total Medals: {sum(grid['CHN'].values())}")
print(f"JPN Tokyo 2020 Medals: {grid['JPN'][2020]}")

# 5. Create Medal Records with Exact Sport Targets
# Rowing = 166 medals (166 / 24 = 6.916)
# Shooting = 175 medals (175 / 26 = 6.731)
rowing_target = 166
shooting_target = 175
sport_assigned_medals = {s["category"]: 0 for s in SPORTS_LIST}

medal_records = []
medal_id_counter = 50001

for ed in EDITIONS:
    year = ed["year"]
    season = ed["season"]
    city = ed["city"]
    host_country = ed["country"]
    season_sports = [s for s in SPORTS_LIST if s["season"] == season]
    
    for c in COUNTRIES_DATA:
        code = c["code"]
        med_count = grid[code][year]
        if med_count == 0:
            continue
            
        gold_c = int(round(med_count * 0.35))
        silver_c = int(round(med_count * 0.33))
        bronze_c = med_count - gold_c - silver_c
        med_types = ["Gold"] * gold_c + ["Silver"] * silver_c + ["Bronze"] * bronze_c
        
        for m_type in med_types:
            cat = None
            if season == "Summer":
                if sport_assigned_medals["Rowing"] < rowing_target and (code in ["GBR", "USA", "GER", "AUS", "NED", "NZL", "ROU", "ITA"] or random.random() < 0.12):
                    cat = "Rowing"
                elif sport_assigned_medals["Shooting"] < shooting_target and (code in ["CHN", "USA", "ITA", "KOR", "IND", "RUS", "GER", "SUI"] or random.random() < 0.12):
                    cat = "Shooting"
            
            if cat is None:
                avail_sports = [s for s in season_sports if s["category"] not in ["Rowing", "Shooting"]]
                if not avail_sports:
                    avail_sports = season_sports
                cat = random.choice(avail_sports)["category"]
            
            sport_assigned_medals[cat] += 1
            
            # Select an athlete
            cat_athletes = sport_to_athletes[cat]
            ath = random.choice(cat_athletes)
            
            s_obj = next(s for s in SPORTS_LIST if s["category"] == cat)
            disc = random.choice(s_obj["disciplines"])
            
            medal_records.append({
                "Medal_ID": medal_id_counter,
                "Year": year,
                "Season": season,
                "Host_City": city,
                "Host_Country": host_country,
                "Country_Code": code,
                "Country_Name": c["name"],
                "Region": c["region"],
                "Sport_Category": cat,
                "Discipline": disc,
                "Event_Gender": ath["Gender"],
                "Medal": m_type,
                "Athlete_ID": ath["Athlete_ID"],
                "Athlete_Name": ath["Athlete_Name"]
            })
            medal_id_counter += 1

medals_df = pd.DataFrame(medal_records)

# Fine-tune Rowing (166) and Shooting (175) to exact target
row_diff = rowing_target - (medals_df["Sport_Category"] == "Rowing").sum()
shoot_diff = shooting_target - (medals_df["Sport_Category"] == "Shooting").sum()

if row_diff != 0:
    candidates = medals_df[(medals_df["Season"] == "Summer") & (medals_df["Sport_Category"] != "Rowing") & (medals_df["Sport_Category"] != "Shooting")].index
    if row_diff > 0:
        replace_idx = np.random.choice(candidates, size=row_diff, replace=False)
        medals_df.loc[replace_idx, "Sport_Category"] = "Rowing"
        medals_df.loc[replace_idx, "Discipline"] = "Single Sculls"
        for idx in replace_idx:
            ath = random.choice(sport_to_athletes["Rowing"])
            medals_df.loc[idx, "Athlete_ID"] = ath["Athlete_ID"]
            medals_df.loc[idx, "Athlete_Name"] = ath["Athlete_Name"]

if shoot_diff != 0:
    candidates = medals_df[(medals_df["Season"] == "Summer") & (medals_df["Sport_Category"] != "Rowing") & (medals_df["Sport_Category"] != "Shooting")].index
    if shoot_diff > 0:
        replace_idx = np.random.choice(candidates, size=shoot_diff, replace=False)
        medals_df.loc[replace_idx, "Sport_Category"] = "Shooting"
        medals_df.loc[replace_idx, "Discipline"] = "10m Air Rifle"
        for idx in replace_idx:
            ath = random.choice(sport_to_athletes["Shooting"])
            medals_df.loc[idx, "Athlete_ID"] = ath["Athlete_ID"]
            medals_df.loc[idx, "Athlete_Name"] = ath["Athlete_Name"]

# Re-check exact values:
r_med = (medals_df["Sport_Category"] == "Rowing").sum()
r_ath = len(sport_to_athletes["Rowing"])
s_med = (medals_df["Sport_Category"] == "Shooting").sum()
s_ath = len(sport_to_athletes["Shooting"])

print("================ FINAL BENCHMARK VERIFICATION ================")
print(f"Rowing: Medals={r_med}, Athletes={r_ath}, Avg Medals per Athlete={r_med / r_ath:.3f} (Benchmark: 6.916)")
print(f"Shooting: Medals={s_med}, Athletes={s_ath}, Avg Medals per Athlete={s_med / s_ath:.3f} (Benchmark: 6.731)")
print(f"USA Total Medals: {(medals_df['Country_Code'] == 'USA').sum()} (Benchmark: 735)")
print(f"China Total Medals: {(medals_df['Country_Code'] == 'CHN').sum()} (Benchmark: 696)")
print(f"Year 2000 Medals: {(medals_df['Year'] == 2000).sum()} (Benchmark: 305)")
print(f"Year 2020 Medals: {(medals_df['Year'] == 2020).sum()} (Benchmark: 363)")
print(f"Year 2026 Medals: {(medals_df['Year'] == 2026).sum()} (Benchmark: 334)")
print("==============================================================")

# 6. Country Sports Investment Dataset
country_investment_records = []
for c in COUNTRIES_DATA:
    code = c["code"]
    name = c["name"]
    region = c["region"]
    base_inv = c["investment"]
    
    for y in YEARS:
        y_medals = int(grid[code][y])
        y_gold = ((medals_df["Country_Code"] == code) & (medals_df["Year"] == y) & (medals_df["Medal"] == "Gold")).sum()
        y_silver = ((medals_df["Country_Code"] == code) & (medals_df["Year"] == y) & (medals_df["Medal"] == "Silver")).sum()
        y_bronze = ((medals_df["Country_Code"] == code) & (medals_df["Year"] == y) & (medals_df["Medal"] == "Bronze")).sum()
        
        y_inv = round((base_inv / 10.0) * (0.8 + 0.4 * (y - 1992)/34.0), 2)
        hp_budget = round(y_inv * 0.65, 2)
        
        # Medal efficiency percentage
        # For Carlos: Slovakia, Georgia, Ethiopia have exceptionally high medal efficiency %
        if code in ["SVK", "GEO", "ETH"]:
            efficiency_pct = round((y_medals / max(1.0, y_inv)) * 140.0, 2)
        elif region == "South America":
            efficiency_pct = round(49.64 + random.uniform(-4.0, 4.0), 2)
        elif region == "Europe/Asia":
            efficiency_pct = round(45.98 + random.uniform(-5.0, 5.0), 2)
        else:
            efficiency_pct = round((y_medals / max(1.0, y_inv)) * 80.0, 2)
            
        cost_per_medal = round(y_inv / max(1, y_medals), 2)
        
        country_investment_records.append({
            "Country_Code": code,
            "Country_Name": name,
            "Region": region,
            "Year": y,
            "Sports_Investment_USD_M": y_inv,
            "High_Performance_Budget_USD_M": hp_budget,
            "Medals_Total": y_medals,
            "Gold_Medals": y_gold,
            "Silver_Medals": y_silver,
            "Bronze_Medals": y_bronze,
            "Medal_Efficiency_Pct": efficiency_pct,
            "Cost_Per_Medal_M": cost_per_medal
        })

investment_df = pd.DataFrame(country_investment_records)

# 7. Regional Efficiency Dataset
# Target: South America leads at 49.64%, followed by Europe/Asia at 45.98%
regional_benchmarks = [
    {"Region": "South America", "Average_Medal_Efficiency_Pct": 49.64, "Total_Investment_USD_M": 1720, "Total_Medals": 112, "Athlete_Count": 420, "Medals_Per_Athlete": 0.267},
    {"Region": "Europe/Asia", "Average_Medal_Efficiency_Pct": 45.98, "Total_Investment_USD_M": 28400, "Total_Medals": 2210, "Athlete_Count": 2450, "Medals_Per_Athlete": 0.902},
    {"Region": "Africa", "Average_Medal_Efficiency_Pct": 41.25, "Total_Investment_USD_M": 980, "Total_Medals": 160, "Athlete_Count": 380, "Medals_Per_Athlete": 0.421},
    {"Region": "North America", "Average_Medal_Efficiency_Pct": 38.45, "Total_Investment_USD_M": 7480, "Total_Medals": 894, "Athlete_Count": 850, "Medals_Per_Athlete": 1.052},
    {"Region": "Oceania", "Average_Medal_Efficiency_Pct": 34.20, "Total_Investment_USD_M": 2950, "Total_Medals": 188, "Athlete_Count": 320, "Medals_Per_Athlete": 0.588},
]
regional_df = pd.DataFrame(regional_benchmarks)

# 8. Host Performance Dataset
host_records = [
    {"Host_Country": "Japan", "Country_Code": "JPN", "Host_Year": 2020, "Host_City": "Tokyo", "Host_Medals": 105, "Non_Host_Avg_Medals": 6.67, "Host_Advantage_Pct": 1475.0, "Global_Rank_When_Hosting": 1},
    {"Host_Country": "United States", "Country_Code": "USA", "Host_Year": 1996, "Host_City": "Atlanta", "Host_Medals": 100, "Non_Host_Avg_Medals": 70.55, "Host_Advantage_Pct": 41.74, "Global_Rank_When_Hosting": 1},
    {"Host_Country": "China", "Country_Code": "CHN", "Host_Year": 2008, "Host_City": "Beijing", "Host_Medals": 93, "Non_Host_Avg_Medals": 67.0, "Host_Advantage_Pct": 38.81, "Global_Rank_When_Hosting": 1},
    {"Host_Country": "Great Britain", "Country_Code": "GBR", "Host_Year": 2012, "Host_City": "London", "Host_Medals": 65, "Non_Host_Avg_Medals": 13.3, "Host_Advantage_Pct": 388.72, "Global_Rank_When_Hosting": 3},
    {"Host_Country": "Australia", "Country_Code": "AUS", "Host_Year": 2000, "Host_City": "Sydney", "Host_Medals": 58, "Non_Host_Avg_Medals": 9.1, "Host_Advantage_Pct": 537.36, "Global_Rank_When_Hosting": 4},
    {"Host_Country": "Spain", "Country_Code": "ESP", "Host_Year": 1992, "Host_City": "Barcelona", "Host_Medals": 22, "Non_Host_Avg_Medals": 5.1, "Host_Advantage_Pct": 331.37, "Global_Rank_When_Hosting": 6},
    {"Host_Country": "Greece", "Country_Code": "GRE", "Host_Year": 2004, "Host_City": "Athens", "Host_Medals": 16, "Non_Host_Avg_Medals": 1.5, "Host_Advantage_Pct": 966.67, "Global_Rank_When_Hosting": 15},
    {"Host_Country": "Brazil", "Country_Code": "BRA", "Host_Year": 2016, "Host_City": "Rio de Janeiro", "Host_Medals": 19, "Non_Host_Avg_Medals": 3.2, "Host_Advantage_Pct": 493.75, "Global_Rank_When_Hosting": 13},
    {"Host_Country": "France", "Country_Code": "FRA", "Host_Year": 2024, "Host_City": "Paris", "Host_Medals": 64, "Non_Host_Avg_Medals": 7.8, "Host_Advantage_Pct": 720.51, "Global_Rank_When_Hosting": 5},
    {"Host_Country": "Italy", "Country_Code": "ITA", "Host_Year": 2026, "Host_City": "Milano-Cortina", "Host_Medals": 30, "Non_Host_Avg_Medals": 10.0, "Host_Advantage_Pct": 200.0, "Global_Rank_When_Hosting": 4},
]
host_df = pd.DataFrame(host_records)

# 9. Sport Category Metrics
sport_metrics_list = []
for s in SPORTS_LIST:
    cat = s["category"]
    cat_medals = (medals_df["Sport_Category"] == cat).sum()
    cat_ath_count = len(sport_to_athletes[cat])
    avg_med = round(cat_medals / cat_ath_count, 3)
    sport_metrics_list.append({
        "Sport_Category": cat,
        "Season": s["season"],
        "Total_Medals": cat_medals,
        "Athlete_Count": cat_ath_count,
        "Avg_Medals_Per_Athlete": avg_med,
        "Gold_Medals": ((medals_df["Sport_Category"] == cat) & (medals_df["Medal"] == "Gold")).sum(),
        "Silver_Medals": ((medals_df["Sport_Category"] == cat) & (medals_df["Medal"] == "Silver")).sum(),
        "Bronze_Medals": ((medals_df["Sport_Category"] == cat) & (medals_df["Medal"] == "Bronze")).sum(),
        "Disciplines_Count": len(s["disciplines"])
    })
sport_metrics_df = pd.DataFrame(sport_metrics_list).sort_values("Avg_Medals_Per_Athlete", ascending=False)

# Save RAW CSV Files
athletes_df.to_csv(os.path.join(RAW_DATA_DIR, "athletes.csv"), index=False)
medals_df.to_csv(os.path.join(RAW_DATA_DIR, "medal_results.csv"), index=False)
investment_df.to_csv(os.path.join(RAW_DATA_DIR, "country_sports_investment.csv"), index=False)
host_df.to_csv(os.path.join(RAW_DATA_DIR, "host_performance.csv"), index=False)
regional_df.to_csv(os.path.join(RAW_DATA_DIR, "regional_efficiency.csv"), index=False)
sport_metrics_df.to_csv(os.path.join(RAW_DATA_DIR, "sport_category_metrics.csv"), index=False)

# Create Master Merged Dataset for Tableau & Web App
master_df = medals_df.merge(
    athletes_df[["Athlete_ID", "Age", "Height_cm", "Weight_kg", "Primary_Discipline"]],
    on="Athlete_ID",
    how="left"
)
master_df = master_df.merge(
    regional_df[["Region", "Average_Medal_Efficiency_Pct"]],
    on="Region",
    how="left"
)
master_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "olympic_merged_master.csv"), index=False)

# SQLite Relational Database
conn = sqlite3.connect(DB_PATH)
athletes_df.to_sql("athletes", conn, if_exists="replace", index=False)
medals_df.to_sql("medal_results", conn, if_exists="replace", index=False)
investment_df.to_sql("country_sports_investment", conn, if_exists="replace", index=False)
host_df.to_sql("host_performance", conn, if_exists="replace", index=False)
regional_df.to_sql("regional_efficiency", conn, if_exists="replace", index=False)
sport_metrics_df.to_sql("sport_category_metrics", conn, if_exists="replace", index=False)
master_df.to_sql("olympic_master_view", conn, if_exists="replace", index=False)

conn.execute("CREATE INDEX IF NOT EXISTS idx_medals_year ON medal_results(Year);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_medals_country ON medal_results(Country_Code);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_medals_sport ON medal_results(Sport_Category);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_athletes_sport ON athletes(Sport_Category);")
conn.commit()
conn.close()

print(f"All datasets generated and committed to SQLite Database at {DB_PATH}")
