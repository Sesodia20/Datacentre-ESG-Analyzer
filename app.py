import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Centre ESG Analyser", layout="wide")

st.title("Data Centre ESG Analyser")
st.write("Load and analyze ESG data for data centres")

# Sidebar for file selection
with st.sidebar:
    st.header("File Selection")
    file_source = st.radio("Choose data source:", ("Upload CSV", "Use Default CSV"))

# Load and display data
if file_source == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.subheader("Data Preview")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Please upload a CSV file to begin analysis.")

else:  # Use Default CSV
    try:
        df = pd.read_csv("data/default_data.csv")
        st.success("Default data loaded successfully!")
        st.subheader("Data Preview")
        st.dataframe(df, use_container_width=True)
    except FileNotFoundError:
        st.warning("Default CSV file not found at 'data/default_data.csv'. Please upload a file instead.")
    except Exception as e:
        st.error(f"Error reading default file: {e}")
