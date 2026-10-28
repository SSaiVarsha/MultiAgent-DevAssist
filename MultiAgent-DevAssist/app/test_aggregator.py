from agents.coordinator import run_agents
from services.aggregator import aggregate_results


request = "Find bugs in this code and improve its quality."

code = """
def calculate_total(price, quantity):
    result = price * quantity
    print(result)
    print(result)

calculate_total(100, 5)
"""


agent_output = run_agents(request, code)

final_analysis = aggregate_results(
    request,
    agent_output["results"]
)


print("\n================================")
print("SELECTED AGENTS")
print("================================")

print(agent_output["selected_agents"])


print("\n================================")
print("FINAL AGGREGATED ANALYSIS")
print("================================")

print(final_analysis)