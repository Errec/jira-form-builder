import streamlit as st
import pandas as pd
from form_logic import parser
from form_logic.utils import clean_string, export_form


st.set_page_config(page_title="Jira Form Builder", layout="wide")
st.title("📄 Jira Form Builder")

# ---- Load existing forms ----
st.sidebar.header("Form Files")
form_files = parser.list_form_files()

selected_file = st.sidebar.selectbox("Load Existing Form", [""] + form_files)
form_data = {}

if selected_file:
    try:
        form_data = parser.load_form(selected_file) or {}
        st.sidebar.success(f"Loaded {selected_file}")
    except Exception as error:
        st.sidebar.error(f"Failed to load {selected_file}: {error}")

# ---- Form Metadata ----
st.subheader("Form Metadata")
form_name = st.text_input("Form Name", form_data.get("form_name", ""))
issue_type = st.text_input("Issue Type", form_data.get("issue_type", ""))
