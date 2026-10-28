from app.agents.code_review_agent import check_code_quality


code = """
def x(a,b):
    print(a+b)
    print(a+b)

x(10,20)
"""


result = check_code_quality(code)

print("\n===== CODE QUALITY AGENT =====\n")
print(result)