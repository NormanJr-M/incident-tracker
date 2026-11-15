from enum import Enum

class Category(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    ACCESS = "access"
    OTHER = "other"

class Status(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    RESOLVED = "resolved"
    CLOSED = "closed"

#Rows are impact (1-3), columns are urgency (1-3).
_PRIORITY_MATRIX = {
    1: {1: "P1", 2: "P2", 3: "P3"},
    2: {1: "P2", 2: "P3", 3: "P4"},
    3: {1: "P3", 2: "P4", 3: "P4"}
}


def calculate_priority(impact, urgency):
    return _PRIORITY_MATRIX[impact][urgency]