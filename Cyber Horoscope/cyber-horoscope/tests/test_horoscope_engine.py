"""
CyberHoroscope — Unit Tests
=============================
pytest test suite covering:
  - Boundary score calculations
  - Cyber sign assignment
  - Roast mode threshold
  - Response structure completeness
  - Input validation
  - Lambda handler integration
  - Lucky number validity
  - generated_at format
"""

import json
import sys
import os

import pytest

# ── Path setup ───────────────────────────────────────────────────────────────
# Allow imports from src/ when running pytest from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import horoscope_engine as engine
import validator as val

# ─────────────────────────────────────────────
# FIXTURES — common answer sets
# ─────────────────────────────────────────────

@pytest.fixture
def worst_answers():
    """All worst choices → maximum raw score (120) → final_score 100."""
    return {"q1": "always", "q2": "none", "q3": "never", "q4": "regularly", "q5": "always"}


@pytest.fixture
def best_answers():
    """All best choices → raw score 0 → final_score 0."""
    return {"q1": "never", "q2": "all", "q3": "always", "q4": "never", "q5": "never"}


@pytest.fixture
def medium_answers():
    """Middle-of-the-road answers."""
    return {
        "q1": "sometimes",
        "q2": "some",
        "q3": "sometimes",
        "q4": "once_or_twice",
        "q5": "sometimes",
    }


@pytest.fixture
def roast_threshold_answers():
    """
    Answers that produce final_score == 71 (just over roast threshold of 70).
    Raw score: q1=30, q2=25, q3=0, q4=0, q5=30-is-not-possible → craft carefully.

    q1=always(30) + q2=none(25) + q3=sometimes(10) + q4=never(0) + q5=always(20) = 85 raw
    final = round(85/120*100) = round(70.83) = 71  ✓
    """
    return {"q1": "always", "q2": "none", "q3": "sometimes", "q4": "never", "q5": "always"}


# ─────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────

class TestScoreBoundaries:
    """Tests for score calculation at boundaries."""

    def test_max_risk_score(self, worst_answers):
        """All worst answers → final_score == 100, sign == Data Breach Influencer."""
        result = engine.generate(worst_answers)
        assert result["final_score"] == 100
        assert result["cyber_sign"] == "Data Breach Influencer"
        assert result["roast_message"] is not None

    def test_min_risk_score(self, best_answers):
        """All best answers → final_score == 0, sign == Firewall Phoenix."""
        result = engine.generate(best_answers)
        assert result["final_score"] == 0
        assert result["cyber_sign"] == "Firewall Phoenix"
        assert result["roast_message"] is None

    def test_raw_max_is_120(self, worst_answers):
        """Verify the RAW_MAX constant matches expected sum."""
        raw = sum(engine.RISK_SCORES[q][worst_answers[q]] for q in engine.RISK_SCORES)
        assert raw == 120
        assert engine.RAW_MAX == 120

    def test_score_normalisation(self, worst_answers, best_answers):
        """Score is correctly normalised to 0–100 range."""
        assert engine.generate(worst_answers)["final_score"] == 100
        assert engine.generate(best_answers)["final_score"] == 0


class TestCyberSigns:
    """Tests for cyber sign assignment across thresholds."""

    def test_firewall_phoenix_at_zero(self, best_answers):
        result = engine.generate(best_answers)
        assert result["cyber_sign"] == "Firewall Phoenix"
        assert result["cyber_sign_emoji"] == "🦅"

    def test_data_breach_influencer_at_100(self, worst_answers):
        result = engine.generate(worst_answers)
        assert result["cyber_sign"] == "Data Breach Influencer"
        assert result["cyber_sign_emoji"] == "📢"

    def test_sign_description_is_non_empty(self, medium_answers):
        result = engine.generate(medium_answers)
        assert len(result["cyber_sign_description"]) > 0


class TestRoastMode:
    """Tests for the roast message threshold behaviour."""

    def test_roast_triggered_above_70(self, roast_threshold_answers):
        """Score >= 70 should include a roast message."""
        result = engine.generate(roast_threshold_answers)
        assert result["final_score"] >= 70
        assert result["roast_message"] is not None
        assert isinstance(result["roast_message"], str)
        assert len(result["roast_message"]) > 0

    def test_roast_absent_below_70(self, best_answers):
        """Score < 70 should have roast_message == None."""
        result = engine.generate(best_answers)
        assert result["final_score"] < 70
        assert result["roast_message"] is None

    def test_roast_absent_for_medium_score(self):
        """Mid-range score that doesn't reach 70."""
        # q1=never(0) + q2=some(10) + q3=sometimes(10) + q4=never(0) + q5=never(0) = 20 raw
        # final = round(20/120*100) = 17
        answers = {"q1": "never", "q2": "some", "q3": "sometimes", "q4": "never", "q5": "never"}
        result = engine.generate(answers)
        assert result["final_score"] < 70
        assert result["roast_message"] is None


class TestResponseStructure:
    """Tests that the response always contains all required keys."""

    REQUIRED_TOP_LEVEL_KEYS = {
        "final_score", "cyber_sign", "cyber_sign_emoji", "cyber_sign_description",
        "dimensions", "prophecies", "lucky_security_charm", "lucky_security_number",
        "roast_message", "generated_at",
    }
    REQUIRED_DIMENSION_KEYS = {
        "phishing_risk_pct", "password_aura", "wifi_karma",
        "scam_magnet_level", "data_leak_risk",
    }
    REQUIRED_PROPHECY_KEYS = {"phishing", "password", "wifi", "data_leak", "daily"}

    def test_all_keys_present(self, medium_answers):
        """Response always contains all required top-level keys."""
        result = engine.generate(medium_answers)
        assert self.REQUIRED_TOP_LEVEL_KEYS.issubset(result.keys())

    def test_all_dimension_keys_present(self, medium_answers):
        result = engine.generate(medium_answers)
        assert self.REQUIRED_DIMENSION_KEYS.issubset(result["dimensions"].keys())

    def test_all_prophecy_keys_present(self, medium_answers):
        result = engine.generate(medium_answers)
        assert self.REQUIRED_PROPHECY_KEYS.issubset(result["prophecies"].keys())

    def test_prophecies_are_non_empty_strings(self, medium_answers):
        result = engine.generate(medium_answers)
        for key, value in result["prophecies"].items():
            assert isinstance(value, str), f"prophecies.{key} should be a string"
            assert len(value) > 0, f"prophecies.{key} should not be empty"

    def test_score_is_in_valid_range(self, medium_answers):
        result = engine.generate(medium_answers)
        assert 0 <= result["final_score"] <= 100


class TestGeneratedAtFormat:
    """Tests for the generated_at timestamp format."""

    def test_generated_at_ends_with_z(self, medium_answers):
        result = engine.generate(medium_answers)
        assert result["generated_at"].endswith("Z"), (
            f"generated_at should end with 'Z', got: {result['generated_at']}"
        )

    def test_generated_at_is_iso8601(self, medium_answers):
        import datetime
        result = engine.generate(medium_answers)
        ts = result["generated_at"].rstrip("Z")
        # Should parse without exception
        datetime.datetime.fromisoformat(ts)


class TestLuckyNumber:
    """Tests for lucky_security_number validity."""

    VALID_LUCKY_NUMBERS = {404, 443, 1337, 8080, 256, 2048, 3389}

    def test_lucky_number_is_valid(self, medium_answers):
        result = engine.generate(medium_answers)
        assert result["lucky_security_number"] in self.VALID_LUCKY_NUMBERS, (
            f"Unexpected lucky number: {result['lucky_security_number']}"
        )

    def test_lucky_charm_is_non_empty(self, medium_answers):
        result = engine.generate(medium_answers)
        assert isinstance(result["lucky_security_charm"], str)
        assert len(result["lucky_security_charm"]) > 0


class TestValidator:
    """Tests for input validation logic."""

    def test_validator_missing_question(self):
        """Missing q3 should return a validation error."""
        answers = {"q1": "always", "q2": "none", "q4": "regularly", "q5": "always"}
        error = val.validate_answers(answers)
        assert error == "Missing answer for q3"

    def test_validator_invalid_value(self):
        """q1 = 'maybe' should return a descriptive error."""
        answers = {"q1": "maybe", "q2": "none", "q3": "never", "q4": "regularly", "q5": "always"}
        error = val.validate_answers(answers)
        assert error is not None
        assert "Invalid value 'maybe' for q1" in error

    def test_validator_valid_answers(self, best_answers):
        """All valid answers should return None."""
        assert val.validate_answers(best_answers) is None

    def test_validator_non_dict_input(self):
        """Non-dict input should fail gracefully."""
        error = val.validate_answers("not a dict")
        assert error is not None
        assert "object" in error.lower()

    def test_validator_empty_dict(self):
        """Empty dict should report the first missing question."""
        error = val.validate_answers({})
        assert error is not None
        assert "Missing answer for q1" in error

    def test_validator_all_questions_checked(self):
        """Each question ID is validated."""
        for qid in ["q1", "q2", "q3", "q4", "q5"]:
            answers = {
                "q1": "never", "q2": "all", "q3": "always",
                "q4": "never", "q5": "never",
            }
            del answers[qid]
            error = val.validate_answers(answers)
            assert f"Missing answer for {qid}" in error


class TestLambdaHandler:
    """Integration tests for the Lambda handler."""

    def _make_event(self, answers: dict, route_key: str = "POST /horoscope") -> dict:
        return {
            "routeKey": route_key,
            "body": json.dumps({"answers": answers}),
        }

    def test_response_200_structure(self, best_answers):
        """Valid input via lambda_handler should return statusCode 200."""
        import handler
        event = self._make_event(best_answers)
        response = handler.lambda_handler(event, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "final_score" in body
        assert "cyber_sign" in body

    def test_health_check_returns_200(self):
        """GET /health should return 200 with healthy status."""
        import handler
        event = {"routeKey": "GET /health", "body": None}
        response = handler.lambda_handler(event, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["status"] == "healthy"

    def test_invalid_json_returns_400(self):
        """Malformed JSON body should return 400."""
        import handler
        event = {"routeKey": "POST /horoscope", "body": "not json {{{"}
        response = handler.lambda_handler(event, None)
        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert body["error"] == "INVALID_JSON"

    def test_invalid_answers_returns_400(self):
        """Invalid answer value should return 400 with INVALID_ANSWERS error."""
        import handler
        event = self._make_event(
            {"q1": "maybe", "q2": "none", "q3": "never", "q4": "regularly", "q5": "always"}
        )
        response = handler.lambda_handler(event, None)
        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert body["error"] == "INVALID_ANSWERS"

    def test_cors_headers_present(self, best_answers):
        """All responses must include CORS headers."""
        import handler
        event = self._make_event(best_answers)
        response = handler.lambda_handler(event, None)
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"
        assert "POST" in response["headers"]["Access-Control-Allow-Methods"]


# ─────────────────────────────────────────────
# DEVELOPER MODE FIXTURES — added v2.0.0
# ─────────────────────────────────────────────

@pytest.fixture
def dev_worst_answers():
    """All worst developer answers → maximum raw score (120) → final_score 100."""
    return {"q1": "always", "q2": "never", "q3": "always", "q4": "none", "q5": "always"}


@pytest.fixture
def dev_best_answers():
    """All best developer answers → raw score 0 → final_score 0."""
    return {"q1": "never", "q2": "always", "q3": "never", "q4": "always", "q5": "never"}


@pytest.fixture
def dev_medium_answers():
    """Middle-of-the-road developer answers."""
    return {
        "q1": "sometimes",
        "q2": "sometimes",
        "q3": "sometimes",
        "q4": "sometimes",
        "q5": "sometimes",
    }


# ─────────────────────────────────────────────
# DEVELOPER MODE TEST CASES — added v2.0.0
# ─────────────────────────────────────────────

class TestDevScoreBoundaries:
    """Tests for developer mode score calculation at boundaries."""

    def test_dev_max_risk_score(self, dev_worst_answers):
        """All worst dev answers → final_score == 100, sign == Supply Chain Catastrophe."""
        result = engine.generate_dev(dev_worst_answers)
        assert result["final_score"] == 100
        assert result["cyber_sign"] == "Supply Chain Catastrophe"
        assert result["roast_message"] is not None

    def test_dev_min_risk_score(self, dev_best_answers):
        """All best dev answers → final_score == 0, sign == Zero Trust Architect."""
        result = engine.generate_dev(dev_best_answers)
        assert result["final_score"] == 0
        assert result["cyber_sign"] == "Zero Trust Architect"
        assert result["roast_message"] is None

    def test_dev_raw_max_is_120(self, dev_worst_answers):
        """Verify DEV_RAW_MAX constant matches expected sum."""
        raw = sum(engine.DEV_RISK_SCORES[q][dev_worst_answers[q]] for q in engine.DEV_RISK_SCORES)
        assert raw == 120
        assert engine.DEV_RAW_MAX == 120

    def test_dev_mode_field_in_response(self, dev_medium_answers):
        """Developer mode response must include mode == 'dev'."""
        result = engine.generate_dev(dev_medium_answers)
        assert result.get("mode") == "dev"


class TestDevCyberSigns:
    """Tests for developer cyber sign assignment across thresholds."""

    def test_zero_trust_architect_at_zero(self, dev_best_answers):
        result = engine.generate_dev(dev_best_answers)
        assert result["cyber_sign"] == "Zero Trust Architect"
        assert result["cyber_sign_emoji"] == "🏰"

    def test_supply_chain_catastrophe_at_100(self, dev_worst_answers):
        result = engine.generate_dev(dev_worst_answers)
        assert result["cyber_sign"] == "Supply Chain Catastrophe"
        assert result["cyber_sign_emoji"] == "💀"

    def test_sign_description_is_non_empty(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        assert len(result["cyber_sign_description"]) > 0


class TestDevResponseStructure:
    """Tests that developer mode response always contains all required keys."""

    REQUIRED_TOP_LEVEL_KEYS = {
        "mode", "final_score", "cyber_sign", "cyber_sign_emoji", "cyber_sign_description",
        "dimensions", "prophecies", "lucky_security_charm", "lucky_security_number",
        "roast_message", "generated_at",
    }
    REQUIRED_DIMENSION_KEYS = {
        "secret_hygiene", "dependency_health", "environment_discipline",
        "code_integrity", "error_exposure",
    }
    REQUIRED_PROPHECY_KEYS = {"secrets", "dependencies", "environment", "code", "errors", "daily"}

    def test_all_keys_present(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        assert self.REQUIRED_TOP_LEVEL_KEYS.issubset(result.keys())

    def test_all_dimension_keys_present(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        assert self.REQUIRED_DIMENSION_KEYS.issubset(result["dimensions"].keys())

    def test_all_prophecy_keys_present(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        assert self.REQUIRED_PROPHECY_KEYS.issubset(result["prophecies"].keys())

    def test_prophecies_are_non_empty_strings(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        for key, value in result["prophecies"].items():
            assert isinstance(value, str), f"prophecies.{key} should be a string"
            assert len(value) > 0, f"prophecies.{key} should not be empty"

    def test_score_is_in_valid_range(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        assert 0 <= result["final_score"] <= 100


class TestDevLuckyNumber:
    """Tests for developer mode lucky number validity."""

    VALID_DEV_NUMBERS = {443, 22, 8080, 3306, 9200, 1337, 4040, 6379}

    def test_lucky_number_is_valid(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        assert result["lucky_security_number"] in self.VALID_DEV_NUMBERS, (
            f"Unexpected dev lucky number: {result['lucky_security_number']}"
        )

    def test_lucky_charm_is_non_empty(self, dev_medium_answers):
        result = engine.generate_dev(dev_medium_answers)
        assert isinstance(result["lucky_security_charm"], str)
        assert len(result["lucky_security_charm"]) > 0


class TestDevValidator:
    """Tests for dev mode input validation."""

    def test_dev_validator_valid_answers(self, dev_best_answers):
        """All valid dev answers should return None."""
        assert val.validate_answers(dev_best_answers, mode="dev") is None

    def test_dev_validator_missing_question(self):
        """Missing q3 in dev mode should return a validation error."""
        answers = {"q1": "never", "q2": "always", "q4": "always", "q5": "never"}
        error = val.validate_answers(answers, mode="dev")
        assert error == "Missing answer for q3"

    def test_dev_validator_invalid_value(self):
        """User mode value 'none' is not valid for dev q2."""
        answers = {"q1": "never", "q2": "none", "q3": "never", "q4": "always", "q5": "never"}
        error = val.validate_answers(answers, mode="dev")
        assert error is not None
        assert "Invalid value 'none' for q2" in error

    def test_user_mode_default_unchanged(self):
        """Calling validate_answers without mode still validates user questions."""
        answers = {"q1": "always", "q2": "none", "q3": "never", "q4": "regularly", "q5": "always"}
        assert val.validate_answers(answers) is None

    def test_user_mode_rejects_dev_values(self):
        """User mode should reject dev-only values like q4='none'."""
        answers = {"q1": "always", "q2": "none", "q3": "never", "q4": "none", "q5": "always"}
        error = val.validate_answers(answers, mode="user")
        assert error is not None


class TestDevLambdaHandler:
    """Integration tests for the Lambda handler with dev mode."""

    def _make_dev_event(self, answers: dict) -> dict:
        return {
            "routeKey": "POST /horoscope",
            "body": json.dumps({"answers": answers, "mode": "dev"}),
        }

    def test_dev_response_200_structure(self, dev_best_answers):
        """Valid dev input should return statusCode 200 with mode == dev."""
        import handler
        event = self._make_dev_event(dev_best_answers)
        response = handler.lambda_handler(event, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "final_score" in body
        assert body.get("mode") == "dev"

    def test_missing_mode_defaults_to_user(self):
        """Request without mode field defaults to user mode — backward compatible."""
        import handler
        answers = {"q1": "never", "q2": "all", "q3": "always", "q4": "never", "q5": "never"}
        event = {
            "routeKey": "POST /horoscope",
            "body": json.dumps({"answers": answers}),
        }
        response = handler.lambda_handler(event, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        # User mode response has no "mode" field (or it's not "dev")
        assert body.get("mode") != "dev"

    def test_dev_invalid_answers_returns_400(self, dev_worst_answers):
        """Dev-mode values submitted with mode='user' should fail validation."""
        import handler
        # dev_worst_answers has q2='never' which is invalid for user mode
        event = {
            "routeKey": "POST /horoscope",
            "body": json.dumps({"answers": dev_worst_answers, "mode": "user"}),
        }
        response = handler.lambda_handler(event, None)
        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert body["error"] == "INVALID_ANSWERS"
