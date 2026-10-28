import os

from app.agents.debugging_agent import debug_code
from app.agents.code_review_agent import check_code_quality
from app.agents.optimization_agent import optimize_code
from app.agents.documentation_agent import generate_documentation
from app.agents.test_case_agent import generate_test_cases
from app.agents.complex_agent import analyze_complex_code
from app.agents.security_agent import analyze_security

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agents.coordinator import run_agents
from app.services.aggregator import aggregate_results
from app.services.report_generator import generate_report

from app.services.code_executor import execute_code as run_code
from app.services.test_runner import run_pytest

app = FastAPI(
    title="DevAssist API",
    description="AI-Powered Multi-Agent Software Development Platform",
    version="2.0"
)


# Serve frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")


class CodeRequest(BaseModel):
    request: str
    code: str
    execution_error: str = ""
    requirement: str = ""


class ExecuteRequest(BaseModel):
    language: str
    code: str


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/analyze")
def analyze_code(data: CodeRequest):
    agent_output = run_agents(
    data.request,
    data.code,
    data.execution_error,
    data.requirement
)

    analysis = aggregate_results(
        data.request,
        agent_output["results"]
    )

    report = generate_report(
        data.request,
        analysis
    )

    return {
        "selected_agents": agent_output["selected_agents"],
        "agent_results": agent_output["results"],
        "aggregated_analysis": analysis,
        "report": report
    }


@app.post("/analyze/agent")
def analyze_single_agent(data: CodeRequest):

    agent = data.request.upper()

    if agent == "DEBUG":
        result = debug_code(
            data.code,
            data.execution_error
        )

    elif agent == "CODE_REVIEW":
        result = check_code_quality(data.code)

    elif agent == "OPTIMIZATION":
        result = optimize_code(data.code)

    elif agent == "DOCUMENTATION":
        result = generate_documentation(data.code)

    elif agent == "TEST_CASE":
        result = generate_test_cases(
        data.code,
        data.requirement
    )
    elif agent == "SECURITY":
        result = analyze_security(data.code)

    elif agent == "COMPLEX":
        result = analyze_complex_code(data.code)

    else:
        return {
            "success": False,
            "error": "Unknown AI agent."
        }

    return {
        "success": True,
        "agent": agent,
        "result": result
    }


@app.post("/execute")
def execute_code(data: ExecuteRequest):

    result = run_code(
    data.language,
    data.code
)

    return result

@app.post("/test")
def run_tests(data: dict):

    source_code = data.get("source_code", "")
    test_code = data.get("test_code", "")

    if not source_code.strip():
        return {
            "success": False,
            "error": "No source code provided."
        }

    if not test_code.strip():
        return {
            "success": False,
            "error": "No test code provided."
        }

    result = run_pytest(
        source_code,
        test_code
    )

    return result

@app.post("/test/analyze-failure")
def analyze_test_failure(data: dict):

    source_code = data.get("source_code", "")
    test_output = data.get("test_output", "")
    test_error = data.get("test_error", "")

    if not source_code.strip():
        return {
            "success": False,
            "error": "No source code provided."
        }

    if not test_output.strip() and not test_error.strip():
        return {
            "success": False,
            "error": "No test failure information provided."
        }

    failure_details = (
        "PYTEST OUTPUT:\n\n"
        + test_output
        + "\n\n"
        + "PYTEST ERROR:\n\n"
        + test_error
    )

    result = debug_code(
        source_code,
        failure_details
    )

    return {
        "success": True,
        "agent": "DEBUG",
        "result": result
    }


@app.get("/project/files")
def get_project_files():

    project_path = "workspace"

    os.makedirs(project_path, exist_ok=True)

    files = []

    for file_name in os.listdir(project_path):

        full_path = os.path.join(
            project_path,
            file_name
        )

        if os.path.isfile(full_path):

            files.append(file_name)

    return {
        "files": files
    }


@app.get("/project/file/{file_name}")
def get_project_file(file_name: str):

    project_path = "workspace"

    file_path = os.path.join(
        project_path,
        file_name
    )

    if not os.path.exists(file_path):

        return {
            "success": False,
            "error": "File not found."
        }

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        code = file.read()

    return {
        "success": True,
        "file": file_name,
        "code": code
    }


@app.post("/project/file")
def save_project_file(data: dict):

    project_path = "workspace"

    os.makedirs(
        project_path,
        exist_ok=True
    )

    file_name = data.get("file")
    code = data.get("code", "")

    if not file_name:

        return {
            "success": False,
            "error": "File name is required."
        }

    file_path = os.path.join(
        project_path,
        file_name
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(code)

    return {
        "success": True,
        "file": file_name
    }


@app.delete("/project/file/{file_name}")
def delete_project_file(file_name: str):
    project_path = "workspace"
    file_path = os.path.join(project_path, file_name)

    if not os.path.exists(file_path):
        return {"success": False, "error": "File not found."}

    os.remove(file_path)

    return {
        "success": True,
        "message": f"{file_name} deleted successfully."
    }


@app.put("/project/file/{file_name}")
def rename_project_file(file_name: str, data: dict):
    project_path = "workspace"

    new_name = data.get("new_name")

    if not new_name:
        return {
            "success": False,
            "error": "New file name is required."
        }

    old_path = os.path.join(project_path, file_name)
    new_path = os.path.join(project_path, new_name)

    if not os.path.exists(old_path):
        return {
            "success": False,
            "error": "File not found."
        }

    if os.path.exists(new_path):
        return {
            "success": False,
            "error": "A file with that name already exists."
        }

    os.rename(old_path, new_path)

    return {
        "success": True,
        "old_name": file_name,
        "new_name": new_name
    }