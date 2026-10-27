/**
 * Global Olympic Sports Performance Analysis (1992 - 2026)
 * Client-Side Chart Rendering & Scenario Interactivity
 */

// Global Chart Defaults for dark Olympic theme
if (typeof Chart !== "undefined") {
    Chart.defaults.color = "#9cb3c9";
    Chart.defaults.borderColor = "rgba(39, 71, 117, 0.5)";
    Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial";
}

// 1. Render Priya's Dashboard: Sport Category Yield & Country Performance
function initPriyaDashboard() {
    // 1A. Avg Medals per Athlete Horizontal Bar Chart
    fetch("/api/sports-yield")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("sportYieldChart");
            if (!ctx) return;
            
            // Top 15 sports
            const labels = data.categories.slice(0, 15);
            const yields = data.yields.slice(0, 15);
            
            // Highlight Rowing (6.916) and Shooting (6.731) with Gold / Cyan
            const backgroundColors = labels.map(label => {
                if (label === "Rowing") return "#FFD700"; // Gold highlight
                if (label === "Shooting") return "#00d2ff"; // Cyan highlight
                return "rgba(0, 129, 200, 0.7)";
            });

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Avg Medals per Athlete",
                        data: yields,
                        backgroundColor: backgroundColors,
                        borderRadius: 6,
                        borderWidth: 1,
                        borderColor: "#ffffff"
                    }]
                },
                options: {
                    indexAxis: "y",
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: ctx => `Yield: ${ctx.parsed.x} medals/athlete (High ROI)`
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: "Avg Medals Awarded per Athlete", color: "#9cb3c9" },
                            grid: { color: "rgba(39, 71, 117, 0.4)" }
                        },
                        y: {
                            grid: { display: false }
                        }
                    }
                }
            });
        });

    // 1B. Global Performance Metrics by Country (USA 735, CHN 696)
    fetch("/api/global-performance")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("countryPerformanceChart");
            if (!ctx) return;

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.countries.slice(0, 12),
                    datasets: [
                        { label: "Gold", data: data.gold.slice(0, 12), backgroundColor: "#FFD700" },
                        { label: "Silver", data: data.silver.slice(0, 12), backgroundColor: "#C0C0C0" },
                        { label: "Bronze", data: data.bronze.slice(0, 12), backgroundColor: "#CD7F32" }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { stacked: true, grid: { display: false } },
                        y: { stacked: true, title: { display: true, text: "Total Medals" }, grid: { color: "rgba(39, 71, 117, 0.4)" } }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                afterBody: ctx => {
                                    const c = ctx[0].label;
                                    if (c === "United States") return "Total: 735 Medals (Superpower #1)";
                                    if (c === "China") return "Total: 696 Medals (Superpower #2)";
                                }
                            }
                        }
                    }
                }
            });
        });
}

// 2. Render Carlos's Dashboard: Investment vs Performance Bubble & Regional Efficiency Pie
function initCarlosDashboard() {
    // 2A. Investment vs Medal Performance Bubble Chart
    fetch("/api/investment-bubble")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("investmentBubbleChart");
            if (!ctx) return;

            // Formulate bubble dataset
            const bubbleData = data.map(item => ({
                x: item.investment,
                y: item.medals,
                r: Math.max(5, Math.min(25, item.efficiency / 4)),
                country: item.country_name,
                code: item.country_code,
                efficiency: item.efficiency,
                is_highlight: item.is_highlight
            }));

            new Chart(ctx, {
                type: "bubble",
                data: {
                    datasets: [{
                        label: "Nations (Bubble size = Efficiency %)",
                        data: bubbleData,
                        backgroundColor: bubbleData.map(b => {
                            if (b.is_highlight) return "rgba(0, 210, 255, 0.85)"; // Overperformers (SVK, GEO, ETH)
                            if (b.code === "USA" || b.code === "CHN") return "rgba(255, 215, 0, 0.75)";
                            return "rgba(0, 166, 81, 0.5)";
                        }),
                        borderColor: bubbleData.map(b => b.is_highlight ? "#ffffff" : "transparent"),
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: ctx => {
                                    const raw = ctx.raw;
                                    return [
                                        `${raw.country} (${raw.code})`,
                                        `Medals: ${raw.y}`,
                                        `Investment: $${raw.x}M`,
                                        `Medal Efficiency: ${raw.efficiency}%`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: "Total Sports Investment ($ Millions USD)" },
                            grid: { color: "rgba(39, 71, 117, 0.4)" }
                        },
                        y: {
                            title: { display: true, text: "Total Olympic Medals Won" },
                            grid: { color: "rgba(39, 71, 117, 0.4)" }
                        }
                    }
                }
            });
        });

    // 2B. Average Medal Efficiency Percentage by Region Pie Chart (South America 49.64%, Europe/Asia 45.98%)
    fetch("/api/regional-efficiency")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("regionalEfficiencyPie");
            if (!ctx) return;

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: data.regions,
                    datasets: [{
                        data: data.efficiencies,
                        backgroundColor: [
                            "#00A651", // South America (Leader: 49.64%)
                            "#0081C8", // Europe/Asia (45.98%)
                            "#FCB131", // Africa
                            "#EE334E", // North America
                            "#9d4edd"  // Oceania
                        ],
                        borderWidth: 2,
                        borderColor: "#0b1a30"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: "right" },
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.label}: ${ctx.parsed}% Avg Efficiency`
                            }
                        }
                    }
                }
            });
        });
}

// 3. Render William Robert's Dashboard: Longitudinal Trend & Host Advantage
function initWilliamDashboard() {
    // 3A. Trend of Total Medals Awarded Over the Years (Line Chart)
    fetch("/api/yearly-trend")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("yearlyTrendLineChart");
            if (!ctx) return;

            new Chart(ctx, {
                type: "line",
                data: {
                    labels: data.years,
                    datasets: [{
                        label: "Total Medals Awarded",
                        data: data.totals,
                        borderColor: "#00d2ff",
                        backgroundColor: "rgba(0, 210, 255, 0.15)",
                        borderWidth: 3,
                        pointBackgroundColor: data.years.map(y => {
                            if (y === 2000) return "#EE334E"; // Low point 305
                            if (y === 2020) return "#FFD700"; // Peak point 363
                            if (y === 2026) return "#00A651"; // Milano-Cortina 334
                            return "#0081C8";
                        }),
                        pointRadius: 6,
                        pointHoverRadius: 9,
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                afterLabel: ctx => {
                                    const y = data.years[ctx.dataIndex];
                                    if (y === 2000) return "★ Historical Low: 305 Medals (Sydney)";
                                    if (y === 2020) return "★ All-Time Peak: 363 Medals (Tokyo)";
                                    if (y === 2026) return "★ Milano-Cortina 2026: 334 Medals (Winter)";
                                    return `Host: ${data.editions[ctx.dataIndex]}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: { title: { display: true, text: "Olympic Games Edition (1992 - 2026)" } },
                        y: {
                            min: 280,
                            max: 380,
                            title: { display: true, text: "Total Medals Awarded" },
                            grid: { color: "rgba(39, 71, 117, 0.4)" }
                        }
                    }
                }
            });
        });

    // 3B. Comparing Medal Totals Across Olympic Hosts (Bar Chart: Japan 105, USA 100, China 93)
    fetch("/api/host-comparison")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("hostComparisonBarChart");
            if (!ctx) return;

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.hosts,
                    datasets: [
                        {
                            label: "Medals Won When Hosting",
                            data: data.host_medals,
                            backgroundColor: data.hosts.map(h => {
                                if (h.includes("Japan")) return "#FFD700"; // 105
                                if (h.includes("United States")) return "#00d2ff"; // 100
                                if (h.includes("China")) return "#EE334E"; // 93
                                return "rgba(0, 129, 200, 0.6)";
                            }),
                            borderRadius: 6
                        },
                        {
                            label: "Away Games Historical Average",
                            data: data.non_host_avg,
                            backgroundColor: "rgba(156, 179, 201, 0.4)",
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false } },
                        y: { title: { display: true, text: "Medal Count" }, grid: { color: "rgba(39, 71, 117, 0.4)" } }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                afterBody: ctx => {
                                    const idx = ctx[0].dataIndex;
                                    return `Host Advantage Boost: +${data.advantage_pct[idx]}% surge!`;
                                }
                            }
                        }
                    }
                }
            });
        });

    // 3C. Regional Medal Efficiency & Distribution Donut Chart
    fetch("/api/regional-efficiency")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("regionalDonutChart");
            if (!ctx) return;

            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: data.regions,
                    datasets: [{
                        data: data.medals,
                        backgroundColor: ["#0081C8", "#FFD700", "#00A651", "#EE334E", "#9d4edd"],
                        borderWidth: 2,
                        borderColor: "#0b1a30"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "60%",
                    plugins: {
                        legend: { position: "right" }
                    }
                }
            });
        });
}

// 4. Interactive Story Scene Switcher
function showScene(sceneIndex) {
    const tabs = document.querySelectorAll(".story-tab-btn");
    const scenes = document.querySelectorAll(".story-scene");
    
    tabs.forEach((tab, idx) => {
        if (idx === sceneIndex) {
            tab.classList.add("active");
        } else {
            tab.classList.remove("active");
        }
    });

    scenes.forEach((scene, idx) => {
        if (idx === sceneIndex) {
            scene.classList.add("active");
        } else {
            scene.classList.remove("active");
        }
    });
}

// 5. Interactive Data Explorer Filter Engine
function filterDataTable() {
    const year = document.getElementById("filterYear") ? document.getElementById("filterYear").value : "ALL";
    const region = document.getElementById("filterRegion") ? document.getElementById("filterRegion").value : "ALL";
    const sport = document.getElementById("filterSport") ? document.getElementById("filterSport").value : "ALL";
    const medal = document.getElementById("filterMedal") ? document.getElementById("filterMedal").value : "ALL";

    fetch("/api/filter-data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ year, region, sport, medal, limit: 150 })
    })
    .then(res => res.json())
    .then(res => {
        const tbody = document.getElementById("tableBody");
        const countSpan = document.getElementById("recordCount");
        if (countSpan) countSpan.innerText = `${res.count} records matched`;
        if (!tbody) return;

        tbody.innerHTML = "";
        res.data.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${row.Year}</strong> (${row.Season})</td>
                <td>${row.Host_City}</td>
                <td><strong>${row.Country_Name}</strong> (${row.Country_Code})</td>
                <td>${row.Region}</td>
                <td>${row.Sport_Category}</td>
                <td>${row.Discipline}</td>
                <td>${row.Athlete_Name}</td>
                <td><span class="medal-pill medal-${row.Medal}">${row.Medal}</span></td>
            `;
            tbody.appendChild(tr);
        });
    });
}

// Auto-initialize based on page
document.addEventListener("DOMContentLoaded", () => {
    initPriyaDashboard();
    initCarlosDashboard();
    initWilliamDashboard();
    if (document.getElementById("tableBody")) {
        filterDataTable();
    }
});
