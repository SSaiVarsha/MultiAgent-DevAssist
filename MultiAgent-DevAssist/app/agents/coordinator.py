from app.agents.debugging_agent import debug_code
from app.agents.code_review_agent import check_code_quality
from app.agents.optimization_agent import optimize_code
from app.agents.documentation_agent import generate_documentation
from app.agents.test_case_agent import generate_test_cases
from app.agents.complex_agent import analyze_complex_code
from app.agents.security_agent import analyze_security


AVAILABLE_AGENTS = [
    "DEBUG",
    "CODE_REVIEW",
    "OPTIMIZATION",
    "DOCUMENTATION",
    "TEST_CASE",
    "SECURITY",
    "COMPLEX"
]


def choose_agents(request: str) -> str:
    """
    Select agents using deterministic keyword-based routing.
    This avoids unreliable LLM agent selection for common requests.
    """

    request_lower = request.lower()

    selected_agents = []

    # Debugging
    debug_keywords = [
        "bug",
        "bugs",
        "error",
        "errors",
        "debug",
        "debugging",
        "wrong output",
        "fix error"
    ]

    if any(
        keyword in request_lower
        for keyword in debug_keywords
    ):
        selected_agents.append("DEBUG")

    # Code Review
    review_keywords = [
        "code review",
        "review code",
        "review my code",
        "readability",
        "maintainability",
        "best practices",
        "code quality",
        "clean code"
    ]

    if any(
        keyword in request_lower
        for keyword in review_keywords
    ):
        selected_agents.append("CODE_REVIEW")

    # Optimization
    optimization_keywords = [
        "performance",
        "optimize",
        "optimization",
        "efficient",
        "efficiency",
        "time complexity",
        "space complexity",
        "faster",
        "memory usage"
    ]

    if any(
        keyword in request_lower
        for keyword in optimization_keywords
    ):
        selected_agents.append("OPTIMIZATION")

    # Documentation
    documentation_keywords = [
        "documentation",
        "document",
        "explain the code",
        "generate documentation",
        "comments",
        "docstring"
    ]

    if any(
        keyword in request_lower
        for keyword in documentation_keywords
    ):
        selected_agents.append("DOCUMENTATION")

    # Test cases
    test_keywords = [
        "test cases",
        "test case",
        "testing",
        "tests",
        "pytest",
        "unit test"
    ]

    if any(
        keyword in request_lower
        for keyword in test_keywords
    ):
        selected_agents.append("TEST_CASE")

    # Security
    security_keywords = [
        "security",
        "security analysis",
        "security issues",
        "security vulnerabilities",
        "vulnerabilities",
        "secure code",
        "security review"
    ]

    if any(
        keyword in request_lower
        for keyword in security_keywords
    ):
        selected_agents.append("SECURITY")

    # Comprehensive analysis
    complex_keywords = [
        "comprehensive analysis",
        "complete analysis",
        "full analysis",
        "analyze everything",
        "overall analysis",
        "all improvements"
    ]

    if any(
        keyword in request_lower
        for keyword in complex_keywords
    ):
        selected_agents.append("COMPLEX")

    # Remove duplicates while preserving order
    selected_agents = list(
        dict.fromkeys(selected_agents)
    )

    # If no specific agent is identified,
    # use the comprehensive analysis agent.
    if not selected_agents:
        selected_agents.append("COMPLEX")

    return ", ".join(selected_agents)


def run_agents(
    request: str,
    code: str,
    execution_error: str = "",
    requirement: str = ""
) -> dict:

    selected_agents = choose_agents(request)

    results = {}

    if "DEBUG" in selected_agents:
        results["DEBUG"] = debug_code(
            code,
            execution_error
        )

    if "CODE_REVIEW" in selected_agents:
        results["CODE_REVIEW"] = check_code_quality(code)

    if "OPTIMIZATION" in selected_agents:
        results["OPTIMIZATION"] = optimize_code(code)

    if "DOCUMENTATION" in selected_agents:
        results["DOCUMENTATION"] = generate_documentation(code)

    if "TEST_CASE" in selected_agents:
        results["TEST_CASE"] = generate_test_cases(
            code,
            requirement
        )

    if "SECURITY" in selected_agents:
        results["SECURITY"] = analyze_security(code)

    if "COMPLEX" in selected_agents:
        results["COMPLEX"] = analyze_complex_code(code)

    return {
        "selected_agents": selected_agents,
        "results": results
    }