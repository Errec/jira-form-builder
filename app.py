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

if "uploaded_form_loaded" not in st.session_state:
    st.session_state.uploaded_form_loaded = False

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "field_name" not in st.session_state:
    st.session_state.field_name = ""

if "field_type" not in st.session_state:
    st.session_state.field_type = "text"

if "required" not in st.session_state:
    st.session_state.required = False

if "options_input" not in st.session_state:
    st.session_state.options_input = ""


# ---- Sidebar ----
st.sidebar.header("Form")

form_mode = st.sidebar.radio(
    "Start with:",
    ["New Form", "Import Form"],
    index=0
)

# ---- Upload Section ----
if form_mode == "Import Form":
    uploaded_file = st.sidebar.file_uploader(
        "Upload YAML", type=["yaml", "yml"], key="file_uploader"
    )

    if uploaded_file and not st.session_state.uploaded_form_loaded:
        try:
            imported_form = parser.load_uploaded_yaml(uploaded_file)
            if imported_form:
                st.session_state.form_data = imported_form
                st.session_state.uploaded_form_loaded = True
                st.session_state.uploaded_file = uploaded_file
                st.sidebar.success("Form imported successfully.")
                st.rerun()
            else:
                st.sidebar.error("Invalid YAML content.")
        except Exception as error:
            st.sidebar.error(f"Error loading file: {error}")

    if st.session_state.uploaded_form_loaded:
        st.sidebar.markdown("---")
        st.sidebar.subheader("File Management")

        remove_action = st.sidebar.radio(
            "Remove uploaded file?",
            ["No Action", "Remove File and Keep Form", "Remove File and Clear Form"],
            index=0
        )

        if remove_action == "Remove File and Keep Form":
            st.session_state.uploaded_form_loaded = False
            st.session_state.uploaded_file = None
            st.sidebar.success("File removed. Form kept.")
            st.rerun()

        if remove_action == "Remove File and Clear Form":
            st.session_state.uploaded_form_loaded = False
            st.session_state.uploaded_file = None
            st.session_state.form_data = {
                "form_name": "",
                "issue_type": "",
                "fields": []
            }
            st.sidebar.success("File removed. Form cleared.")
            st.rerun()

elif form_mode == "New Form":
    if st.sidebar.button("Reset Form"):
        st.session_state.form_data = {
            "form_name": "",
            "issue_type": "",
            "fields": []
        }
        st.session_state.uploaded_form_loaded = False
        st.session_state.uploaded_file = None
        st.rerun()


form_data = st.session_state.form_data


# ---- Form Metadata ----
st.subheader("Form Metadata")
form_data["form_name"] = st.text_input("Form Name", form_data.get("form_name", "")).strip()
form_data["issue_type"] = st.text_input("Issue Type", form_data.get("issue_type", "")).strip()


# ---- Fields Management ----
st.subheader("Fields")

col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.field_name = st.text_input("Field Name", st.session_state.field_name).strip()

with col2:
    st.session_state.field_type = st.selectbox(
        "Field Type",
        [
            "text", "textarea", "select", "number", "date",
            "checkbox", "radio", "userpicker", "projectpicker",
        ],
        index=["text", "textarea", "select", "number", "date",
               "checkbox", "radio", "userpicker", "projectpicker"].index(st.session_state.field_type)
    ).strip()

with col3:
    st.session_state.required = st.checkbox("Required", value=st.session_state.required)

# ---- Options input shows dynamically if field_type needs it ----
options = []
if st.session_state.field_type in ["select", "checkbox", "radio"]:
    st.session_state.options_input = st.text_input(
        "Options (comma separated)", st.session_state.options_input
    ).strip()
    if st.session_state.options_input:
        options = [opt.strip() for opt in st.session_state.options_input.split(",") if opt.strip()]

# ---- Add Field button ----
if st.button("Add Field"):
    if not st.session_state.field_name:
        st.warning("Field name cannot be empty.")
    elif any(f["name"].lower() == st.session_state.field_name.lower() for f in form_data["fields"]):
        st.warning(f"Field '{st.session_state.field_name}' already exists.")
    else:
        form_data["fields"].append(
            {
                "name": clean_string(st.session_state.field_name),
                "type": clean_string(st.session_state.field_type),
                "required": st.session_state.required,
                "options": options if options else None,
            }
        )
        st.success(f"Field '{st.session_state.field_name}' added.")
        st.session_state.field_name = ""
        st.session_state.field_type = "text"
        st.session_state.required = False
        st.session_state.options_input = ""


# ---- Fields Preview ----
if form_data["fields"]:
    st.subheader("Fields Preview")
    df = pd.DataFrame(form_data["fields"])

    if 'options' in df.columns:
        df['options'] = df['options'].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else ""
        )

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
