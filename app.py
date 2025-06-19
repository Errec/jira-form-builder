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

# ---- Fields Management ----
st.subheader("Fields")

if "fields" not in form_data or not isinstance(form_data.get("fields"), list):
    form_data["fields"] = []

with st.form("add_field_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        field_name = st.text_input("Field Name")
    with col2:
        field_type = st.selectbox(
            "Field Type",
            [
                "text", "textarea", "select", "number", "date",
                "checkbox", "radio", "userpicker", "projectpicker",
            ],
        )
    with col3:
        required = st.checkbox("Required", value=False)

    options = []
    if field_type in ["select", "checkbox", "radio"]:
        options = [
            opt.strip()
            for opt in st.text_input("Options (comma separated)").split(",")
            if opt.strip()
        ]

    submitted = st.form_submit_button("Add Field")
