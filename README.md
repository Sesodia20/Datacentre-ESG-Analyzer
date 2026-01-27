# Datacentre ESG Analyzer

AI-powered ESG sustainability dashboard for data centres. It helps sustainability teams, operations, and analysts load ESG data, validate inputs, track KPIs, visualise trends, and generate actionable, AI-assisted recommendations. The app runs locally via Streamlit with a professional dark theme and robust error handling.

## Project Overview
## Problem Solved
ESG data for data centres is often siloed, inconsistent, and messy. Teams need one unified view to validate inputs, compute key sustainability KPIs (energy, water, emissions, land), compare year-over-year changes, and derive insights quickly for internal reporting and decision-making.

## Intended Users
- Sustainability managers  
- Data centre operations teams  
- ESG analysts  
- Stakeholders preparing internal reports or disclosures

## Key Functionalities

- **KPI Dashboard:** 6 KPI cards (Energy, Water, GHG Emissions, Land Use, PUE, CUE) with safe YoY deltas.  
- **Interactive Charts:** Yearly aggregated bar/line charts (Plotly) with dark-theme styling.  
- **AI Insights:** Gemini-powered ESG analysis and tailored recommendations by focus area (energy, water, emissions, overall).  
- **PDF Export:** Generates a concise report using `fpdf2` for sharing.  
- **Data Validation:** Required column checks and safe numeric conversion with user-facing warnings.  
- **Graceful Degradation:** AI features auto-disable when `GEMINI_API_KEY` is missing; core analytics still work.

## Data Format
Upload a CSV in the app (or select the default file at `data/datacentre_env.csv`).

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

- **Claude Haiku (Anthropic):** Used during development as an AI coding assistant/agent.
  - Purpose: Support prompt design, code generation/refactoring, debugging suggestions, and UI/UX improvements during implementation.
  - Role: Assisted development workflow only; final integration and decisions were user-reviewed and implemented in the codebase.


## Repository
- GitHub: https://github.com/Sesodia20/Datacentre-ESG-Analyzer.git
- View commit history and version changes directly in the repository.

## Notes
- This app includes default dataset to show an example output apart from the option to upload a csv file. 
- For newly uploaded csv file, robust error handling for incomplete uploads and invalid numeric values.
- When AI is disabled, core analytics (KPI and charts) still function fully.
- To display analysis & recommendations, "enable analysis" in the sidebar needs to be selected
