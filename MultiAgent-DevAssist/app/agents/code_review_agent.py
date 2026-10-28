from app.services.ollama_service import ask_ollama


def check_code_quality(code: str) -> str:

    prompt = f"""
You are the Code Review Agent in DevAssist.

Review ONLY the source code provided below.

Your job is to evaluate:
1. Readability
2. Naming conventions
3. Code structure
4. Duplicate or unnecessary code
5. Maintainability
6. Appropriate coding practices

IMPORTANT RULES:

1. Do NOT invent problems.
2. Do NOT treat optional improvements as bugs.
3. Do NOT assume requirements that are not shown in the code.
4. Do NOT assume that an input is invalid unless the code
or user request clearly establishes that requirement.
5. Do NOT recommend generic error handling.
6. Do NOT recommend generic security improvements.
7. Do NOT recommend input validation unless the source code
clearly shows a validation-related problem.
8. Do NOT recommend comments or documentation simply because
they could theoretically be added.
9. If the code is already good, clearly say so.
10. Focus on actual code quality observations.

Separate your response into:

OVERALL REVIEW

POSITIVE ASPECTS

CONFIRMED QUALITY ISSUES

OPTIONAL IMPROVEMENTS

For CONFIRMED QUALITY ISSUES:
Only include actual problems visible in the code.

For OPTIONAL IMPROVEMENTS:
Only include improvements that are genuinely useful for this
specific code.

If there are no confirmed quality issues, write:

None identified.

If there are no relevant optional improvements, write:

None identified.

IMPORTANT:

Do not rewrite the entire code unless a change is necessary
to demonstrate a specific improvement.

Keep the review concise and professional.

SOURCE CODE:

{code}
"""

    return ask_ollama(prompt)