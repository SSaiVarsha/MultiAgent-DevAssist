from app.services.ollama_service import ask_ollama


def debug_code(code: str, execution_error: str = "") -> str:

    error_context = ""

    if execution_error:
        error_context = f"""
EXECUTION ERROR DETECTED:

{execution_error}

IMPORTANT:
This error came directly from the code execution or testing engine.

You MUST analyze this error together with the source code.

Do not ignore the execution error.
"""

    prompt = f"""
You are the Debugging Agent in DevAssist.

Your ONLY task is to find actual bugs or errors in the
SOURCE CODE provided below.

{error_context}

STRICT EVIDENCE RULE:

Every reported issue MUST be directly supported by:

1. The source code, OR
2. The execution error provided above.

Do NOT invent bugs.

Do NOT assume requirements that are not shown.

Do NOT add generic security warnings.

If an execution error or test failure is provided, identify
its exact cause.

For every confirmed issue provide:

- Issue type
- Problem
- Relevant code
- Why it happens
- Exact fix

Classify issues as:

1. SYNTAX ERROR
The code cannot be parsed or compiled.

2. LOGICAL ERROR
The code runs but produces an incorrect result.

3. RUNTIME ERROR
The code fails during execution.

4. POTENTIAL ERROR
Use only when the source clearly contains a condition
that can realistically cause failure.

IMPORTANT:

If an execution error or test failure is provided:

1. Treat it as direct evidence.
2. Identify the exact failure.
3. Find the corresponding location in the source code.
4. Report the confirmed issue.
5. Explain the exact correction.

AUTOMATIC FIX REQUIREMENT:

At the end of your response, provide a complete corrected
version of the SOURCE CODE.

The corrected code MUST:

- Preserve the original program functionality.
- Change ONLY what is necessary to fix the confirmed issue.
- Be complete and executable.
- NOT contain Markdown code fences.
- NOT contain explanations inside the code section.

Use exactly these markers:

CORRECTED_CODE_START

[complete corrected source code]

CORRECTED_CODE_END

If no fix is required, return the original source code
between the markers.

SOURCE CODE:

{code}
"""

    return ask_ollama(prompt)