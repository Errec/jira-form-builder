import os
import sys
import streamlit as st
import pandas as pd
from form_logic import parser
from form_logic.utils import clean_string, export_form


# Ensure local modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Jira Form Builder", layout="wide")
st.title("📄 Jira Form Builder")


# ---- Initialize Session State ----
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "form_name": "",
        "issue_type": "",
        "fields": []
    }


# ---- Form Files Menu ----
st.sidebar.header("Form Files")

form_mode = st.sidebar.radio(
    "Start with:",
    ["New Form", "Import Form"],
    index=0
)

if form_mode == "Import Form":
    form_files = parser.list_form_files()
    selected_file = st.sidebar.selectbox("Select YAML File", form_files)

    if selected_file:
        try:
            st.session_state.form_data = parser.load_form(selected_file) or {
                "form_name": "",
                "issue_type": "",
                "fields": []
            }
            st.sidebar.success(f"Loaded {selected_file}")
        except Exception as error:
            st.sidebar.error(f"Failed to load {selected_file}: {error}")

elif form_mode == "New Form":
    if st.sidebar.button("Reset Form"):
        st.session_state.form_data = {
            "form_name": "",
            "issue_type": "",
            "fields": []
        }
        st.rerun()


form_data = st.session_state.form_data


# ---- Form Metadata ----
st.subheader("Form Metadata")
form_data["form_name"] = st.text_input("Form Name", form_data.get("form_name", "")).strip()
form_data["issue_type"] = st.text_input("Issue Type", form_data.get("issue_type", "")).strip()


# ---- Fields Management ----
st.subheader("Fields")

with st.form("add_field_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        field_name = st.text_input("Field Name").strip()
    with col2:
        field_type = st.selectbox(
            "Field Type",
            [
                "text", "textarea", "select", "number", "date",
                "checkbox", "radio", "userpicker", "projectpicker",
            ]
        ).strip()
    with col3:
        required = st.checkbox("Required", value=False)

    options = []
    if field_type in ["select", "checkbox", "radio"]:
        options_input = st.text_input("Options (comma separated)").strip()
        options = [opt.strip() for opt in options_input.split(",") if opt.strip()]

    submitted = st.form_submit_button("Add Field")

    if submitted:
        if not field_name:
            st.warning("Field name cannot be empty.")
        elif any(f["name"].lower() == field_name.lower() for f in form_data["fields"]):
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
            st.success(f"Field '{field_name}' added.")


# ---- Fields Preview ----
if form_data["fields"]:
    st.subheader("Fields Preview")
    df = pd.DataFrame(form_data["fields"])
    st.dataframe(df, use_container_width=True)


# ---- Export ----
st.subheader("Export Form")

if not form_data.get("form_name") or not form_data.get("issue_type"):
    st.warning("Form Name and Issue Type cannot be empty for export.")

elif not form_data.get("fields"):
    st.warning("Add at least one field before exporting.")

else:
    export_data = export_form(
        form_data.get("form_name", ""),
        form_data.get("issue_type", ""),
        form_data.get("fields", [])
    )

    col1, col2 = st.columns(2)

    with col1:
        yaml_data = parser.export_to_yaml(export_data)
        st.download_button(
            label="Download YAML",
            data=yaml_data,
            file_name=f"{form_data['form_name'] or 'form'}.yaml",
            mime="text/yaml",
        )

    with col2:
        json_data = parser.export_to_json(export_data)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"{form_data['form_name'] or 'form'}.json",
            mime="application/json",
        )
