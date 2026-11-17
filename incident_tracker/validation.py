from incident_tracker.errors import ValidationError, validate_scale
from incident_tracker.models import Category

MAX_TITLE_LENGTH = 200

def _require_text(value, field, max_length=None):
    if not isinstance(value,str) or not value.strip():
        raise ValidationError(f"{field} must not be empty")

    value = value.strip()


    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            f"{field} must be at most {max_length} characters"
        )

    return value


def validate_category(value):
    if not isinstance(value, str):
        raise ValidationError("category must be text")

    try: 
        return Category(value.strip().lower()).value
    except  ValueError:
        allowed = ", ".join(category.value for category in Category) 
        raise ValidationError(f"category must be one of: {allowed}")



def validate_incident_input(
        title, description, category, impact, urgency, reporter
):
    return {
        "title": _require_text(title, "title", MAX_TITLE_LENGTH),
        "description": _require_text(description, "description"),
        "category": validate_category(category),
        "impact": validate_scale(impact, "impact"),
        "urgency": validate_scale(urgency, "urgency"),
        "reporter": _require_text(reporter, "reporter"),
    }