from services.ollama_service import ask_ollama


prompt = "Explain what a Python function is in 2 simple sentences."

answer = ask_ollama(prompt)

print("\nAI Response:\n")
print(answer)