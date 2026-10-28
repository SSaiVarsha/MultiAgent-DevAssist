from agents.coordinator import run_agents
from services.aggregator import aggregate_results
from services.report_generator import generate_report


request = "Find bugs in this code and improve its quality."

code = """
def calculate_total(price, quantity):
    result = price * quantity
    print(result)
    print(result)

calculate_total(100, 5)
"""


# Step 1: Run selected agents
agent_output = run_agents(request, code)


# Step 2: Aggregate their results
analysis = aggregate_results(
    request,
    agent_output["results"]
)


# Step 3: Generate final report
report = generate_report(
    request,
    analysis
)


print("\n================================")
print("FINAL REPORT")
print("================================")

print(report)