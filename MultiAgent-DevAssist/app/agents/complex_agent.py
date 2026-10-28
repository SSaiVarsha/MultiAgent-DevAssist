from app.services.ollama_service import ask_ollama


def analyze_complex_code(code: str) -> str:
    prompt = f"""
You are a complex software analysis agent in a multi-agent
software engineering assistant.

Perform a comprehensive analysis of the following code.

Analyze:
1. Possible bugs and errors
2. Code quality and readability
3. Time complexity
4. Space complexity
5. Performance issues
6. Maintainability
7. Security concerns if applicable
8. Possible improvements
9. Documentation requirements
10. Test cases that should be created

For each important issue:
- Explain it in simple words.
- Explain why it matters.
- Suggest a practical solution.

Finally provide:
- Overall assessment
- Priority of the issues
- Recommended next steps

Use clear headings and structured output.

Here is the code:

{code}
"""

    return ask_ollama(prompt)