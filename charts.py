import plotly.express as px
import streamlit as st


def plot_bar_charts(chart_df):
    """
    Create and display bar charts for main KPIs (Energy, Water, GHG, Land).
    
    Args:
        chart_df (pd.DataFrame): Chart data with Year, Value, Key columns
    """
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
                color_discrete_sequence=["#9370DB"]
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='#000000',
                paper_bgcolor='#000000',
                font=dict(color='white'),
            )
            fig.update_traces(marker_line_width=0, width=0.5)
            fig.update_xaxes(showgrid=True, gridcolor='#333333', tickfont=dict(color='white'), title_font=dict(color='white'))
            fig.update_yaxes(showgrid=True, gridcolor='#333333', tickfont=dict(color='white'), title_font=dict(color='white'))
            bar_cols[idx % 2].plotly_chart(fig, use_container_width=True)


def plot_line_charts(chart_df):
    """
    Create and display line charts for efficiency metrics (PUE, CUE).
    
    Args:
        chart_df (pd.DataFrame): Chart data with Year, Value, Key columns
    """
    line_kpi_keys = ["pue", "co2e_per_kwh"]
    line_kpi_labels = ["Power Usage Effectiveness (PUE)", "Carbon Usage Effectiveness (CUE - kgCO2e/kWh)"]

    st.write("**Line Charts: Efficiency Metrics Trends**")
    line_cols = st.columns(2)

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
            fig.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='#000000',
                paper_bgcolor='#000000',
                font=dict(color='white'),
                legend=dict(bgcolor='rgba(0,0,0,0)')
            )
            fig.update_xaxes(showgrid=True, gridcolor='#333333', tickfont=dict(color='white'), title_font=dict(color='white'))
            fig.update_yaxes(showgrid=True, gridcolor='#333333', tickfont=dict(color='white'), title_font=dict(color='white'))
            line_cols[idx].plotly_chart(fig, use_container_width=True)
