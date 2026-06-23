"""
CyberHoroscope — Lambda Entry Point
====================================
Parses the API Gateway HTTP event, validates input, delegates to the
horoscope engine, and returns a properly formatted JSON response with
CORS headers.

Routes handled:
  GET  /health    → health check
  POST /horoscope → quiz submission → horoscope generation
"""

import json
import logging
import os

from horoscope_engine import generate, generate_dev
from validator import validate_answers

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


# ─────────────────────────────────────────────
# Public handler
# ─────────────────────────────────────────────
def lambda_handler(event: dict, context) -> dict:
    """
    AWS Lambda entry point.

    Parameters
    ----------
    event   : dict  — API Gateway HTTP API proxy event
    context : LambdaContext — runtime context (unused)

    Returns
    -------
    dict  — API Gateway proxy response (statusCode, headers, body)
    """
    logger.info("Received event: routeKey=%s", event.get("routeKey", "UNKNOWN"))

    # ── Health check ─────────────────────────────────────────────────────────
    if event.get("routeKey") == "GET /health":
        logger.info("Health check requested")
        return _response(200, {
            "status": "healthy",
            "message": "The cyber spirits are with us.",
        })

    # ── Parse request body ───────────────────────────────────────────────────
    try:
        raw_body = event.get("body") or "{}"
        body: dict = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        logger.warning("JSON parse error: %s", exc)
        return _response(400, {
            "error": "INVALID_JSON",
            "message": "Request body must be valid JSON.",
            "status": 400,
        })

    # ── Validate answers ──────────────────────────────────────────────────────
    mode = body.get("mode", "user")   # "user" default — fully backward compatible
    answers = body.get("answers", {})
    validation_error = validate_answers(answers, mode)
    if validation_error:
        logger.warning("Validation failed: %s", validation_error)
        return _response(400, {
            "error": "INVALID_ANSWERS",
            "message": validation_error,
            "status": 400,
        })

    # ── Generate horoscope ────────────────────────────────────────────────────
    try:
        if mode == "dev":
            result = generate_dev(answers)
        else:
            result = generate(answers)
        logger.info(
            "Horoscope generated: score=%s sign=%s",
            result.get("final_score"),
            result.get("cyber_sign"),
        )
        return _response(200, result)
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Unexpected error in horoscope engine: %s", exc, exc_info=True)
        return _response(500, {
            "error": "INTERNAL_ERROR",
            "message": "The cybersecurity cosmos is temporarily misaligned. Please try again.",
            "status": 500,
        })


# ─────────────────────────────────────────────
# Response helper
# ─────────────────────────────────────────────
def _response(status_code: int, body: dict) -> dict:
    """
    Build an API Gateway HTTP proxy response dict.

    Always includes CORS headers so the browser SPA can call from any origin.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }
