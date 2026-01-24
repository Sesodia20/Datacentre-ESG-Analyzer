import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API (optional - may not be present)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize model only if API key exists
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def is_api_available():
    """
    Check if Gemini API is configured and available.
    
    Returns:
        bool: True if API key is set, False otherwise
    """
    return GEMINI_API_KEY is not None and model is not None


def compute_metric(df, year_col, year, key, agg="sum"):
    """Helper function to compute metrics"""
    sub = df[df[year_col] == year]
    if sub.empty or key not in sub.columns:
        return None
    if agg == "sum":
        return sub[key].dropna().astype(float).sum()
    elif agg == "mean":
        return sub[key].dropna().astype(float).mean()
    return None


def generate_esg_analysis(df, selected_year, prev_year=None):
    """
    Generate ESG analysis with YoY comparisons, risks, and improvement areas.
    
    Args:
        df (pd.DataFrame): The ESG data
        selected_year (int): The selected year for analysis
        prev_year (int): The previous year for comparison
    
    Returns:
        str: Analysis text from Gemini
        
    Raises:
        RuntimeError: If Gemini API is not configured
        ValueError: If data is invalid or incomplete
    """
    if not is_api_available():
        raise RuntimeError("Gemini API key is not configured. Please add GEMINI_API_KEY to .env file.")
    
    # Find year column
    year_col = None
    for col in df.columns:
        if "year" in col.lower():
            year_col = col
            break
    
    if year_col is None:
        raise ValueError("Could not find year column in dataset")
    
    year_data = df[df[year_col] == selected_year]
    if year_data.empty:
        raise ValueError(f"No data found for year {selected_year}")
    
    # Compute metrics for current year
    metrics_current = {
        "year": selected_year,
        "energy_kwh": compute_metric(df, year_col, selected_year, "energy_kwh", "sum"),
        "water_liters": compute_metric(df, year_col, selected_year, "water_liters", "sum"),
        "ghg_emissions": compute_metric(df, year_col, selected_year, "ghg_emissions_kgco2e", "sum"),
        "pue": compute_metric(df, year_col, selected_year, "pue", "mean"),
        "cue": compute_metric(df, year_col, selected_year, "co2e_per_kwh", "mean"),
        "land_used": compute_metric(df, year_col, selected_year, "land_used_m2", "sum"),
    }
    
    # Compute YoY changes if previous year exists
    yoy_changes = {}
    if prev_year is not None:
        metrics_prev = {
            "energy_kwh": compute_metric(df, year_col, prev_year, "energy_kwh", "sum"),
            "water_liters": compute_metric(df, year_col, prev_year, "water_liters", "sum"),
            "ghg_emissions": compute_metric(df, year_col, prev_year, "ghg_emissions_kgco2e", "sum"),
            "pue": compute_metric(df, year_col, prev_year, "pue", "mean"),
            "cue": compute_metric(df, year_col, prev_year, "co2e_per_kwh", "mean"),
            "land_used": compute_metric(df, year_col, prev_year, "land_used_m2", "sum"),
        }
        
        for key in metrics_current:
            if key != "year" and metrics_current[key] and metrics_prev[key]:
                pct_change = ((metrics_current[key] - metrics_prev[key]) / metrics_prev[key]) * 100
                yoy_changes[key] = pct_change
    
    # Format YoY comparison
    yoy_text = ""
    if yoy_changes:
        yoy_text = f"\nYear-over-Year Changes ({prev_year} → {selected_year}):\n"
        yoy_text += f"- Energy: {yoy_changes.get('energy_kwh', 0):+.1f}%\n"
        yoy_text += f"- Water: {yoy_changes.get('water_liters', 0):+.1f}%\n"
        yoy_text += f"- GHG Emissions: {yoy_changes.get('ghg_emissions', 0):+.1f}%\n"
        yoy_text += f"- PUE: {yoy_changes.get('pue', 0):+.1f}%\n"
        yoy_text += f"- CUE: {yoy_changes.get('cue', 0):+.1f}%\n"
    
    prompt = f"""
    Analyze the following Data Centre ESG metrics for {selected_year}:
    
    Current Year ({selected_year}) Metrics:
    - Energy Consumption: {metrics_current['energy_kwh']:,.0f} kWh
    - Water Usage: {metrics_current['water_liters']:,.0f} Liters
    - GHG Emissions: {metrics_current['ghg_emissions']:,.0f} kgCO2e
    - Power Usage Effectiveness (PUE): {metrics_current['pue']:.2f}
    - Carbon Usage Effectiveness (CUE): {metrics_current['cue']:.2f} kgCO2e/kWh
    - Land Used: {metrics_current['land_used']:,.0f} m²
    {yoy_text}
    
    Provide your analysis in this EXACT structure:
    
    1. EXECUTIVE SUMMARY (exactly 5 lines):
    [Provide 5 concise lines summarizing the overall ESG position and key observations]
    
    2. KEY RISKS & CONCERNS:
    [List top 3-4 identified risks with brief explanations]
    
    3. TOP 3 AREAS FOR IMPROVEMENT:
    [For each area, provide the area name, why it's critical, and 2-3 specific actions to address it]
    
    Format clearly with headers and bullet points.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to generate analysis: {str(e)}")


def generate_recommendations(df, selected_year, prev_year=None, focus_area="overall"):
    """
    Generate specific recommendations with YoY comparisons and actionable items.
    
    Args:
        df (pd.DataFrame): The ESG data
        selected_year (int): The selected year for analysis
        prev_year (int): The previous year for comparison
        focus_area (str): Focus area - 'energy', 'water', 'emissions', 'overall'
    
    Returns:
        str: Recommendations text from Gemini
        
    Raises:
        RuntimeError: If Gemini API is not configured
        ValueError: If data is invalid or incomplete
    """
    if not is_api_available():
        raise RuntimeError("Gemini API key is not configured. Please add GEMINI_API_KEY to .env file.")
    
    year_col = None
    for col in df.columns:
        if "year" in col.lower():
            year_col = col
            break
    
    if year_col is None:
        raise ValueError("Could not find year column in dataset")
    
    # Compute metrics
    metrics_current = {
        "energy_kwh": compute_metric(df, year_col, selected_year, "energy_kwh", "sum"),
        "water_liters": compute_metric(df, year_col, selected_year, "water_liters", "sum"),
        "ghg_emissions": compute_metric(df, year_col, selected_year, "ghg_emissions_kgco2e", "sum"),
        "pue": compute_metric(df, year_col, selected_year, "pue", "mean"),
        "cue": compute_metric(df, year_col, selected_year, "co2e_per_kwh", "mean"),
    }
    
    # Compute YoY for context
    yoy_context = ""
    if prev_year is not None:
        metrics_prev = {
            "energy_kwh": compute_metric(df, year_col, prev_year, "energy_kwh", "sum"),
            "water_liters": compute_metric(df, year_col, prev_year, "water_liters", "sum"),
            "ghg_emissions": compute_metric(df, year_col, prev_year, "ghg_emissions_kgco2e", "sum"),
        }
        
        energy_change = ((metrics_current['energy_kwh'] - metrics_prev['energy_kwh']) / metrics_prev['energy_kwh'] * 100) if metrics_prev['energy_kwh'] else 0
        water_change = ((metrics_current['water_liters'] - metrics_prev['water_liters']) / metrics_prev['water_liters'] * 100) if metrics_prev['water_liters'] else 0
        ghg_change = ((metrics_current['ghg_emissions'] - metrics_prev['ghg_emissions']) / metrics_prev['ghg_emissions'] * 100) if metrics_prev['ghg_emissions'] else 0
        
        yoy_context = f"\nYear-over-Year Context: Energy {energy_change:+.1f}%, Water {water_change:+.1f}%, GHG {ghg_change:+.1f}%"
    
    focus_guidance = {
        "energy": "Prioritize energy efficiency, renewable energy sources, and cooling optimization.",
        "water": "Focus on water recycling, efficient cooling systems, and water reclamation technologies.",
        "emissions": "Concentrate on carbon offsetting, renewable energy transition, and operational efficiency.",
        "overall": "Develop integrated strategies across energy, water, and emissions reduction."
    }
    
    prompt = f"""
    Generate detailed, actionable recommendations for {selected_year} based on:
    
    Current Metrics:
    - Energy: {metrics_current['energy_kwh']:,.0f} kWh | PUE: {metrics_current['pue']:.2f}
    - Water: {metrics_current['water_liters']:,.0f} Liters
    - GHG Emissions: {metrics_current['ghg_emissions']:,.0f} kgCO2e | CUE: {metrics_current['cue']:.2f}
    {yoy_context}
    
    Focus Area: {focus_guidance.get(focus_area, focus_guidance['overall'])}
    
    Provide recommendations in this EXACT structure:
    
    1. TOP 3 IMPROVEMENT AREAS:
    For each area, list:
    - Area Name
    - Why it matters (impact/risk)
    - 3 specific, measurable actions
    - Expected outcome (% improvement or ROI)
    
    2. IMPLEMENTATION TIMELINE:
    - Quick Wins (0-3 months)
    - Short Term (3-6 months)
    - Medium Term (6-12 months)
    
    3. SUCCESS METRICS:
    [Define 3-4 KPIs to track improvement]
    
    Be concise, specific, and focused on data centre sustainability.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to generate recommendations: {str(e)}")

