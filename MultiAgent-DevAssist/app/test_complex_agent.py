from agents.complex_agent import analyze_complex_code


code = """
def calculate_average(numbers):
    total = 0

    for i in range(len(numbers)):
        total = total + numbers[i]

    average = total / len(numbers)

    return average


numbers = [10, 20, 30, 40]
print(calculate_average(numbers))
"""


result = analyze_complex_code(code)

print("\n===== COMPLEX AGENT =====\n")
print(result)