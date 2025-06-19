"""Form validation logic."""


def validate_field(field):
    """Check if field has minimum structure."""
    required_keys = ["name", "type"]
    return all(key in field for key in required_keys)
