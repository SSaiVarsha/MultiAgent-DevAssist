from app.services.ollama_service import ask_ollama
from app.services.test_requirement import detect_expected_behavior


def generate_test_cases(code: str, requirement: str = "") -> str:

    expected_behavior = detect_expected_behavior(
        requirement,
        code
    )

    # For clearly detected simple operations, generate
    # deterministic tests instead of relying on the LLM
    # to determine expected values.

    if expected_behavior == "ADDITION":
        return """def test_add_normal_case():
    assert add(2, 3) == 5


def test_add_zero_case():
    assert add(0, 5) == 5


def test_add_negative_case():
    assert add(-2, -3) == -5


def test_add_mixed_numbers():
    assert add(-5, 10) == 5
"""

    if expected_behavior == "SUBTRACTION":
        return """def test_subtract_normal_case():
    assert subtract(5, 3) == 2


def test_subtract_zero_case():
    assert subtract(5, 0) == 5


def test_subtract_negative_case():
    assert subtract(-5, -3) == -2


def test_subtract_mixed_numbers():
    assert subtract(-5, 10) == -15
"""

    if expected_behavior == "MULTIPLICATION":
        return """def test_multiply_normal_case():
    assert multiply(5, 3) == 15


def test_multiply_zero_case():
    assert multiply(5, 0) == 0


def test_multiply_negative_case():
    assert multiply(-2, 3) == -6


def test_multiply_one_case():
    assert multiply(10, 1) == 10
"""

    if expected_behavior == "DIVISION":
        return """def test_divide_normal_case():
    assert divide(10, 2) == 5


def test_divide_one_case():
    assert divide(10, 1) == 10


def test_divide_decimal_case():
    assert divide(5, 2) == 2.5
"""

    # If the requirement is not one of the simple
    # deterministic cases, use the LLM.

    prompt = f"""
You are the Test Case Agent in DevAssist.

Generate executable Python pytest tests for the source code.

USER REQUIREMENT:

{requirement}

SOURCE CODE:

{code}

IMPORTANT:

The user requirement describes the expected behavior.

The source code may contain bugs.

Do NOT assume the current implementation is correct.

Expected values must be based on the requirement when
the requirement clearly specifies the behavior.

Do NOT simply execute the current implementation and
use its result as the expected value.

Return ONLY pytest Python code.

Do NOT return explanations.

Do NOT return Markdown code fences.

Do NOT redefine functions from the source code.

Assume the source code is imported automatically.

Every test must begin with:

def test_

Generate useful normal, boundary, and edge cases.

Use pytest.raises() only when an exception is clearly
expected from the requirement or source code.
"""

    return ask_ollama(prompt)