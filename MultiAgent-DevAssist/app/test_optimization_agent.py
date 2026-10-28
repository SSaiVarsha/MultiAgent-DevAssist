from agents.optimization_agent import optimize_code


code = """
def find_duplicates(numbers):
    duplicates = []

    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                if numbers[i] not in duplicates:
                    duplicates.append(numbers[i])

    return duplicates


numbers = [1, 2, 3, 2, 4, 3, 5]
print(find_duplicates(numbers))
"""


result = optimize_code(code)

print("\n===== OPTIMIZATION AGENT =====\n")
print(result)