from agents.debugging_agent import debug_code


code = """
def add_numbers(a, b):
    result = a + c
    return result

print(add_numbers(10, 20))
"""


result = debug_code(code)

print("\n===== DEBUGGING AGENT =====\n")
print(result)