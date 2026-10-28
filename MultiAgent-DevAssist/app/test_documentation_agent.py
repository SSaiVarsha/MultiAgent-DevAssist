from agents.documentation_agent import generate_documentation


code = """
def calculate_total(price, quantity):
    total = price * quantity
    return total


result = calculate_total(100, 5)
print(result)
"""


result = generate_documentation(code)

print("\n===== DOCUMENTATION AGENT =====\n")
print(result)