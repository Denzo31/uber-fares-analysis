# 🚖 Uber Fares Dataset Analysis using Power BI

This project is part of the *Introduction to Big Data Analytics (INSY 8413)* course at Adventist University of Central Africa (AUCA). It provides an end-to-end analysis of the Uber Fares dataset, combining Python-based preprocessing with interactive Power BI dashboards for visualization and insight generation.

## 📁 Project Structure

```plaintext
uber-fares-analysis/
├── data/
│   ├── raw/
│   │   └── uber_fares_raw.csv
│   └── processed/
│       └── uber_fares_cleaned_enhanced.csv
├── scripts/
│   └── eda_analysis.py
├── powerbi/
│   └── uber_analysis_dashboard.pbix
├── screenshots/
│   ├── image1.png
│   ├── image2.png
│   ├── image3.png
│   └── image4.png
├── reports/
│   └── analysis_report.pdf
└── README.md
```
# 📊 Tools and Technologies
Python (Pandas, NumPy): Data preprocessing and feature engineering

Power BI: Interactive dashboard creation

DAX: Custom calculations and KPIs

GitHub: Version control and documentation

# 🧪 Methodology
1. Data Cleaning
Removed missing and invalid entries

Normalized passenger counts

Calculated distances using Haversine formula

2. Feature Engineering
Extracted time features (hour, weekday, etc.)

Added fare per km and trip categories

Identified peak/off-peak time periods

3. Visualization
Four-page Power BI dashboard:

Executive Summary

Temporal Analysis

Geographic Analysis

Passenger & Pricing Analysis

# 📌 Key Insights
Most rides happen during rush hours (7–9 AM, 5–7 PM)

Single-passenger rides dominate (69.6%)

Fare distribution centered around $8.00

Higher revenue per ride in cross-borough and airport trips

# 🧠 Business Recommendations
Introduce dynamic surge pricing during peak hours

Offer incentives for drivers in underserved areas

Expand into geographic hotspots with high fare potential

# 🛠 Future Work
Integrate real-time data streams

Use weather and event data for demand forecasting

Explore machine learning for predictive analytics

# 📄 Author
RUTAGANIRA SHEMA Derrick
Group E | Student ID: 26506
Instructor: Eric Maniraguha
Course: INSY 8413 - Introduction to Big Data Analytics

# 📅 Submission Date: July 27, 2025
# 🎓 Institution: Adventist University of Central Africa (AUCA)
