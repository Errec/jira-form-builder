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

# ---- Options input and Import ----
import_options = []

if st.session_state.field_type in ["select", "checkbox", "radio"]:
    st.session_state.options_input = st.text_input(
        "Options (comma separated)", st.session_state.options_input
    ).strip()

    with st.expander("📥 Import Options from CSV/XLSX"):
        import_file = st.file_uploader(
            "Upload CSV or Excel", type=["csv", "xlsx"], key="options_import"
        )

        if import_file:
            try:
                if import_file.name.endswith(".csv"):
                    df = pd.read_csv(import_file)
                elif import_file.name.endswith(".xlsx"):
                    df = pd.read_excel(import_file)
                else:
                    st.error("Unsupported file format.")
                    df = None

                if df is not None:
                    if df.shape[1] == 0:
                        st.error("No columns found in the file.")
                    else:
                        import_column = st.selectbox("Select column", df.columns)

                        import_options = (
                            df[import_column]
                            .dropna()
                            .astype(str)
                            .tolist()
                        )

                        if not import_options:
                            st.error("Selected column has no valid data.")
                        else:
                            st.success(f"Imported {len(import_options)} options from file.")

            except Exception as e:
                st.error(f"Failed to load file: {e}")

    manual_options = [
        opt.strip() for opt in st.session_state.options_input.split(",")
        if opt.strip()
    ] if st.session_state.options_input else []

    options = list(dict.fromkeys(manual_options + import_options))  # Unique and ordered
else:
    options = []

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

        # Reset input fields
        st.session_state.field_name = ""
        st.session_state.field_type = "text"
        st.session_state.required = False
        st.session_state.options_input = ""

# ---- Fields Preview ----
if form_data["fields"]:
    st.subheader("Fields Preview (Interactive)")

    indices_to_remove = []

    for index, field in enumerate(form_data["fields"]):
        field_label = f"{field['name']} {'*' if field.get('required') else ''}"
        field_type = field.get("type")
        field_options = field.get("options") or []

        col_preview, col_trash = st.columns([20, 1])

        with col_preview:
            if field_type in ["text", "textarea"]:
                if field_type == "textarea":
                    st.text_area(field_label, key=f"prev_textarea_{index}")
                else:
                    st.text_input(field_label, key=f"prev_text_{index}")

            elif field_type == "number":
                st.number_input(field_label, key=f"prev_number_{index}")

            elif field_type == "date":
                st.date_input(field_label, key=f"prev_date_{index}")

            elif field_type == "checkbox":
                if field_options:
                    st.multiselect(field_label, field_options, key=f"prev_checkbox_{index}")
                else:
                    st.checkbox(field_label, key=f"prev_checkboxsingle_{index}")

            elif field_type == "radio":
                st.radio(field_label, field_options or ["Option 1", "Option 2"], key=f"prev_radio_{index}")

            elif field_type == "select":
                st.selectbox(field_label, field_options or ["Option 1", "Option 2"], key=f"prev_select_{index}")

            elif field_type == "userpicker":
                st.text_input(f"{field_label} (User Picker)", key=f"prev_user_{index}")

            elif field_type == "projectpicker":
                st.text_input(f"{field_label} (Project Picker)", key=f"prev_project_{index}")

        with col_trash:
            trash_style = """
            <style>
            div[data-testid="stButton"] button {
                padding: 0.1rem 0.3rem;
                font-size: 0.7rem;
            }
            </style>
            """
            st.markdown(trash_style, unsafe_allow_html=True)
            if st.button("🗑️", key=f"delete_{index}"):
                indices_to_remove.append(index)

    if indices_to_remove:
        for i in sorted(indices_to_remove, reverse=True):
            del form_data["fields"][i]
        st.rerun()

    st.info("This is a functional preview. Inputs are not connected to any backend.")

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
