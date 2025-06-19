"""Handles parsing, loading, and saving YAML/JSON."""

import os
import yaml
import json


FORMS_DIR = "forms"


def list_form_files():
    """List YAML form files."""
    if not os.path.exists(FORMS_DIR):
        os.makedirs(FORMS_DIR)
    return [f for f in os.listdir(FORMS_DIR) if f.endswith((".yaml", ".yml"))]


def load_form(file_name):
    """Load form YAML."""
    with open(os.path.join(FORMS_DIR, file_name), "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_uploaded_yaml(uploaded_file):
    """Load uploaded YAML."""
    return yaml.safe_load(uploaded_file)


def export_to_yaml(data):
    """Export form data to YAML string."""
    return yaml.dump(data, allow_unicode=True, sort_keys=False)


def export_to_json(data):
    """Export form data to JSON string."""
    return json.dumps(data, indent=4, ensure_ascii=False)
