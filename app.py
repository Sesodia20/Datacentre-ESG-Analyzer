import os
import streamlit as st
import pandas as pd
import numpy as np
from gemini_api import generate_esg_analysis, generate_recommendations
from metric import KPI_CONFIG, compute_metric, format_number, calculate_kpi_values, prepare_chart_data
from charts import plot_bar_charts, plot_line_charts
from styling import apply_page_styling
from analysis import create_pdf_report

st.set_page_config(page_title="Data Centre ESG Analyser", layout="wide")

# Apply page styling with grey background and custom CSS
apply_page_styling()

# Initialize session storage for AI outputs
if "analysis_text" not in st.session_state:
    st.session_state.analysis_text = None
if "recommendations_text" not in st.session_state:
    st.session_state.recommendations_text = None

st.title("Data Centre ESG Analyser")
st.write("Load and analyze ESG data for data centres")

# Sidebar for file selection
with st.sidebar:
    st.header("File Selection")
    # Show two options with a visible prompt
    st.write("**Choose data source:**")
    file_source = st.selectbox("Data source", ("Upload CSV", "Use Default CSV"), index=0, label_visibility="collapsed", key="file_source_radio")

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


# Render KPI cards in 3x2 grid (3 columns, 2 rows)
st.subheader("Key Performance Indicators")

def get_kpi_style(key, value):
    """Determine color style based on metric efficiency"""
    # Green for efficient metrics (lower is better for energy/water/emissions, lower PUE/CUE is better)
    if key in ["energy_kwh", "water_liters", "ghg_emissions_kgco2e", "land_used_m2", "pue", "co2e_per_kwh"]:
        if key == "pue" and value < 1.67:  # PUE < 1.67 is good
            return "light_grey"
        elif key == "co2e_per_kwh" and value < 0.5:  # CUE < 0.5 is good
            return "light_grey"
        elif key in ["energy_kwh", "water_liters", "ghg_emissions_kgco2e"] and value < df[key].median():
            return "light_grey"
        else:
            return "medium_grey"
    return "light_grey"

# Display in 2 rows of 3 columns with styled boxes
for row in range(2):
    cols = st.columns(3)
    for col_idx in range(3):
        item_idx = row * 3 + col_idx
        if item_idx < len(kpi_values):
            item = kpi_values[item_idx]
            cfg = item["cfg"]
            curr = item["curr"]
            pct = item["pct"]
            value_str = format_number(curr, unit=cfg.get("unit"), is_float=cfg.get("is_float", False))
            if pct is None or pd.isna(pct):
                delta_str = "—"
                delta_color = "#888888"
            else:
                delta_str = f"{pct:+.1f}%"
                delta_color = "#00ff00" if pct > 0 else "#ff3333"
            
            # Create styled metric box with border and grey shading
            with cols[col_idx]:
                style = get_kpi_style(cfg["key"], curr)
                # Apply styled container with HTML - embossed design
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
                        border: 2px solid #444444;
                        border-top: 2px solid #555555;
                        border-left: 2px solid #555555;
                        border-bottom: 2px solid #111111;
                        border-right: 2px solid #111111;
                        border-radius: 12px;
                        padding: 20px;
                        min-height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        box-shadow: 
                            inset 0 1px 0 rgba(255,255,255,0.1),
                            0 8px 16px rgba(0,0,0,0.8),
                            0 2px 4px rgba(0,0,0,0.6);
                    ">
                           <div>
                               <p style="margin: 0; color: #ffffff; font-size: 13px; font-weight: 600; font-family: Tahoma, Geneva, Verdana, sans-serif; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9;">{cfg['label']}</p>
                               <p style="margin: 12px 0 0 0; color: #ffffff; font-size: 28px; font-weight: bold; font-family: Tahoma, Geneva, Verdana, sans-serif; text-shadow: 0 2px 4px rgba(0,0,0,0.7); line-height: 1.2;">{value_str}</p>
                           </div>
                           <p style="
                               margin: 0; 
                               color: {delta_color};
                               font-size: 16px; 
                               font-weight: bold;
                               font-family: Tahoma, Geneva, Verdana, sans-serif;
                               padding: 8px 12px;
                               border-radius: 6px;
                               display: inline-block;
                               text-shadow: 0 1px 2px rgba(0,0,0,0.5);
                           ">{delta_str}</p>
                    </div>
                """, unsafe_allow_html=True)


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
        st.write("**Select Analysis Type:**")
        ai_option = st.selectbox(
            "Analysis Type",
            ("Full Analysis", "Energy Focus", "Water Focus", "Emissions Focus"),
            label_visibility="collapsed"
        )

if enable_ai:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate Analysis", key="analyze_btn"):
            with st.spinner("Generating analysis..."):
                analysis = generate_esg_analysis(df, selected_year, prev_year)
                st.session_state.analysis_text = analysis
    
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
                st.session_state.recommendations_text = recommendations

    # Display both sections independently if they exist
    if st.session_state.analysis_text:
        st.markdown("### 📊 ESG Analysis")
        st.write(st.session_state.analysis_text)
    
    if st.session_state.recommendations_text:
        st.markdown("### 💡 Recommendations")
        st.write(st.session_state.recommendations_text)

    # PDF download section
    if st.session_state.analysis_text or st.session_state.recommendations_text:
        st.markdown("### Export AI Output")
        if st.session_state.analysis_text and st.session_state.recommendations_text:
            pdf_bytes = create_pdf_report(
                st.session_state.analysis_text,
                st.session_state.recommendations_text,
                selected_year,
                prev_year,
            )
            st.download_button(
                label="Download PDF (Analysis + Recommendations)",
                data=pdf_bytes,
                file_name=f"esg_report_{selected_year}.pdf",
                mime="application/pdf",
            )
        else:
            st.info("Generate both analysis and recommendations to enable PDF download.")


# Show data preview and simple summary below
st.subheader("Data Preview")

# Style the dataframe with conditional coloring
def style_dataframe(df):
    """Apply conditional styling to dataframe"""
    styled_df = df.copy()
    
    # Create a styler for highlighting efficient vs needs-attention metrics
    def highlight_metrics(val):
        if pd.isna(val) or isinstance(val, (str, int)):
            return ""
        
        # Green for low values (efficient), light red for high values (needs attention)
        if isinstance(val, (float, np.floating)):
            # Assuming lower is better for most metrics
            if val < 1000:
                return "background-color: #90EE90"  # Light green
            elif val > 5000:
                return "background-color: #FFB6C1"  # Light red
        return ""
    
    try:
        return df.style.applymap(highlight_metrics)
    except Exception:
        return df

# Render dataframes with black background and white text via pandas Styler
try:
    styled = df.style.set_properties(**{
        'background-color': '#000000',
        'color': '#ffffff',
        'border-color': '#222222'
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#000000'), ('color', '#ffffff'), ('border-color', '#222222'), ('font-weight', 'bold')]},
        {'selector': 'tbody th', 'props': [('background-color', '#000000'), ('color', '#ffffff'), ('border-color', '#222222'), ('font-weight', 'bold')]},
        {'selector': 'td', 'props': [('background-color', '#000000'), ('color', '#ffffff'), ('border-color', '#222222')]},
        {'selector': 'table', 'props': [('background-color', '#000000'), ('border-collapse', 'collapse')]}
    ])
    st.table(styled)
except Exception:
    st.dataframe(df, use_container_width=True)

st.subheader("Summary Statistics")
try:
    desc_df = df.describe(include="all")
    # Format None/NaN values to be visible
    desc_df = desc_df.fillna('—')
    styled_desc = desc_df.style.set_properties(**{
        'background-color': '#000000',
        'color': '#ffffff',
        'border-color': '#222222'
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#000000'), ('color', '#ffffff'), ('border-color', '#222222'), ('font-weight', 'bold')]},
        {'selector': 'tbody th', 'props': [('background-color', '#000000'), ('color', '#ffffff'), ('border-color', '#222222'), ('font-weight', 'bold')]},
        {'selector': 'td', 'props': [('background-color', '#000000'), ('color', '#ffffff'), ('border-color', '#222222')]},
        {'selector': 'table', 'props': [('background-color', '#000000'), ('border-collapse', 'collapse')]}
    ]).format(lambda x: str(x) if x != 'None' else '—')
    st.table(styled_desc)
except Exception:
    st.dataframe(df.describe(include="all"), use_container_width=True)
