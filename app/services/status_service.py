ALLOWED_TRANSITIONS = {
    "open": ["in_progress", "cancelled"],
    "in_progress": ["resolved"],
    "resolved": [],
    "cancelled": []
}

def is_valid_transition(current_status, new_status):
    return new_status in ALLOWED_TRANSITIONS.get(current_status, [])
