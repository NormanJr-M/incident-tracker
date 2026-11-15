from incident_tracker.models import Category, Status, calculate_priority

def test_critical_priority_when_impact_and_urgency_both_high():
    assert calculate_priority(impact=1, urgency=1) =="P1"

def test_low_priority_when_impact_and_urgency_both_low():
    assert calculate_priority(impact=3, urgency=3) =="P4"

def test_medium_priority_for_mixed_values():
    assert calculate_priority(impact=1, urgency=3) =="P3"
    assert calculate_priority(impact=3, urgency=1) =="P3"

def test_category_has_expected_values():
    assert Category.NETWORK.value =="network"

def test_status_starts_as_new():
    assert Status.NEW.value =="new"