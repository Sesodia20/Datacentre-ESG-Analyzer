import os
import streamlit as st
import pandas as pd
import numpy as np
from gemini_api import generate_esg_analysis, generate_recommendations
from metric import KPI_CONFIG, compute_metric, format_number, calculate_kpi_values, prepare_chart_data
from charts import plot_bar_charts, plot_line_charts

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

# KPI configuration imported from metric.py

# Calculate KPI values and deltas
kpi_values = calculate_kpi_values(df, year_col, selected_year, prev_year)


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
chart_df = prepare_chart_data(df, year_col, years)

# Display bar and line charts using imported functions
plot_bar_charts(chart_df)
plot_line_charts(chart_df)


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
