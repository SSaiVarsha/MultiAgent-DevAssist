from app.services.ollama_service import ask_ollama


def analyze_security(code: str) -> str:

    prompt = f"""
You are the Security Agent in DevAssist, an AI-powered
software engineering platform.

Your tasks are:
1. Identify security vulnerabilities in the source code.
2. Explain confirmed vulnerabilities and their severity.
3. Generate a corrected version of the complete source code.

STRICT EVIDENCE RULES:

- Report vulnerabilities supported by the supplied code.
- Do not invent vulnerabilities or assume missing functionality.
- Distinguish confirmed vulnerabilities from potential risks.
- Do not claim that code is completely secure based only on
  a limited source-code review.
- Do not remove essential functionality to eliminate a warning.
- Do not introduce new vulnerabilities while fixing existing ones.

CHECK FOR:

1. Hard-coded credentials and secrets
2. SQL injection
3. Command injection
4. Unsafe eval() and exec()
5. Unsafe deserialization
6. Path traversal
7. Insecure file operations
8. Authentication and authorization weaknesses
9. Sensitive data exposure
10. Unsafe handling of user-controlled input

FOR EACH CONFIRMED VULNERABILITY, REPORT:

- Severity: Critical, High, Medium, or Low
- Vulnerability type
- Relevant source code
- Explanation of the problem
- Why it matters
- Recommended fix

SECURE FIX REQUIREMENTS:

- Return the complete corrected source code, not a fragment.
- Preserve the original intended functionality wherever possible.
- Make the smallest practical changes needed to address the
  identified vulnerabilities.
- Prefer allowlists and fixed permitted operations when
  user input could control operating-system commands.
- Do not assume that replacing os.system() with subprocess.run()
  automatically makes arbitrary user-controlled commands safe.
- When using subprocess, prefer argument lists and shell=False.
- Validate inputs according to their intended use.
- Do not invent credentials, API keys, or configuration values.
- If a safe correction cannot be determined, explain why and
  do not pretend the code has been fixed.
- If no fix is necessary, return the original source code.

Use this exact response structure:

SECURITY SUMMARY

[Brief summary]

CONFIRMED VULNERABILITIES

[Details, or None identified.]

POSITIVE SECURITY ASPECTS

[Relevant observations, or None identified.]

RECOMMENDED IMPROVEMENTS

[Specific recommendations, or None identified.]

SECURITY FIX STATUS

[FIXED, NO_FIX_REQUIRED, or MANUAL_REVIEW_REQUIRED]

SECURITY_FIXED_CODE_START

[Complete corrected source code only]

SECURITY_FIXED_CODE_END

SOURCE CODE:

{code}
"""

    return ask_ollama(prompt)