"""
CyberHoroscope — Horoscope Engine
====================================
Core scoring and horoscope generation logic.

Entry point: generate(answers) → dict

All computation is pure in-memory Python — no I/O, no external calls.
"""

import datetime
import random

import content

# ─────────────────────────────────────────────
# Risk score lookup table
# Must match 02-functional-spec.yaml risk_score values exactly.
# ─────────────────────────────────────────────
RISK_SCORES: dict[str, dict[str, int]] = {
    "q1": {"always": 30, "sometimes": 15, "never": 0},   # password reuse
    "q2": {"none": 25, "some": 10, "all": 0},             # 2FA
    "q3": {"never": 20, "sometimes": 10, "always": 0},    # updates
    "q4": {"regularly": 25, "once_or_twice": 10, "never": 0},  # cracked software
    "q5": {"always": 20, "sometimes": 10, "never": 0},    # shortened links
}

# Maximum possible raw score (30+25+20+25+20)
RAW_MAX: int = 120

# ─────────────────────────────────────────────
# Cyber sign definitions (ordered low → high risk)
# ─────────────────────────────────────────────
CYBER_SIGNS: list[dict] = [
    {
        "threshold": 20,
        "sign": "Firewall Phoenix",
        "emoji": "🦅",
        "description": "Rising from the ashes of every breach attempt, untouched.",
    },
    {
        "threshold": 40,
        "sign": "Encryption Wizard",
        "emoji": "🧙",
        "description": "Your digital spells keep most threats at bay.",
    },
    {
        "threshold": 60,
        "sign": "Patch Warrior",
        "emoji": "⚔️",
        "description": "You fight the good fight, but a few chinks remain in your armour.",
    },
    {
        "threshold": 80,
        "sign": "Phishing Magnet",
        "emoji": "🧲",
        "description": "Scammers have placed a standing order with your email address.",
    },
    {
        "threshold": 100,
        "sign": "Data Breach Influencer",
        "emoji": "📢",
        "description": "You are basically unpaid marketing for the dark web.",
    },
]


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────
def generate(answers: dict) -> dict:
    """
    Score quiz answers and return a fully populated horoscope response dict.

    Parameters
    ----------
    answers : dict
        Validated answer dict, e.g. {"q1": "always", "q2": "none", ...}

    Returns
    -------
    dict
        Horoscope response matching the schema in 02-functional-spec.yaml
        and 04-api-spec.yaml.
    """
    # ── Step 1: Calculate final score ────────────────────────────────────────
    raw_score: int = sum(RISK_SCORES[q][answers[q]] for q in RISK_SCORES)
    final_score: int = round((raw_score / RAW_MAX) * 100)

    # ── Step 2: Determine cyber sign ─────────────────────────────────────────
    sign_data: dict = CYBER_SIGNS[-1]  # fallback to highest tier
    for entry in CYBER_SIGNS:
        if final_score <= entry["threshold"]:
            sign_data = entry
            break

    # ── Step 3: Calculate dimension scores ───────────────────────────────────
    # Phishing risk (q2 + q5), max raw = 25 + 20 = 45
    phishing_raw: int = RISK_SCORES["q2"][answers["q2"]] + RISK_SCORES["q5"][answers["q5"]]
    phishing_risk_pct: int = round((phishing_raw / 45) * 100)

    # Password aura (q1 only), max raw = 30
    password_raw: int = RISK_SCORES["q1"][answers["q1"]]
    password_aura: str = _map_to_label(
        password_raw,
        {0: "Legendary", 15: "Moderate", 30: "Catastrophic"},
    )
    # Fill in gaps (score 1–14 = Strong, 16–29 = Weak)
    if password_raw > 0 and password_raw < 15:
        password_aura = "Strong"
    elif password_raw > 15 and password_raw < 30:
        password_aura = "Weak"

    # Wi-Fi karma (q3 + q4), max raw = 20 + 25 = 45
    wifi_raw: int = RISK_SCORES["q3"][answers["q3"]] + RISK_SCORES["q4"][answers["q4"]]
    wifi_karma: str = _map_to_label(
        wifi_raw,
        {0: "Pristine", 10: "Cautious", 20: "Reckless", 35: "Suicidal"},
    )

    # Scam magnet (q4 + q5), max raw = 25 + 20 = 45
    scam_raw: int = RISK_SCORES["q4"][answers["q4"]] + RISK_SCORES["q5"][answers["q5"]]
    scam_magnet: str = _map_to_label(
        scam_raw,
        {0: "Repellent", 10: "Neutral", 20: "Attractive", 30: "Irresistible"},
    )

    # Data leak risk (q1 + q2 + q3), max raw = 30 + 25 + 20 = 75
    leak_raw: int = (
        RISK_SCORES["q1"][answers["q1"]]
        + RISK_SCORES["q2"][answers["q2"]]
        + RISK_SCORES["q3"][answers["q3"]]
    )
    data_leak: str = _map_to_label(
        leak_raw,
        {0: "Minimal", 20: "Low", 40: "Moderate", 60: "High", 75: "Certain"},
    )

    # ── Step 4: Select prophecies ─────────────────────────────────────────────
    # Phishing prophecy
    phishing_level = "high" if phishing_risk_pct >= 60 else ("medium" if phishing_risk_pct >= 30 else "low")
    phishing_prophecy: str = random.choice(content.CONTENT["phishing_prophecies"][phishing_level])

    # Password prophecy
    password_level = "high" if password_raw >= 20 else ("medium" if password_raw >= 10 else "low")
    password_prophecy: str = random.choice(content.CONTENT["password_prophecies"][password_level])

    # Wi-Fi prophecy
    wifi_level = "high" if wifi_raw >= 30 else ("medium" if wifi_raw >= 15 else "low")
    wifi_prophecy: str = random.choice(content.CONTENT["wifi_prophecies"][wifi_level])

    # Data leak prophecy
    leak_level = "high" if leak_raw >= 55 else ("medium" if leak_raw >= 25 else "low")
    leak_prophecy: str = random.choice(content.CONTENT["data_leak_prophecies"][leak_level])

    # Daily prophecy (always random, independent of score)
    daily_prophecy: str = random.choice(content.CONTENT["daily_security_prophecies"])

    # ── Step 5: Lucky charm and number ───────────────────────────────────────
    lucky_charm: str = random.choice(content.CONTENT["lucky_security_charms"])
    lucky_number: int = random.choice(content.CONTENT["lucky_security_numbers"])

    # ── Step 6: Roast mode (score >= 70) ─────────────────────────────────────
    roast: str | None = (
        random.choice(content.CONTENT["roast_mode"]["messages"])
        if final_score >= 70
        else None
    )

    # ── Step 7: Build and return response ────────────────────────────────────
    return {
        "final_score": final_score,
        "cyber_sign": sign_data["sign"],
        "cyber_sign_emoji": sign_data["emoji"],
        "cyber_sign_description": sign_data["description"],
        "dimensions": {
            "phishing_risk_pct": phishing_risk_pct,
            "password_aura": password_aura,
            "wifi_karma": wifi_karma,
            "scam_magnet_level": scam_magnet,
            "data_leak_risk": data_leak,
        },
        "prophecies": {
            "phishing": phishing_prophecy,
            "password": password_prophecy,
            "wifi": wifi_prophecy,
            "data_leak": leak_prophecy,
            "daily": daily_prophecy,
        },
        "lucky_security_charm": lucky_charm,
        "lucky_security_number": lucky_number,
        "roast_message": roast,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    }


# ─────────────────────────────────────────────
# Private helpers
# ─────────────────────────────────────────────
def _map_to_label(score: int, thresholds: dict) -> str:
    """
    Map a numeric score to a label string using threshold buckets.

    Parameters
    ----------
    score      : int  — the score to classify
    thresholds : dict — {min_score: label} mapping (int keys)

    Returns
    -------
    str — the label for the highest threshold that score >= min_score.

    Example
    -------
    score=15, thresholds={0: "A", 10: "B", 20: "C"} → "B"
    """
    result_label: str = ""
    for min_score in sorted(thresholds.keys()):
        if score >= min_score:
            result_label = thresholds[min_score]
    return result_label


# ── Developer Mode Engine ───────────────────────────────────────────────────
# Added in v2.0.0. Everything above this line is unchanged.

DEV_RISK_SCORES: dict[str, dict[str, int]] = {
    "q1": {"always": 30, "sometimes": 15, "never": 0},   # hardcoded secrets
    "q2": {"never": 25, "sometimes": 12, "always": 0},   # CVE handling
    "q3": {"always": 25, "sometimes": 12, "never": 0},   # prod as test env
    "q4": {"none": 20, "sometimes": 10, "always": 0},    # code review / branch protection
    "q5": {"always": 20, "sometimes": 10, "never": 0},   # error exposure
}

DEV_RAW_MAX: int = 120  # 30+25+25+20+20

DEV_CYBER_SIGNS: list[dict] = [
    {"threshold": 20,  "sign": "Zero Trust Architect",     "emoji": "🏰", "description": "Your codebase is a fortress. Security engineers weep with joy."},
    {"threshold": 40,  "sign": "Dependency Guardian",      "emoji": "🛡️", "description": "You patch things before they become CVEs. Rare energy."},
    {"threshold": 60,  "sign": "The Merge Conflict",       "emoji": "⚠️", "description": "Your intentions are good. Your .env file tells a different story."},
    {"threshold": 80,  "sign": "Prod Cowboy",              "emoji": "🤠", "description": "You deploy on Fridays. You test on prod. You live dangerously."},
    {"threshold": 100, "sign": "Supply Chain Catastrophe", "emoji": "💀", "description": "Your npm install is a threat actor's favourite moment of the day."},
]


def generate_dev(answers: dict) -> dict:
    """Generate a developer-mode cyber horoscope. Added v2.0.0."""
    # ── Step 1: Calculate final score ────────────────────────────────────────
    raw_score: int = sum(DEV_RISK_SCORES[q][answers[q]] for q in DEV_RISK_SCORES)
    final_score: int = round((raw_score / DEV_RAW_MAX) * 100)

    # ── Step 2: Determine cyber sign ─────────────────────────────────────────
    sign_data: dict = DEV_CYBER_SIGNS[-1]  # fallback to highest tier
    for entry in DEV_CYBER_SIGNS:
        if final_score <= entry["threshold"]:
            sign_data = entry
            break

    # ── Step 3: Calculate dimension scores ───────────────────────────────────
    secret_raw: int     = DEV_RISK_SCORES["q1"][answers["q1"]]
    dep_raw: int        = DEV_RISK_SCORES["q2"][answers["q2"]]
    env_raw: int        = DEV_RISK_SCORES["q3"][answers["q3"]]
    integrity_raw: int  = DEV_RISK_SCORES["q4"][answers["q4"]]
    error_raw: int      = DEV_RISK_SCORES["q5"][answers["q5"]]

    secret_label    = _map_to_label(secret_raw,    {0: "Immaculate",    15: "Questionable",      30: "GitHub Search Nightmare"})
    dep_label       = _map_to_label(dep_raw,       {0: "Fort Knox",     12: "Probably Fine",     25: "CVE Buffet"})
    env_label       = _map_to_label(env_raw,       {0: "Textbook",      12: "Casual Chaos",      25: "Prod is Dev"})
    integrity_label = _map_to_label(integrity_raw, {0: "Signed & Sealed", 10: "Loosely Gated",   20: "Yolo Push"})
    error_label     = _map_to_label(error_raw,     {0: "Silent & Secure", 10: "Occasionally Chatty", 20: "Stack Trace as a Feature"})

    # ── Step 4: Prophecy tier selection ──────────────────────────────────────
    secret_level   = "high" if secret_raw    >= 20 else ("medium" if secret_raw    >= 10 else "low")
    dep_level      = "high" if dep_raw       >= 20 else ("medium" if dep_raw       >= 10 else "low")
    env_level      = "high" if env_raw       >= 20 else ("medium" if env_raw       >= 10 else "low")
    int_level      = "high" if integrity_raw >= 15 else ("medium" if integrity_raw >=  8 else "low")
    err_level      = "high" if error_raw     >= 15 else ("medium" if error_raw     >=  8 else "low")

    # ── Step 5: Roast mode (score >= 70) ─────────────────────────────────────
    roast: str | None = (
        random.choice(content.DEV_CONTENT["dev_roast_messages"])
        if final_score >= 70
        else None
    )

    # ── Step 6: Build and return response ────────────────────────────────────
    return {
        "mode": "dev",
        "final_score": final_score,
        "cyber_sign": sign_data["sign"],
        "cyber_sign_emoji": sign_data["emoji"],
        "cyber_sign_description": sign_data["description"],
        "dimensions": {
            "secret_hygiene":          secret_label,
            "dependency_health":       dep_label,
            "environment_discipline":  env_label,
            "code_integrity":          integrity_label,
            "error_exposure":          error_label,
        },
        "prophecies": {
            "secrets":      random.choice(content.DEV_CONTENT["secret_prophecies"][secret_level]),
            "dependencies": random.choice(content.DEV_CONTENT["dependency_prophecies"][dep_level]),
            "environment":  random.choice(content.DEV_CONTENT["environment_prophecies"][env_level]),
            "code":         random.choice(content.DEV_CONTENT["code_integrity_prophecies"][int_level]),
            "errors":       random.choice(content.DEV_CONTENT["error_exposure_prophecies"][err_level]),
            "daily":        random.choice(content.DEV_CONTENT["daily_dev_prophecies"]),
        },
        "lucky_security_charm":  random.choice(content.DEV_CONTENT["lucky_dev_charms"]),
        "lucky_security_number": random.choice(content.DEV_CONTENT["lucky_dev_numbers"]),
        "roast_message": roast,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    }
