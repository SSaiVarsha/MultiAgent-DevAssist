from app.services.ollama_service import ask_ollama


def optimize_code(code: str) -> str:
    prompt = f"""
You are an optimization agent in a software engineering assistant.

Analyze the following code and identify opportunities to improve its efficiency.

Check for:
1. Time complexity
2. Space complexity
3. Unnecessary computations
4. Repeated operations
5. Inefficient loops or algorithms
6. Memory usage
7. Performance improvements
8. Better algorithms or data structures

For each issue:
- Explain the problem in simple words.
- Explain why it affects performance.
- Suggest an improvement.

If the code is already reasonably optimized, clearly mention that.

Also provide an improved version of the code when possible.

Here is the code:

{code}
"""

    return ask_ollama(prompt)