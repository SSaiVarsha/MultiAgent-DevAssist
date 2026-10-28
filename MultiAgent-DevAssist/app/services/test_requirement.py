import re


def detect_expected_behavior(requirement: str, code: str = "") -> str:
    """
    Detect simple expected behavior from the user's requirement.

    This is intentionally deterministic so the testing system
    does not depend entirely on LLM interpretation.
    """

    text = requirement.lower().strip()

    if not text:
        return ""

    # Addition / sum
    if (
        "return the sum" in text
        or "returns the sum" in text
        or "should add" in text
        or "should return the addition" in text
    ):
        return "ADDITION"

    # Subtraction / difference
    if (
        "return the difference" in text
        or "returns the difference" in text
        or "should subtract" in text
        or "should return the subtraction" in text
    ):
        return "SUBTRACTION"

    # Multiplication / product
    if (
        "return the product" in text
        or "returns the product" in text
        or "should multiply" in text
        or "should return the multiplication" in text
    ):
        return "MULTIPLICATION"

    # Division
    if (
        "return the quotient" in text
        or "returns the quotient" in text
        or "should divide" in text
        or "should return the division" in text
    ):
        return "DIVISION"

    return "UNKNOWN"