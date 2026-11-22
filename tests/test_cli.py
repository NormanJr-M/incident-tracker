import pytest
from incident_tracker.database import get_connection, init_db
from incident_tracker.cli import display_menu, get_menu_choice, handle_menu_choice, run_cli, create_incident_prompt, update_incident_prompt
from incident_tracker.repository import get_incident



@pytest.fixture
def db():
    conn = get_connection(":memory:")
    init_db(conn)
    yield conn
    conn.close()



def test_display_menu_show_all_options(capsys):
    display_menu()

    output = capsys.readouterr().out

    assert "IT INCIDENT TRACKER" in output
    assert "1. Create Incident" in output
    assert "2. View Incident" in output
    assert "3. List Incidents" in output
    assert "4. Update Incident" in output
    assert "5. Resolve Incident" in output
    assert "6. Exit" in output



def test_get_menu_choice_returns_user_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")

    choice = get_menu_choice()

    assert choice == "3"



def test_get_menu_choice_removes_surrounding_spaces(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "  2  ")

    choice = get_menu_choice()

    assert choice == "2"



def test_handle_menu_choice_displays_selected_action(capsys, db):
    handle_menu_choice("3", db)

    output = capsys.readouterr().out

    assert "--- List Incidents ---" in output
    assert "No incidents found." in output



def test_handle_menu_choice_rejects_invalid_option(capsys, db):
    handle_menu_choice("9", db)

    output = capsys.readouterr().out

    assert "Invalid option" in output



def test_run_cli_exits_when_user_selects_six(monkeypatch, capsys, db):
    monkeypatch.setattr("builtins.input", lambda _: "6")

    run_cli(db)

    output = capsys.readouterr().out

    assert "IT INCIDENT TRACKER" in output
    assert "Goodbye!" in output



def test_create_incident_prompt_saves_incident(db, monkeypatch, capsys):
    inputs = iter([
        "Laptop won't start",
        "The user's laptop does not power on.",
        "hardware",
        "1",
        "1",
        "John",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    create_incident_prompt(db)

    output = capsys.readouterr().out

    assert "Incident created successfully!" in output
    assert "Incident ID:" in output
    assert "Priority: P1" in output
    assert "Status: new" in output

    incident = get_incident(db, 1)

    assert incident is not None
    assert incident["title"] == "Laptop won't start"
    assert incident["category"] == "hardware"
    assert incident["reporter"] == "John"



def test_view_incident_prompt_displays_incident(db, monkeypatch, capsys):
    incident_id = 1

    from incident_tracker.repository import create_incident

    create_incident(
        db,
        title="Laptop won't start",
        description="The laptop does not power on.",
        category="hardware",
        impact=1,
        urgency=1,
        reporter="John",
    )

    monkeypatch.setattr("builtins.input", lambda _: str(incident_id))

    from incident_tracker.cli import view_incident_prompt
    view_incident_prompt(db)

    output = capsys.readouterr().out

    assert "Laptop won't start" in output
    assert "The laptop does not power on." in output
    assert "Priority: P1" in output
    assert "Status: new" in output
    assert "Reported by: John" in output


def test_list_incidents_prompt_displays_incidents(db, capsys):
    from incident_tracker.repository import create_incident
    from incident_tracker.cli import list_incidents_prompt

    create_incident(
        db,
        title="Laptop won't start",
        description="The laptop does not power on.",
        category="hardware",
        impact=1,
        urgency=1,
        reporter="John",
    )

    create_incident(
        db,
        title="Website unavailable",
        description="The website cannot be reached.",
        category="network",
        impact=2,
        urgency=2,
        reporter="Mary",
    )

    list_incidents_prompt(db)

    output = capsys.readouterr().out

    assert "Laptop won't start" in output
    assert "Website unavailable" in output
    assert "Total incidents: 2" in output



def test_update_incident_prompt_updates_incident(db, monkeypatch, capsys):
    from incident_tracker.repository import create_incident, get_incident
    from incident_tracker.cli import update_incident_prompt

    incident_id = create_incident(
        db,
        title="Laptop won't start",
        description="The laptop does not power on.",
        category="hardware",
        impact=1,
        urgency=1,
        reporter="John",
    )

    inputs = iter([
        str(incident_id),
        "Laptop starts intermittently",
        "",
        "",
        "",
        "",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    update_incident_prompt(db)

    output = capsys.readouterr().out
    incident = get_incident(db, incident_id)

    assert "Incident updated successfully!" in output
    assert incident["title"] == "Laptop starts intermittently"
    assert incident["description"] == "The laptop does not power on."
    assert incident["category"] == "hardware"
    assert incident["priority"] == "P1"



def test_update_incident_prompt_handles_missing_incident(db, monkeypatch, capsys):
    from incident_tracker.cli import update_incident_prompt

    monkeypatch.setattr("builtins.input", lambda _: "999")

    update_incident_prompt(db)

    output = capsys.readouterr().out

    assert "No incident found with ID 999." in output



def test_resolve_incident_prompt_resolves_incident(db, monkeypatch, capsys):
    from incident_tracker.repository import create_incident, get_incident
    from incident_tracker.cli import resolve_incident_prompt

    incident_id = create_incident(
        db,
        title="Website unavailable",
        description="Customers cannot access the website.",
        category="network",
        impact=1,
        urgency=1,
        reporter="Mary",
    )

    inputs = iter([str(incident_id), "Website service restored"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    resolve_incident_prompt(db)

    output = capsys.readouterr().out
    incident = get_incident(db, incident_id)

    assert "resolved successfully!" in output
    assert incident["status"] == "resolved"
    assert incident["resolution_notes"] == "Website service restored"
    assert incident["resolved_at"] is not None



def test_resolve_incident_prompt_handles_missing_incident(db, monkeypatch, capsys):
    from incident_tracker.cli import resolve_incident_prompt

    monkeypatch.setattr("builtins.input", lambda _: "999")

    resolve_incident_prompt(db)

    output = capsys.readouterr().out

    assert "No incident found with ID 999." in output



def test_resolve_incident_prompt_rejects_empty_notes(db, monkeypatch, capsys):
    from incident_tracker.repository import create_incident, get_incident
    from incident_tracker.cli import resolve_incident_prompt

    incident_id = create_incident(
        db,
        title="Printer offline",
        description="The office printer is unavailable.",
        category="hardware",
        impact=2,
        urgency=2,
        reporter="John",
    )

    inputs = iter([str(incident_id), "   "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    resolve_incident_prompt(db)

    output = capsys.readouterr().out
    incident = get_incident(db, incident_id)

    assert "resolution_notes must not be empty" in output
    assert incident["status"] == "new"
    assert incident["resolved_at"] is None