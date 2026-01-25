# Datacentre ESG Analyzer

AI-powered ESG sustainability dashboard for data centres. It helps sustainability teams, operations, and analysts load ESG data, track KPIs, visualize trends, and generate actionable, AI-assisted recommendations. The app runs locally via Streamlit with a professional dark theme and robust error handling.

## Project Overview
# Problem Solved 
ESG data for data centres is often siloed and messy. Teams need one unified view to validate inputs, compute KPIs (energy, water, emissions, land), compare year-over-year changes, and derive insights quickly.
# Intended Users
Sustainability managers, data centre operations, ESG analysts, and stakeholders preparing internal reports or disclosures.

## Key Features
# KPI Dashboard 
6 KPI cards (Energy, Water, GHG Emissions, Land Use, PUE, CUE) with safe YoY deltas.
# Interactive Charts
Yearly aggregated bar/line charts (Plotly) with dark theme styling.
# AI Insights
Gemini-powered ESG analysis and tailored recommendations by focus area (energy, water, emissions, overall).
# PDF Export 
Generate a concise report via `fpdf2` for sharing.
# Data Validation
Required column checks and safe numeric conversion with user-facing warnings.
# Graceful Degradation
AI features auto-disable when the API key is missing; user-friendly error messages.
# Dark Theme UX
Custom styling for sidebar, tables, and controls for readability.

## How to Run
1. # Clone the repository
	```bash
	git clone https://github.com/Sesodia20/Datacentre-ESG-Analyzer.git
	cd Datacentre-ESG-Analyzer
	```
2. # (Optional) Create a virtual environment**
	```bash
	python -m venv .venv
	.venv\Scripts\activate
	```
3. # Install dependencies**
	```bash
	pip install streamlit pandas numpy plotly fpdf2 python-dotenv google-generativeai
	```
	Note: `google.generativeai` is deprecated; the app still works, but consider migrating to `google.genai`.
4. # Prepare data**
	- Upload a CSV from the app, or place a default file at `data/datacentre_env.csv`.
	- Required columns: `year`, `data_centre`, `location`, `energy_kwh`, `water_liters`, `pue`, `co2e_per_kwh`, `ghg_emissions_kgco2e`, `land_used_m2`.
5. # Configure AI (optional)**
	- Create a `.env` file with your Gemini key: `GEMINI_API_KEY=your_key_here`.
	- Without a key, AI controls are disabled and the app runs normally.
6. # Start the app**
	```bash
	streamlit run app.py
	```
	Open the local URL shown (e.g., `http://localhost:8501`).

## AI Tools Summary
- **Gemini (Google):** Used to generate ESG analysis narratives and actionable recommendations.
  - Purpose: Turn KPIs + trends into concise insights and tailored action plans.
  - Availability: Checked at runtime; disabled gracefully if `GEMINI_API_KEY` is absent.
  - Deprecation Notice: Current client library `google.generativeai` shows a warning; migration to `google.genai` is recommended.

## Repository
- GitHub: https://github.com/Sesodia20/Datacentre-ESG-Analyzer.git
- View commit history and version changes directly in the repository.

## Notes
- This app includes default dataset to show an example output apart from the option to upload a csv file. 
- For newly uploaded csv file, robust error handling for incomplete uploads and invalid numeric values.
- When AI is disabled, core analytics (KPI and charts) still function fully.
- To display analysis & recommendations, "enable analysis" in the sidebar needs to be selected
