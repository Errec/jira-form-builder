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

    if submitted:
        if not field_name.strip():
            st.warning("Field name cannot be empty.")
        elif any(f["name"].lower() == field_name.strip().lower() for f in form_data["fields"]):
            st.warning(f"Field '{field_name}' already exists.")
        else:
            form_data["fields"].append(
                {
                    "name": clean_string(field_name),
                    "type": clean_string(field_type),
                    "required": required,
                    "options": options if options else None,
                }
            )
# ---- Fields Preview ----
if form_data["fields"]:
    st.subheader("Fields Preview")
    df = pd.DataFrame(form_data["fields"])
    st.dataframe(df, use_container_width=True)

# ---- Export ----
st.subheader("Export Form")

export_data = export_form(form_name, issue_type, form_data["fields"])

col1, col2 = st.columns(2)

with col1:
    if st.button("Download YAML"):
        yaml_data = parser.export_to_yaml(export_data)
        st.download_button(
            label="Download YAML",
            data=yaml_data,
            file_name=f"{form_name or 'form'}.yaml",
            mime="text/yaml",
        )

with col2:
    if st.button("Download JSON"):
        json_data = parser.export_to_json(export_data)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"{form_name or 'form'}.json",
            mime="application/json",
        )
