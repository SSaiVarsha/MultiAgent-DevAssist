from app.services.ollama_service import ask_ollama


def aggregate_results(request: str, results: dict) -> str:

    combined_results = ""

    for agent, result in results.items():
        combined_results += f"""
===== {agent} RESULT =====

{result}

"""

    prompt = f"""
You are the Result Aggregation and Prioritization component
of DevAssist.

User request:
{request}

The following specialized agents analyzed the code:

{combined_results}

Your job is to combine their findings accurately.

IMPORTANT RULES:

1. Do NOT invent problems.

2. Do NOT convert suggestions into confirmed bugs.

3. A confirmed issue must have clear evidence in the provided
agent analysis.

4. Optional validation, error handling, security hardening,
style improvements, or future enhancements must NOT be treated
as confirmed bugs unless the code clearly demonstrates the problem.

5. Keep these categories separate:

CONFIRMED ISSUES
Actual problems clearly identified in the code.

POTENTIAL ISSUES
Problems that may occur under specific conditions.

OPTIONAL IMPROVEMENTS
Suggestions that improve quality but are not bugs.

6. Only CONFIRMED ISSUES may receive:
HIGH
MEDIUM
LOW

7. POTENTIAL ISSUES must not be given the same priority as
confirmed bugs.

8. Remove duplicate findings.

9. Do not repeat the same issue in multiple sections.

10. If no confirmed issues exist, clearly say:
"No confirmed issues identified."

Use this structure:

OVERALL ASSESSMENT

CONFIRMED ISSUES

POTENTIAL ISSUES

OPTIONAL IMPROVEMENTS

POSITIVE ASPECTS

RECOMMENDED ACTIONS

FINAL RECOMMENDATION

For confirmed issues, include:
- Issue
- Type
- Priority
- Why it is a real problem
- Suggested fix

For potential issues:
- Condition under which the issue may occur
- Why it is only potential

For optional improvements:
- Improvement
- Benefit

Use simple and professional language.

IMPORTANT STRICT FILTERING RULES:

11. Never place a confirmed issue in POTENTIAL ISSUES.

12. Never place a confirmed issue in OPTIONAL IMPROVEMENTS.

13. If the Debugging Agent identifies a syntax error,
keep it only under CONFIRMED ISSUES.

14. Do not create a potential issue merely by describing
another situation in which the same confirmed error could occur.

15. Do not recommend type hints, comments, documentation,
security improvements, validation, or error handling unless
they are directly relevant to the user's request or supported
by an agent finding.

16. Do not add generic programming advice.

17. Every finding must be traceable to the source code,
execution error, or an explicit agent finding.

18. If an issue is already confirmed, remove duplicate
versions of that issue from all other sections.

Do not mention that you are an AI.
"""

    return ask_ollama(prompt)