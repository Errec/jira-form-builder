"""Utility functions for form handling."""


def clean_string(value):
    """Trim and sanitize string input."""
    return value.strip() if isinstance(value, str) else value


def export_form(form_name, issue_type, fields):
    """Prepare data structure for export."""
    return {
        "form_name": clean_string(form_name),
        "issue_type": clean_string(issue_type),
        "fields": fields,
    }
