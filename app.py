import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from gemini_api import generate_esg_analysis, generate_recommendations

st.set_page_config(page_title="Data Centre ESG Analyser", layout="wide")

st.title("Data Centre ESG Analyser")
st.write("Load and analyze ESG data for data centres")

# Sidebar for file selection
with st.sidebar:
    st.header("File Selection")
    file_source = st.radio("Choose data source:", ("Upload CSV", "Use Default CSV"))

# Load and display data
def find_default_csv():
    candidates = [
        "data/datacentre_env.csv",
        "data/datacentre_env.csv.csv",
        "data/default_data.csv",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def infer_year_column(df: pd.DataFrame):
    # look for a column that contains 'year'
    for col in df.columns:
        if "year" in col.lower():
            return col
    return None


def format_number(val, unit=None, is_float=False):
    if pd.isna(val):
        return "—"
    if is_float:
        s = f"{val:,.2f}"
    else:
        try:
            s = f"{int(val):,}"
        except Exception:
            s = f"{val}"
    return f"{s} {unit}" if unit else s


# Load data (uploaded or default)
df = None
uploaded_file = None
if file_source == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
else:
    default_path = find_default_csv()
    if default_path:
        try:
            df = pd.read_csv(default_path)
            st.success(f"Default data loaded from '{default_path}'")
        except Exception as e:
            st.error(f"Error reading default file: {e}")
    else:
        st.warning("No default CSV found in `data/`. Please upload a CSV file.")

if df is None:
    st.info("Provide a CSV (upload or place a default in `data/`) to enable KPI analysis.")
    st.stop()

# Infer the year column
year_col = infer_year_column(df)
if year_col is None:
    st.error("Could not find a 'year' column in the dataset. Ensure there is a column name containing 'year'.")
    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)
    st.stop()

# Normalize year values to int where possible
try:
    df[year_col] = df[year_col].astype(int)
except Exception:
    # leave as-is if conversion fails
    pass

years = sorted(df[year_col].dropna().unique())
if len(years) == 0:
    st.error("No valid year values found in the year column.")
    st.stop()

# Year selection
st.sidebar.header("Year Selection")
selected_year = st.sidebar.selectbox("Select year (current):", years, index=len(years) - 1)

# Compute previous year (user asked YoY vs previous year)
prev_year = None
years_sorted = sorted(years)
if selected_year in years_sorted:
    idx = years_sorted.index(selected_year)
    if idx > 0:
        prev_year = years_sorted[idx - 1]

# KPI configuration: sum for totals, mean for ratio metrics
KPI_CONFIG = [
    {"key": "energy_kwh", "label": "Energy", "agg": "sum", "unit": "kWh", "is_float": False},
    {"key": "water_liters", "label": "Water", "agg": "sum", "unit": "L", "is_float": False},
    {"key": "ghg_emissions_kgco2e", "label": "Greenhouse Gas Emission", "agg": "sum", "unit": "kgCO2e", "is_float": False},
    {"key": "land_used_m2", "label": "Local Ecosystem", "agg": "sum", "unit": "m²", "is_float": False},
    {"key": "co2e_per_kwh", "label": "Carbon Usage Effectiveness", "agg": "mean", "unit": "kgCO2e/kWh", "is_float": True},
    {"key": "pue", "label": "Power Usage Effectiveness", "agg": "mean", "unit": None, "is_float": True},
]


def compute_metric(df, year_col, year, key, agg):
    sub = df[df[year_col] == year]
    if sub.empty:
        return np.nan
    if key not in sub.columns:
        return np.nan
    if agg == "sum":
        return sub[key].dropna().astype(float).sum()
    elif agg == "mean":
        return sub[key].dropna().astype(float).mean()
    else:
        return np.nan


# Calculate KPI values and deltas
kpi_values = []
for cfg in KPI_CONFIG:
    key = cfg["key"]
    agg = cfg["agg"]
    curr = compute_metric(df, year_col, selected_year, key, agg)
    prev = compute_metric(df, year_col, prev_year, key, agg) if prev_year is not None else np.nan
    if pd.isna(prev) or prev == 0:
        pct = None
    else:
        pct = (curr - prev) / prev * 100
    kpi_values.append({"cfg": cfg, "curr": curr, "prev": prev, "pct": pct})


# Render KPI cards in 6 equal columns
cols = st.columns(6)
for i, item in enumerate(kpi_values):
    cfg = item["cfg"]
    curr = item["curr"]
    pct = item["pct"]
    value_str = format_number(curr, unit=cfg.get("unit"), is_float=cfg.get("is_float", False))
    if pct is None or pd.isna(pct):
        delta_str = "—"
    else:
        delta_str = f"{pct:+.1f}%"
    cols[i].metric(cfg["label"], value_str, delta_str)


# Visualization section
st.subheader("KPI Trends & Analysis")

# Prepare data for charting: aggregate by year
chart_data = []
for year in years:
    for cfg in KPI_CONFIG:
        key = cfg["key"]
        agg = cfg["agg"]
        val = compute_metric(df, year_col, year, key, agg)
        chart_data.append({
            "Year": year,
            "KPI": cfg["label"],
            "Value": val,
            "Key": key
        })

chart_df = pd.DataFrame(chart_data)

# Bar charts for main KPIs (Energy, Water, GHG Emissions, Land)
bar_kpi_keys = ["energy_kwh", "water_liters", "ghg_emissions_kgco2e", "land_used_m2"]
bar_kpi_labels = ["Energy (kWh)", "Water (Liters)", "GHG Emissions (kgCO2e)", "Local Ecosystem (m²)"]

st.write("**Bar Charts: Main KPI Trends**")
bar_cols = st.columns(2)

for idx, (key, label) in enumerate(zip(bar_kpi_keys, bar_kpi_labels)):
    sub = chart_df[chart_df["Key"] == key]
    if not sub.empty:
        fig = px.bar(
            sub,
            x="Year",
            y="Value",
            title=label,
            labels={"Value": label, "Year": "Year"},
            color_discrete_sequence=["#00CED1"]
        )
        fig.update_layout(height=400, showlegend=False)
        fig.update_traces(marker_line_width=0, width=0.5)
        bar_cols[idx % 2].plotly_chart(fig, use_container_width=True)

# Line charts for PUE and CUE (Carbon Usage Effectiveness & Power Usage Effectiveness)
st.write("**Line Charts: Efficiency Metrics Trends**")
line_cols = st.columns(2)

line_kpi_keys = ["pue", "co2e_per_kwh"]
line_kpi_labels = ["Power Usage Effectiveness (PUE)", "Carbon Usage Effectiveness (CUE - kgCO2e/kWh)"]

for idx, (key, label) in enumerate(zip(line_kpi_keys, line_kpi_labels)):
    sub = chart_df[chart_df["Key"] == key]
    if not sub.empty:
        fig = px.line(
            sub,
            x="Year",
            y="Value",
            title=label,
            labels={"Value": label, "Year": "Year"},
            markers=True,
            color_discrete_sequence=["#ff7f0e"]
        )
        fig.update_layout(height=400, showlegend=False)
        line_cols[idx].plotly_chart(fig, use_container_width=True)


# AI-Powered Analysis Section
st.subheader("AI-Powered ESG Analysis & Recommendations")

with st.sidebar:
    st.header("AI Analysis Settings")
    enable_ai = st.checkbox("Enable AI Analysis", value=False)
    
    if enable_ai:
        ai_option = st.radio(
            "Select Analysis Type:",
            ("Full Analysis", "Energy Focus", "Water Focus", "Emissions Focus")
        )

if enable_ai:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate Analysis", key="analyze_btn"):
            with st.spinner("Generating analysis..."):
                analysis = generate_esg_analysis(df, selected_year, prev_year)
                st.write(analysis)
    
    with col2:
        focus_map = {
            "Full Analysis": "overall",
            "Energy Focus": "energy",
            "Water Focus": "water",
            "Emissions Focus": "emissions"
        }
        if st.button("Generate Recommendations", key="recommend_btn"):
            with st.spinner("Generating recommendations..."):
                focus_area = focus_map.get(ai_option, "overall")
                recommendations = generate_recommendations(df, selected_year, prev_year, focus_area)
                st.write(recommendations)


# Show data preview and simple summary below
st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)

st.subheader("Summary Statistics")
st.write(df.describe(include="all"))
