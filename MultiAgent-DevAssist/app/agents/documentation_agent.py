from app.services.ollama_service import ask_ollama


def generate_documentation(code: str) -> str:
    prompt = f"""
You are a documentation agent in a software engineering assistant.

Analyze the following code and generate clear documentation.

Include:
1. What the code does
2. Purpose of each function
3. Input parameters
4. Return values
5. Important logic or steps
6. Example usage
7. Any important notes for a developer

Use simple and clear language.

Here is the code:

{code}
"""

    return ask_ollama(prompt)