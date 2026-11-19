import pytest

from incident_tracker.database import get_connection, init_db
from incident_tracker.repository import create_incident, get_incident

@pytest.fixture
def db():
    conn = get_connection(":memory:")
    init_db(conn)

    yield conn

    conn.close()


def test_create_incident_returns_new_id(db):
    incident_id = create_incident(
        db,
        title = "Outlook won't open",
        description = "Outlook crashes when launched",
        category = "software",
        impact = 2,
        urgency = 2,
        reporter = "Alice",
    )


    assert isinstance(incident_id, int)
    assert incident_id > 0



def test_create_incident_returns_new_id(db):
    incident_id = create_incident(
         db,
         title="Outlook won't open",
         description="Outlook crashes when launched",
         category="software",
         impact=2,
         urgency=2,
         reporter="Alice",
    )

    row = db.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,),
    ).fetchone()

    assert row is not None
    assert row["title"] == "Outlook won't open"
    assert row["category"] == "software"
    assert row["priority"] == "P3"
    assert row["status"] == "new"
    assert row["reporter"] == "Alice"



def test_create_incident_saves_correct_details(db):
    incident_id = create_incident(
        db,
        title = "Outlook won't open",
        description = "Outlook crashes when launched",
        category = "software",
        impact = 2,
        urgency = 2,
        reporter = "Alice",
    )

    row = db.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,),
    ).fetchone()


    assert row is not None
    assert row["title"] == "Outlook won't open"
    assert row["category"] == "software"
    assert row["priority"] == "P3"
    assert row["status"] == "new"
    assert row["reporter"] == "Alice"


def test_get_incident_returns_saved_incident(db):
    from incident_tracker.repository import get_incident

    incident_id = create_incident(
        db,
        title = "Wi-Fi unavailable",
        description = "Cannot connect to office Wi-Fi",
        category = "network",
        impact = 1,
        urgency = 1,
        reporter = "Alice",
    )

    incident = get_incident(db, incident_id)

    assert incident is not None
    assert incident["id"] == incident_id
    assert incident["title"] == "Wi-Fi unavailable"
    assert incident["priority"] == "P1"


def test_get_incident_returns_none_when_not_found(db):
    from incident_tracker.repository import get_incident

    incident = get_incident(db, 9999)

    assert incident is None



def test_update_incident_changes_details_and_priority(db):
    from incident_tracker.repository import update_incident

    incident_id = create_incident(
        db,
        title="Slow computer",
        description="Computer takes too long to start",
        category="hardware",
        impact=3,
        urgency=3,
        reporter="Alice",
    )

    updated = update_incident(
        db,
        incident_id,
        title="Computer won't start",
        description="Computer fails to boot",
        category="hardware",
        impact=1,
        urgency=1,
    )


    incident = get_incident(db, incident_id)

    assert updated is True
    assert incident["title"] == "Computer won't start"
    assert incident["description"] == "Computer fails to boot"
    assert incident["priority"] == "P1"



def test_update_noneexistent_incident_returns_false(db):
    from incident_tracker.repository import update_incident

    updated = update_incident(
        db,
        9999,
        title="Updated incident",
        description="Testing a nonexistent incident",
        category="software",
        impact=2,
        urgency=2,
    )

    assert updated is False



def test_update_incident_status(db):
    from incident_tracker.repository import update_incident_status

    incident_id = create_incident(
        db,
        title="Wi-Fi unavailable",
        description="Cannot connect to office Wi-Fi",
        category="network",
        impact=2,
        urgency=2,
        reporter="Alice",
    )

    updated = update_incident_status(
        db,
        incident_id,
        "in_progress",
    )

    incident = get_incident(db, incident_id)

    assert updated is True
    assert incident["status"] == "in_progress"


def test_update_incident_status_rejects_invalid_status(db):
    from incident_tracker.errors import ValidationError
    from incident_tracker.repository import update_incident_status

    with pytest.raises(ValidationError):
        update_incident_status(
            db,
            9999,
            "pending",
        )

def test_resolve_incident_saves_resolution_details(db):
    from incident_tracker.repository import resolve_incident

    incident_id = create_incident(
        db,
        title="Wi-Fi unavailable",
        description="Cannot connect to office Wi-Fi",
        category="network",
        impact=2,
        urgency=2,
        reporter="Alice",
    )

    resolved = resolve_incident(
        db,
        incident_id,
        resolution_notes="Restarted the network router",
    )


    incident = get_incident(db, incident_id)


    assert resolved is True
    assert incident["status"] == "resolved"
    assert incident["resolved_at"] is not None
    assert incident["resolution_notes"] == "Restarted the network router"


def test_resolve_incident_rejects_empty_resolution_notes(db):
    import pytest
    from incident_tracker.errors import ValidationError
    from incident_tracker.repository import resolve_incident

    incident_id = create_incident(
        db,
        title="Wi-Fi unavailable",
        description="Cannot connect to office Wi-Fi",
        category="network",
        impact=2,
        urgency=2,
        reporter="Alice",
    )


    with pytest.raises(ValidationError):
        resolve_incident(
            db,
            incident_id,
            resolution_notes="  ",
        )


def test_resolve_nonexistent_incident_returns_false(db):
    from incident_tracker.repository import resolve_incident

    resolved = resolve_incident(
        db,
        9999,
        resolution_notes="Restarted the network router",
    )


    assert resolved is False



def test_list_incidents_returns_newest_first(db):
    from incident_tracker.repository import list_incidents

    first_id = create_incident(
        db,
        title="Printer offline",
        description="The printer is not responding",
        category="hardware",
        impact=2,
        urgency=2,
        reporter="Alice",
    )

    second_id = create_incident(
        db,
        title="Wi-Fi unavailable",
        description="Cannot connect to office Wi-Fi",
        category="network",
        impact=2,
        urgency=1,
        reporter="Bob",
    )

    incidents = list_incidents(db)

    assert len(incidents) == 2
    assert incidents[0]["id"] == second_id
    assert incidents[1]["id"] == first_id


def test_list_incidents_returns_empty_list(db):
    from incident_tracker.repository import list_incidents

    incidents = list_incidents(db)

    assert incidents == []