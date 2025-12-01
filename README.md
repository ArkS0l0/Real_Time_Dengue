# 🦟 Dengue Risk Prediction Notebook

## Overview
This notebook provides a **real-time dengue danger assessment system** for Singapore areas. It auto-fetches weather data, real-time case counts, and produces actionable risk scores with mitigation recommendations.

## Features
- ✓ **Auto-fetch weather**: Uses OpenWeatherMap API (real-time humidity, temperature, rainfall)
- ✓ **Real-time dengue cases**: Pulls from local `dengue_cases.csv` or public APIs
- ✓ **Weighted risk scoring**: Combines environmental + epidemiological signals
- ✓ **Danger levels**: High/Medium/Low with action recommendations
- ✓ **Tailored mitigation**: Suggestions based on specific risk drivers
- ✓ **Auto-report**: Saves results to `dengue_report.csv` for historical tracking

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenWeather API Key (Optional but Recommended)
For real-time weather auto-fetch, set an environment variable:

**PowerShell (Current session):**
```powershell
$env:OPENWEATHER_API_KEY = 'YOUR_API_KEY_HERE'
```

**PowerShell (Persistent - Windows):**
```powershell
[Environment]::SetEnvironmentVariable('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE', 'User')
```

Get a free API key: https://openweathermap.org/api

### 3. Populate Dengue Case Data
Edit `dengue_cases.csv` with real case counts and active clusters for your areas:

```csv
area,cases_last_week,active_clusters
Woodlands,39,5
Ang Mo Kio,15,2
...
```

**Data sources:**
- Singapore NEA / MOH weekly dengue updates: https://www.nea.gov.sg/dengue-zika
- Or maintain your own district-level tracking

## Usage

1. Open the notebook in Jupyter Lab / VS Code
2. Run cells sequentially:
   - **Cell 1**: Import libraries
   - **Cell 2**: Input area name (e.g., "Woodlands")
   - **Cell 3**: Auto-fetch real-time dengue cases (from CSV or API)
   - **Cell 4**: Run danger scoring algorithm
   - **Cell 5**: Display color-coded risk level + 4-week timeline
   - **Cell 6**: Save results to report

3. Results are automatically appended to `dengue_report.csv`

## Inputs

| Field | Source | Example |
|-------|--------|---------|
| Area name | User input | Woodlands |
| Construction sites | User input | yes/no |
| Humidity (%) | Weather API or manual | 70 |
| Temperature (°C) | Weather API or manual | 30.8 |
| Recent rainfall (mm) | Weather API or manual | 0.0 |
| Historical cases | `dengue_cases.csv` or user | 39 |
| Active clusters | `dengue_cases.csv` or user | 5 |

## Outputs

### Danger Level (High/Medium/Low)
Based on weighted heuristic (max score: 10):
- **High (≥6)**: Immediate action required
- **Medium (3–5)**: Targeted response
- **Low (<3)**: Routine monitoring

### Recommended Action
Mapped to danger level:
- **High**: "Immediate — Enhanced surveillance, fogging, community alerts, intensive source reduction"
- **Medium**: "Targeted inspections, community outreach, larvicide in hotspots, weekly monitoring"
- **Low**: "Routine monitoring and public education; update weekly"

### Mitigation Suggestions
Dynamically generated based on:
- Construction activity
- Humidity (≥75%)
- Temperature (≥30°C)
- Rainfall (≥50mm)
- Historical cases (≥5)
- Active clusters

Example output for Woodlands:
```
Danger: High (score 8)
Action: Immediate — Enhanced surveillance, fogging where appropriate, community alerts, and intensive source reduction

Suggestions:
- Inspect construction sites and drains; enforce water management
- Focus on outdoor breeding spots; adult mosquitoes more active
- Conduct targeted house-to-house inspections and public awareness
- Prioritize interventions in 5 active clusters; set up temporary response teams
```

## Scoring Algorithm

```
Score = 0
+ 2 if construction sites present
+ (humidity - 60) / 7.5, capped at 2 if humidity > 60%
+ 1.5 if temperature ≥ 30°C
+ 0.8 if temperature 26–29.9°C
+ 2 if recent rainfall ≥ 50mm
+ 1 if recent rainfall 20–49mm
+ 3 if historical cases ≥ 20
+ 1 if historical cases 5–19
+ 1 if active clusters ≥ 3
```

## Reports

Results are saved to `dengue_report.csv` with columns:
- timestamp
- area
- construction
- humidity_pct, temperature_c, rainfall_mm
- historical_cases, danger_score, danger_level
- recommended_action
- suggestions

Use for:
- Historical trend analysis
- Policy effectiveness tracking
- Outbreak correlation studies

## Future Enhancements

- [ ] Integration with WHO dengue surveillance data
- [ ] Machine learning model (trained on historical case-weather correlations)
- [ ] Cluster mapping and geospatial visualization
- [ ] SMS/email alerts for High-danger areas
- [ ] Weekly automated report generation

## License
This tool is provided for public health use. Data accuracy depends on input source quality.

## Contact
For questions or feedback, contact your local health authority or dengue program coordinator.
