from agents.test_case_agent import generate_test_cases


code = """
def calculate_average(numbers):
    if not numbers:
        return None

    total = sum(numbers)
    return total / len(numbers)


print(calculate_average([10, 20, 30]))
"""


result = generate_test_cases(code)

print("\n===== TEST CASE AGENT =====\n")
print(result)
