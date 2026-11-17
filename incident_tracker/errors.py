class ValidationError(ValueError):
    """Raised when user input does not meet the rules."""


def validate_scale(value, field):
    """Require a whole number from 1 to 3."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(
            f"{field} must be a whole number from 1 to 3"
        )

    if value not in (1, 2 ,3):
        raise ValidationError(f"{field} must be between 1 and 3")

    return value