import pytest

from incident_tracker.models import calculate_priority
from incident_tracker.validation import (
    ValidationError,
    validate_incident_input,
)


def test_valid_input_is_returned_cleaned():
    cleaned = validate_incident_input(
        title="  Outlook won't open  ",
        description="Crashes on start",
        category="software",
        impact=2,
        urgency=2,
        reporter="alice",
    )
    assert cleaned["title"] == "Outlook won't open"
    assert cleaned["category"] == "software"


def test_blank_title_is_rejected():
    with pytest.raises(ValidationError, match="title"):
        validate_incident_input(" ", "desc", "software", 2, 2, "alice")


def test_overlong_title_is_rejected():
    with pytest.raises(ValidationError, match="title"):
        validate_incident_input("x" * 201, "desc", "software", 2, 2, "alice")


def test_unknown_category_is_rejected():
    with pytest.raises(ValidationError, match="category"):
        validate_incident_input("t", "desc", "banana", 2, 2, "alice")


def test_category_is_case_insensitive():
    cleaned = validate_incident_input("t", "desc", "NETWORK", 2, 2, "alice")
    assert cleaned["category"] == "network"


@pytest.mark.parametrize("bad_value", [0, 4, 5, -1, "high", None, 2.5])
def test_impact_must_be_1_to_3(bad_value):
    with pytest.raises(ValidationError, match="impact"):
        validate_incident_input(
            "t", "desc", "software", bad_value, 2, "alice"
        )


def test_urgency_must_be_1_to_3():
    with pytest.raises(ValidationError, match="urgency"):
        validate_incident_input("t", "desc", "software", 2, 9, "alice")


def test_calculate_priority_rejects_out_of_range_values():
    with pytest.raises(ValidationError, match="impact"):
        calculate_priority(impact=5, urgency=1)