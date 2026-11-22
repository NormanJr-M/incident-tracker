from incident_tracker.errors import ValidationError
from incident_tracker.repository import create_incident, get_incident, list_incidents, update_incident, resolve_incident


def display_menu():
    """Display the main Incident Tracker menu."""
    print("\n" + "=" * 32)
    print("       IT INCIDENT TRACKER")
    print("=" * 32)
    print("1. Create Incident")
    print("2. View Incident")
    print("3. List Incidents")
    print("4. Update Incident")
    print("5. Resolve Incident")
    print("6. Exit")
    print("=" * 32)



def get_menu_choice():
    """Ask the user to choose a menu option."""
    return input("Choose an option: ").strip()



def create_incident_prompt(conn):
    """Collect incident details and save a new incident."""
    print("\n--- Create Incident ---")

    title = input("Title: ")
    description = input("Description: ")
    category = input("Category (hardware/software/network/access/other): ")

    try:
        impact = int(input("Impact (1 = high, 3 = low): "))
        urgency = int(input("Urgency (1 = high, 3 = low): "))
    except ValueError:
        print("Impact and urgency must be whole numbers from 1 to 3.")
        return

    reporter = input("Reported by: ")

    try:
        incident_id = create_incident(
            conn,
            title=title,
            description=description,
            category=category,
            impact=impact,
            urgency=urgency,
            reporter=reporter,
        )
    except ValidationError as exc:
        print(f"Could not create incident: {exc}")
        return

    incident = get_incident(conn, incident_id)

    print("\nIncident created successfully!")
    print(f"Incident ID: {incident_id}")
    print(f"Priority: {incident['priority']}")
    print(f"Status: {incident['status']}")



def view_incident_prompt(conn):
    """Ask for an incident ID and display its details."""
    print("\n--- View Incident ---")

    try:
        incident_id = int(input("Enter incident ID: "))
    except ValueError:
        print("Incident ID must be a whole number.")
        return

    incident = get_incident(conn, incident_id)

    if incident is None:
        print(f"No incident found with ID {incident_id}.")
        return

    print("\n--- Incident Details ---")
    print(f"Incident ID: {incident['id']}")
    print(f"Title: {incident['title']}")
    print(f"Description: {incident['description']}")
    print(f"Category: {incident['category']}")
    print(f"Impact: {incident['impact']}")
    print(f"Urgency: {incident['urgency']}")
    print(f"Priority: {incident['priority']}")
    print(f"Status: {incident['status']}")
    print(f"Reported by: {incident['reporter']}")



def list_incidents_prompt(conn):
    """Display all incidents stored in the database."""
    print("\n--- List Incidents ---")

    incidents = list_incidents(conn)

    if not incidents:
        print("No incidents found.")
        return

    for incident in incidents:
        print("\n------------------------------")
        print(f"Incident ID: {incident['id']}")
        print(f"Title: {incident['title']}")
        print(f"Category: {incident['category']}")
        print(f"Priority: {incident['priority']}")
        print(f"Status: {incident['status']}")
        print(f"Reported by: {incident['reporter']}")

    print("\n------------------------------")
    print(f"Total incidents: {len(incidents)}")



def update_incident_prompt(conn):
    """Update the details of an existing incident."""
    print("\n--- Update Incident ---")

    try:
        incident_id = int(input("Enter incident ID: "))
    except ValueError:
        print("Incident ID must be a whole number.")
        return

    incident = get_incident(conn, incident_id)

    if incident is None:
        print(f"No incident found with ID {incident_id}.")
        return

    print("Press Enter to keep the current value.")

    title = input(f"Title [{incident['title']}]: ").strip()
    description = input(f"Description [{incident['description']}]: ").strip()
    category = input(f"Category [{incident['category']}]: ").strip()

    try:
        impact_input = input(f"Impact (1 = high, 3 = low) [{incident['impact']}]: ").strip()
        urgency_input = input(f"Urgency (1 = high, 3 = low) [{incident['urgency']}]: ").strip()

        impact = int(impact_input) if impact_input else incident["impact"]
        urgency = int(urgency_input) if urgency_input else incident["urgency"]

    except ValueError:
        print("Impact and urgency must be whole numbers from 1 to 3.")
        return


    try:
        updated = update_incident(
            conn,
            incident_id,
            title=title or incident["title"],
            description=description or incident["description"],
            category=category or incident["category"],
            impact=impact,
            urgency=urgency,
        )
    except ValidationError as exc:
        print(f"Could not update incident: {exc}")
        return

    if not updated:
        print(f"No incident found with ID {incident_id}.")
        return

    incident = get_incident(conn, incident_id)

    print("\nIncident updated successfully!")
    print(f"Incident ID: {incident_id}")
    print(f"Title: {incident['title']}")
    print(f"Priority: {incident['priority']}")
    print(f"Status: {incident['status']}")


def resolve_incident_prompt(conn):
    """Resolve an incident and save resolution notes."""
    print("\n--- Resolve Incident ---")

    try:
        incident_id = int(input("Enter incident ID: "))
    except ValueError:
        print("Incident ID must be a whole number.")
        return

    incident = get_incident(conn, incident_id)

    if incident is None:
        print(f"No incident found with ID {incident_id}.")
        return

    if incident["status"] == "resolved":
        print(f"Incident {incident_id} is already resolved.")
        return

    print(f"Incident: {incident['title']}")
    resolution_notes = input("Resolution notes: ").strip()

    try:
        resolved = resolve_incident(
            conn,
            incident_id,
            resolution_notes=resolution_notes,
        )
    except ValidationError as exc:
        print(f"Could not resolve incident: {exc}")
        return

    if not resolved:
        print(f"No incident found with ID {incident_id}.")
        return

    print(f"\nIncident {incident_id} resolved successfully!")
    print(f"Resolution notes: {resolution_notes}")



def handle_menu_choice(choice, conn):
    """Handle the user's sleected menu option."""
    if choice == "1":
        create_incident_prompt(conn)
    elif choice == "2":
        view_incident_prompt(conn)
    elif choice == "3":
        list_incidents_prompt(conn)
    elif choice == "4":
        update_incident_prompt(conn)
    elif choice == "5":
        resolve_incident_prompt(conn)
    elif choice == "6":
        print("Goodbye!")
    else:
        print("Invalid option. Please choose a number from 1 to 6.")


def run_cli(conn):
    """Run the main menu until the user chooses to exit."""
    while True:
        display_menu()
        choice = get_menu_choice()
        handle_menu_choice(choice, conn)

        if choice == "6":
            break