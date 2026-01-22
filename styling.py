import streamlit as st


def apply_page_styling():
    """
    Apply grey background and custom CSS styling to the entire app.
    """
    st.markdown("""
        <style>
        /* Dark theme: black background and dark metric boxes */
        body {
            background-color: #000000;
        }
        .main {
            background-color: #000000;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
        }

        /* Top header / toolbar / any app-level bars */
        header, [data-testid="stHeader"], [data-testid="stToolbar"], .stAppHeader, .css-1v3fvcr, .css-1v3fvcr > div, .block-container > header {
            background-color: #000000 !important;
            color: #ffffff !important;
            border-color: #000000 !important;
        }

        /* Make toolbar and menu visible with dark theme */
        [data-testid="stToolbar"] {
            background-color: #000000 !important;
            display: flex !important;
            visibility: visible !important;
        }

        /* Style toolbar buttons and menu */
        [data-testid="stToolbarActionButton"],
        [data-testid="stToolbar"] button {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #333333 !important;
        }

        [data-testid="stToolbar"] button:hover {
            background-color: #1a1a1a !important;
            border: 1px solid #555555 !important;
        }

        /* Sidebar styling - refactored without aggressive * selector */
        [data-testid="stSidebar"] {
            background-color: #0b0b0b;
        }

        /* Style specific sidebar elements without affecting nested content */
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stTextInput,
        [data-testid="stSidebar"] .stNumberInput,
        [data-testid="stSidebar"] .stMultiSelect {
            background-color: transparent;
            color: #ffffff;
        }

        /* Sidebar Selectbox - single white border on outer container only */
        [data-testid="stSidebar"] .stSelectbox > div {
            border: 2.5px solid #ffffff !important;
            border-radius: 6px !important;
            padding: 0px !important;
            background-color: #000000 !important;
        }
        /* Combobox - no border, black background, white text */
        [data-testid="stSidebar"] div[role="combobox"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: none !important;
            padding: 8px 10px !important;
            font-size: 14px !important;
            outline: none !important;
            box-shadow: none !important;
        }
        /* BaseWeb select - no inner border */
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            border: none !important;
            background-color: #000000 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] input {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: none !important;
        }
        /* Dropdown arrow - white color */
        [data-testid="stSidebar"] [data-baseweb="select"] svg {
            fill: #ffffff !important;
            color: #ffffff !important;
            stroke: #ffffff !important;
        }
        /* Dropdown list - black background, white text */
        [data-testid="stSidebar"] div[role="listbox"] {
            background-color: #000000 !important;
            border: none !important;
            border-radius: 0px !important;
        }
        [data-testid="stSidebar"] div[role="option"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: none !important;
        }
        [data-testid="stSidebar"] div[role="option"]:hover {
            background-color: #1a1a1a !important;
        }
        /* Selected option text - white */
        [data-testid="stSidebar"] div[role="listbox"] [aria-selected="true"] {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
        }

        /* Sidebar Text/Number Input - visible white border */
        [data-testid="stSidebar"] .stTextInput > div > div > input,
        [data-testid="stSidebar"] .stNumberInput > div > div > input {
            border: 2px solid #ffffff !important;
            border-radius: 6px !important;
            background-color: #000000 !important;
            color: #ffffff !important;
        }

        /* Sidebar Multiselect - visible white border */
        [data-testid="stSidebar"] .stMultiSelect > div {
            border: 2px solid #ffffff !important;
            border-radius: 6px !important;
            background-color: #000000 !important;
        }

        /* Sidebar File Uploader - visible white border */
        [data-testid="stSidebar"] [data-testid="stFileUploader"],
        [data-testid="stSidebar"] div[data-testid="stDropzone"] {
            border: 2px solid #ffffff !important;
            border-radius: 8px !important;
            background-color: #000000 !important;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] button,
        [data-testid="stSidebar"] div[data-testid="stDropzone"] button {
            border: 2px solid #ffffff !important;
            background-color: #000000 !important;
            color: #ffffff !important;
            border-radius: 6px !important;
        }

        /* Sidebar Checkbox - white box with visible checkmark */
        [data-testid="stSidebar"] input[type="checkbox"],
        [data-testid="stSidebar"] div[role="checkbox"] {
            border: 2.5px solid #ffffff !important;
            border-radius: 4px !important;
            background-color: #000000 !important;
            accent-color: #ffffff !important;
            width: 20px !important;
            height: 20px !important;
            cursor: pointer !important;
        }
        [data-testid="stSidebar"] input[type="checkbox"]:checked,
        [data-testid="stSidebar"] div[role="checkbox"][aria-checked="true"] {
            background-color: #ffffff !important;
            border-color: #ffffff !important;
        }
        [data-testid="stSidebar"] input[type="checkbox"]:checked::after {
            content: '✓';
            color: #000000 !important;
        }
        [data-testid="stSidebar"] .stCheckbox label {
            color: #ffffff !important;
        }

        /* Additional Streamlit container selectors to prevent default light boxes */
        .block-container, .element-container, .stApp, .css-1d391kg, .streamlit-expander, .stContainer {
            background-color: #000000 !important;
            color: #ffffff !important;
        }

        /* Custom metric box styling with borders and dark shades */
        [data-testid="metric-container"], .stMetric, .stMetricValue, .stMetricLabel, .stMetricDelta {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #222222 !important;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.6);
        }
        /* Ensure nested metric inner elements are also dark */
        .stMetric > div, .stMetric > div > div, .stMetricValue > div, .stMetricLabel > div {
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        
        /* Subheader styling */
        [data-testid="stMarkdownContainer"] h3 {
            color: #ffffff !important;
            background-color: #000000 !important;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #9370DB;
        }
        
        /* Data table styling */
        [data-testid="dataFrameContainer"], .stDataFrame, [data-testid="stDataFrame"], table {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #222222 !important;
            border-radius: 5px;
        }
        /* Make table headers black background with white text */
        [data-testid="stDataFrame"] thead, table thead {
            background-color: #000000 !important;
        }
        [data-testid="stDataFrame"] th, table th {
            background-color: #000000 !important;
            color: #ffffff !important;
            border-color: #222222 !important;
            font-weight: bold !important;
        }
        /* Make table cells black background with white text */
        [data-testid="stDataFrame"] td, table td {
            background-color: #000000 !important;
            color: #ffffff !important;
            border-color: #222222 !important;
        }
        
        /* Button and control styling: make controls dark with visible borders */
        button, .stButton>button, .stDownloadButton>button, input, textarea, select, option, .stSelectbox, .stTextInput, .stNumberInput {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1.5px solid #555555 !important;
            border-radius: 6px !important;
            box-shadow: 0 0 0 1px #111111 !important;
        }
        button:hover, .stButton>button:hover, .stDownloadButton>button:hover {
            background-color: #111111 !important;
            border-color: #777777 !important;
        }
        /* Force all visible text to white for dark theme */
        body, p, span, h1, h2, h3, h4, h5, div, a, label, td, th, input, textarea, select, option {
            color: #ffffff !important;
        }
        /* Ensure placeholders and option backgrounds are dark */
        ::placeholder { color: #bbbbbb !important; }
        select option { background-color: #000000 !important; color: #ffffff !important; }

        /* Streamlit selectbox / dropdown overrides: combobox, listbox and options */
        [role="combobox"], [role="listbox"], [role="option"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border-color: #222222 !important;
        }
        /* Ensure dropdown option inner elements are dark and visible */
        div[role="listbox"] > div, div[role="listbox"] > div > div {
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        /* Fallback: common Streamlit selectbox containers */
        .stSelectbox, .stSelectbox > div, .stSelectbox div[role="button"], .stSelectbox .css-1v3fvcr {
            background-color: #000000 !important;
            color: #ffffff !important;
            border-color: #222222 !important;
        }
        /* Make dropdown arrow / caret and control icons visible (white) */
        .stSelectbox svg, .stSelectbox .css-1v3fvcr svg, div[role="button"] svg, div[role="listbox"] svg, [data-testid="stSidebar"] svg {
            fill: #ffffff !important;
            color: #ffffff !important;
            stroke: #ffffff !important;
            opacity: 1 !important;
        }
        /* Ensure button icons are visible */
        .stButton>button svg, button svg {
            fill: #ffffff !important;
            color: #ffffff !important;
        }
        /* Fallback: replace native select arrow with white caret using background-image */
        select {
            -webkit-appearance: none !important;
            -moz-appearance: none !important;
            appearance: none !important;
            background-image: linear-gradient(45deg, transparent 50%, #ffffff 50%), linear-gradient(135deg, #ffffff 50%, transparent 50%);
            background-position: calc(100% - 18px) calc(1em + 2px), calc(100% - 13px) calc(1em + 2px);
            background-size: 5px 5px, 5px 5px;
            background-repeat: no-repeat;
            padding-right: 28px !important;
        }

        /* File uploader / dropzone (browse files) styling */
        [data-testid="stFileUploader"], .stFileUploader, div[data-testid="stDropzone"], .css-1f3ugq6 {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #222222 !important;
            border-radius: 8px !important;
        }
        /* Make the browse button inside the uploader black with white text and a visible border */
        [data-testid="stFileUploader"] button, .stFileUploader button, div[data-testid="stDropzone"] button, input[type="file"]::-webkit-file-upload-button {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
            border-radius: 6px !important;
            padding: 8px 12px !important;
        }
        /* Ensure the drag-and-drop placeholder is dark */
        [data-testid="stFileUploader"] .css-1n8k4vy, div[data-testid="stDropzone"] .css-1n8k4vy, .stFileUploader .css-1n8k4vy {
            background-color: #000000 !important;
            color: #ffffff !important;
            opacity: 0.9 !important;
        }
        /* Fallback: target any role=button within uploader area */
        div[data-testid="stFileUploader"] [role="button"], div[data-testid="stDropzone"] [role="button"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }

        /* Force every nested element in the uploader/dropzone to be black and opaque */
        [data-testid="stFileUploader"] *, div[data-testid="stDropzone"] * {
            background-color: #000000 !important;
            color: #ffffff !important;
            background-image: none !important;
            opacity: 1 !important;
            border-color: #222222 !important;
        }

        /* Remove any pale overlay shapes inside uploader */
        [data-testid="stFileUploader"]::before, [data-testid="stFileUploader"]::after,
        div[data-testid="stDropzone"]::before, div[data-testid="stDropzone"]::after {
            background: none !important;
            content: none !important;
        }

        /* Checkboxes: make the box visible with a white border and dark background */
        /* Checkboxes: bright white box and bright white tick, stronger border */
        input[type="checkbox"], div[role="checkbox"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 3px solid #ffffff !important;
            border-radius: 5px !important;
            box-shadow: 0 0 8px rgba(255, 255, 255, 0.8) !important;
            accent-color: #ffffff !important;
            width: 20px !important;
            height: 20px !important;
        }
        /* Make checked state more visible */
        input[type="checkbox"]:checked, div[role="checkbox"][aria-checked="true"] {
            background-color: #ffffff !important;
            border-color: #ffffff !important;
            box-shadow: 0 0 12px rgba(255, 255, 255, 1) !important;
        }
        /* Ensure the inner tick mark is white and visible */
        div[role="checkbox"] svg, input[type="checkbox"] + svg, .stCheckbox svg {
            fill: #ffffff !important;
            stroke: #ffffff !important;
            color: #ffffff !important;
            opacity: 1 !important;
        }
        /* Ensure the label text remains white */
        .stCheckbox label, .stCheckbox__label, div[role="checkbox"] + label {
            color: #ffffff !important;
            border: none !important;
            box-shadow: none !important;
            padding-left: 6px !important;
        }

        /* Radio buttons: white circular outline and visible white dot when selected */
        input[type="radio"], .stRadio input[type="radio"], div[role="radio"], .stRadio {
            accent-color: #ffffff !important;
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        /* Make the radio control itself have a white border */
        input[type="radio"]::before, input[type="radio"]::after, div[role="radio"]::before, div[role="radio"]::after {
            border: 2px solid #ffffff !important;
        }
        /* Target Streamlit radio svg/icon fallback */
        div[role="radio"] svg, .stRadio svg {
            fill: #000000 !important;
            stroke: #ffffff !important;
            color: #ffffff !important;
        }
        /* Ensure radio labels are white */
        .stRadio label, .stRadio__label, div[role="radio"] + label {
            color: #ffffff !important;
        }
        /* Add a fallback white circular indicator before radio option labels (in case native glyphs hidden)
           Works for both label-based and div[role="radio"] structures. */
        [data-testid="stSidebar"] div[role="radio"]::before,
        [data-testid="stSidebar"] .stRadio label::before,
        [data-testid="stSidebar"] div[role="radiogroup"] label::before {
            content: '' !important;
            display: inline-block !important;
            width: 16px !important;
            height: 16px !important;
            margin-right: 10px !important;
            vertical-align: middle !important;
            border-radius: 50% !important;
            border: 2px solid #ffffff !important;
            background-color: transparent !important;
        }
        /* Filled dot when selected (detect aria-checked or .stRadio--selected if present) */
        [data-testid="stSidebar"] div[role="radio"][aria-checked="true"]::before,
        [data-testid="stSidebar"] .stRadio label[aria-checked="true"]::before,
        [data-testid="stSidebar"] div[role="radio"].stRadio--selected::before,
        [data-testid="stSidebar"] .stRadio .stRadio__option--selected::before {
            background-color: #ffffff !important;
        }
        /* Also support input:checked + label patterns */
        [data-testid="stSidebar"] input[type="radio"]:checked + label::before,
        [data-testid="stSidebar"] input[type="radio"]:checked + span::before {
            background-color: #ffffff !important;
        }
        /* Streamlit specific metric and dataframe selectors */
        .stMetricLabel, .stMetricValue, .stMetricDelta, [data-testid="stMarkdownContainer"] {
            color: #ffffff !important;
        }
        table, .css-1d391kg, .stDataFrame, [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {
            color: #ffffff !important;
        }
        </style>
        """, unsafe_allow_html=True)


def create_metric_box(col, label, value, delta=None, color_style="light_grey"):
    """
    Create a styled metric box with border and grey shading.
    
    Args:
        col: Streamlit column object
        label (str): Metric label
        value (str): Metric value
        delta (str): Optional delta/change indicator
        color_style (str): Box color style ('light_grey', 'medium_grey', 'dark_grey')
    """
    # Color mapping for different grey shades
    color_map = {
        "light_grey": "#f5f5f5",
        "medium_grey": "#e8e8e8",
        "dark_grey": "#d9d9d9"
    }
    
    bg_color = color_map.get(color_style, "#f5f5f5")
    
    with col:
        st.metric(label, value, delta)
