from datetime import datetime, timezone

from incident_tracker.models import calculate_priority
from incident_tracker.validation import validate_incident_input

def create_incident(
        conn,
        *,
        title,
        description,
        category,
        impact,
        urgency,
        reporter,
):
    """Validate and save a new incident, returning its database ID."""

    incident = validate_incident_input(
        title=title,
        description = description,
        category = category,
        impact = impact,
        urgency = urgency,
        reporter = reporter,
    )

    priority = calculate_priority(
        incident["impact"],
        incident["urgency"],
    )

    now =  datetime.now(timezone.utc).isoformat(timespec="seconds")


    cursor = conn.execute(
        """
            INSERT INTO incidents (
                title,
                description,
                category,
                impact,
                urgency,
                priority,
                status,
                reporter,
                assignee,
                created_at,
                updated_at,
                resolved_at,
                resolution_notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            incident["title"],
            incident["description"],
            incident["category"],
            incident["impact"],
            incident["urgency"],
            priority,
            "new",
            incident["reporter"],
            None,
            now,
            now,
            None,
            None,
        ),
    )

    conn.commit()

    return cursor.lastrowid


def get_incident(conn, incident_id):
    """Return an incident by ID, or None if it doesn't exist."""

    row = conn.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,),
    ).fetchone()


    return row


def update_incident(
    conn,
    incident_id,
    *,
    title,
    description,
    category,
    impact,
    urgency,
):
    """Update an incident's details and return whether it exists."""

    from incident_tracker.validation import validate_incident_input

    incident = validate_incident_input(
        title=title,
        description=description,
        category=category,
        impact=impact,
        urgency=urgency,
        reporter="Update",
    )

    priority = calculate_priority(
        incident["impact"],
        incident["urgency"],
    )


    now = datetime.now(timezone.utc).isoformat(timespec="seconds")


    cursor = conn.execute(
        """
            UPDATE incidents
            SET title = ?,
                description = ?,
                category = ?,
                impact = ?,
                urgency = ?,
                priority = ?,
                updated_at = ?
            WHERE id = ?
        """,
        (
            incident["title"],
            incident["description"],
            incident["category"],
            incident["impact"],
            incident["urgency"],
            priority,
            now,
            incident_id,
        ),
    )


    conn.commit()

    return cursor.rowcount > 0


from incident_tracker.models import Status
from incident_tracker.errors import ValidationError



def update_incident_status(conn, incident_id, new_status):
    """Update an incident's status and return whether it exists."""

    if not isinstance(new_status, str):
        raise ValidationError("status must be text")

    try:
        status = Status(new_status.strip().lower()).value
    except ValueError:
        allowed = ",".join(s.value for s in Status)
        raise ValidationError(f"status must be one of: {allowed}")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    cursor = conn.execute(
        """
            UPDATE incidents
            SET status = ?, updated_at = ?
            WHERE id = ?
        """,
        (status, now, incident_id),
    )

    conn.commit()

    return cursor.rowcount > 0



def resolve_incident(conn, incident_id, *, resolution_notes):
    """Mark an incident as resolved and save resolution details."""

    if not isinstance(resolution_notes, str) or not resolution_notes.strip():
        raise ValidationError("resolution_notes must not be empty")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    cursor = conn.execute(
        """
            UPDATE incidents
            SET status = ?, resolved_at = ?, resolution_notes = ?, updated_at = ?
            WHERE id = ?
        """,
        ("resolved", now, resolution_notes.strip(), now, incident_id),
    )

    conn.commit()
    return cursor.rowcount > 0



def list_incidents(conn):
    """Return all incidents, newest first."""

    cursor = conn.execute(
        """
            SELECT *
            FROM incidents
            ORDER BY created_at DESC, id DESC
        """
    )

    return cursor.fetchall()