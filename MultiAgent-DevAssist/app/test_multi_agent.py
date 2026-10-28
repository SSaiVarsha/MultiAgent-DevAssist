from agents.coordinator import run_agents


request = "Find bugs in this code and improve its quality."

code = """
def calculate_total(price, quantity):
    result = price * quantity
    print(result)
    print(result)

calculate_total(100, 5)
"""


result = run_agents(request, code)


print("\n================================")
print("SELECTED AGENTS")
print("================================")

print(result["selected_agents"])


print("\n================================")
print("AGENT RESULTS")
print("================================")


for agent, output in result["results"].items():
    print(f"\n===== {agent} =====\n")
    print(output)