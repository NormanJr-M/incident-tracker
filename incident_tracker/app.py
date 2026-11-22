from incident_tracker.cli import run_cli
from incident_tracker.database import get_connection, init_db
from incident_tracker.logging_setup import setup_logging


def main():
    """Initialize and start the Incident Tracker application."""
    logger = setup_logging()
    conn = None

    try:
        conn = get_connection("incidents.db")
        init_db(conn)
        logger.info("Incident Tracker started.")

        run_cli(conn)

    except Exception:
        logger.exception("An unexpected application error occurred.")
        raise

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()