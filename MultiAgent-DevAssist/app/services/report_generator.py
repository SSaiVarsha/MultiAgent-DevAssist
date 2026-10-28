from app.services.ollama_service import ask_ollama


def generate_report(request: str, analysis: str) -> str:

    prompt = f"""
You are the Report Generator of DevAssist.

Create a professional software analysis report from the
aggregated analysis below.

USER REQUEST:
{request}

AGGREGATED ANALYSIS:
{analysis}

IMPORTANT RULES:

1. Do NOT invent issues.

2. Do NOT upgrade potential issues into confirmed bugs.

3. Do NOT treat missing validation or error handling as a bug
unless the analysis provides clear evidence that it causes a
real problem in the given code.

4. Preserve the distinction between:
- Confirmed Issues
- Potential Issues
- Optional Improvements

5. Only confirmed issues should receive a priority.

6. If there are no confirmed issues, write:
"None identified."

7. Do not repeat the same issue.

8. Keep the report based only on the supplied analysis.

IMPORTANT QUALITY RULES:

1. Only mention facts directly supported by the agent analysis.

2. Do not add generic security statements.

3. Do not recommend error handling unless an actual
   error-handling problem was identified.

4. Do not recommend input validation unless the code or
   analysis shows that it is relevant.

5. Do not add generic coding advice unrelated to the user's request.

6. Do not repeat the same issue as a recommendation.

7. If a confirmed syntax or runtime error exists,
   focus the report on fixing that error.

8. Keep Optional Improvements empty when no relevant
   improvement was identified.

9. Positive Aspects must describe actual properties of
   the provided code, not generic programming advice.

10. The final recommendation must directly reflect the
    confirmed findings.

11. Do not create new issues that are not present in the
aggregated analysis.

12. Do not move confirmed issues into Potential Issues.

13. Do not turn confirmed issues into Optional Improvements.

14. Do not repeat a confirmed issue in another section.

15. If the aggregated analysis says there are no potential
issues, write exactly:
None identified.

16. If the aggregated analysis says there are no optional
improvements, write exactly:
None identified.

17. For a syntax error, runtime error, or compilation error,
focus the report on the actual error and its correction.

18. Do not add unrelated recommendations such as type hints,
security hardening, validation, documentation, or error handling
unless explicitly supported by the aggregated analysis.

Generate exactly this structure:

# DEVASSIST FINAL REPORT

## 1. Request
Briefly describe what the user requested.

## 2. Overall Assessment
Give a concise assessment of the code.

## 3. Confirmed Issues

### High Priority
List confirmed high-priority issues.

If none:
"None identified."

### Medium Priority
List confirmed medium-priority issues.

If none:
"None identified."

### Low Priority
List confirmed low-priority issues.

If none:
"None identified."

## 4. Potential Issues
List issues that may occur under specific conditions.

If none:
"None identified."

## 5. Optional Improvements
List improvements that are useful but are not confirmed bugs.

If none:
"None identified."

## 6. Positive Aspects
Mention what the code does well.

## 7. Recommended Actions
Give practical actions based on the findings.

## 8. Final Recommendation
Give a short conclusion.

Use simple professional language.
"""

    return ask_ollama(prompt)