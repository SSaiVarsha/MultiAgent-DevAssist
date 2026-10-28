from agents.coordinator import choose_agents


requests = [
    "Find bugs in this Python code.",
    "Improve the performance of this code.",
    "Generate documentation for this function.",
    "Create test cases for this code.",
    "Review this code completely and find all possible improvements."
]


for request in requests:
    result = choose_agents(request)

    print("\n==============================")
    print("USER REQUEST:")
    print(request)
    print("\nSELECTED AGENTS:")
    print(result)