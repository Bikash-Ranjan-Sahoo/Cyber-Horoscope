"""
CyberHoroscope — Input Validator
==================================
Validates the incoming quiz answers before they reach the scoring engine.
Returns None on success, or a descriptive error string on failure.
No external imports required.
"""

# ─────────────────────────────────────────────
# Allowed answer values per question
# Must match 02-functional-spec.yaml exactly.
# ─────────────────────────────────────────────
VALID_ANSWERS: dict[str, list[str]] = {
    "q1": ["always", "sometimes", "never"],         # password reuse
    "q2": ["none", "some", "all"],                   # 2FA usage
    "q3": ["never", "sometimes", "always"],          # update frequency
    "q4": ["regularly", "once_or_twice", "never"],   # cracked software
    "q5": ["always", "sometimes", "never"],          # shortened links
}

# Developer mode valid answers — added v2.0.0
DEV_VALID_ANSWERS: dict[str, list[str]] = {
    "q1": ["always", "sometimes", "never"],   # hardcoded secrets
    "q2": ["never", "sometimes", "always"],   # CVE handling
    "q3": ["always", "sometimes", "never"],   # prod as test env
    "q4": ["none", "sometimes", "always"],    # code review / branch protection
    "q5": ["always", "sometimes", "never"],   # error exposure
}


def validate_answers(answers: dict, mode: str = "user") -> str | None:
    """
    Validate the answers dict submitted by the user.

    Parameters
    ----------
    answers : dict
        Expected shape: {"q1": "always", "q2": "none", ...}

    Returns
    -------
    str | None
        None if all answers are valid.
        A human-readable error string describing the first problem found.
    """
    if not isinstance(answers, dict):
        return "answers must be an object"

    valid_map = DEV_VALID_ANSWERS if mode == "dev" else VALID_ANSWERS

    for question_id, allowed_values in valid_map.items():
        if question_id not in answers:
            return f"Missing answer for {question_id}"

        submitted_value = answers[question_id]
        if submitted_value not in allowed_values:
            return (
                f"Invalid value '{submitted_value}' for {question_id}. "
                f"Allowed: {', '.join(allowed_values)}"
            )

    return None  # all valid
