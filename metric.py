import pandas as pd
import numpy as np

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
    """
    Compute a metric (sum or mean) for a specific year and key.
    
    Args:
        df (pd.DataFrame): The dataframe
        year_col (str): The name of the year column
        year (int): The year to filter
        key (str): The column key to compute
        agg (str): Aggregation method ('sum' or 'mean')
    
    Returns:
        float or np.nan: The computed metric value
    """
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


def format_number(val, unit=None, is_float=False):
    """
    Format a number with optional unit.
    
    Args:
        val (float): The value to format
        unit (str): Optional unit to append
        is_float (bool): Whether to show decimal places
    
    Returns:
        str: Formatted string
    """
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


def calculate_kpi_values(df, year_col, selected_year, prev_year=None):
    """
    Calculate KPI values and YoY percentage changes.
    
    Args:
        df (pd.DataFrame): The dataframe
        year_col (str): The name of the year column
        selected_year (int): Current year to analyze
        prev_year (int): Previous year for comparison
    
    Returns:
        list: List of dicts with KPI config, current value, previous value, and % change
    """
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
    
    return kpi_values


def prepare_chart_data(df, year_col, years):
    """
    Prepare data aggregated by year for charting.
    
    Args:
        df (pd.DataFrame): The dataframe
        year_col (str): The name of the year column
        years (list): List of years to aggregate
    
    Returns:
        pd.DataFrame: Chart-ready dataframe with Year, KPI, Value, Key columns
    """
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
    
    return pd.DataFrame(chart_data)
