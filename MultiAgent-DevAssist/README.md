# MultiAgent-DevAssist

## An AI-Powered Software Engineering Assistant

DevAssist is a web-based software engineering assistant that integrates specialized AI agents to help developers analyze code, identify bugs, review code quality, optimize performance, generate documentation, create test cases, and detect potential security vulnerabilities.

## Features

- **Debugging Agent:** Identifies errors and suggests corrections.
- **Code Review Agent:** Reviews readability and maintainability.
- **Optimization Agent:** Recommends performance improvements.
- **Documentation Agent:** Generates code documentation.
- **Test Case Agent:** Generates Python tests using Pytest.
- **Security Agent:** Identifies potential security vulnerabilities.
- **Complex Analysis Agent:** Performs comprehensive code analysis.
- **Code Execution:** Supports configured Python, Java, C++, and JavaScript execution.
- **Automated Failure Analysis:** Analyzes test failures and suggests corrections.
- **Local AI:** Uses Ollama with the Qwen2.5-Coder model.

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- AI: Ollama, Qwen2.5-Coder
- Testing: Pytest
- Development: Visual Studio Code

## Project Structure

```text
MultiAgent-DevAssist/
├── app/
│   ├── agents/
│   ├── services/
│   └── main.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .gitignore
├── README.md
└── requirements.txt
```

## Prerequisites

- Python
- Git
- Ollama
- A compatible compiler or runtime for the programming languages you want to execute

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SSaiVarsha/MultiAgent-DevAssist.git
cd MultiAgent-DevAssist
```


### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and configure Ollama

Install Ollama separately, then download the model:

```bash
ollama pull qwen2.5-coder:7b
```

Start Ollama if it is not already running:

```bash
ollama.exe serve
```

### 5. Start DevAssist

From the project root, run:

```bash
uvicorn app.main:app --reload
```

Open the application at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Security Notice

AI-generated code and security recommendations must be reviewed before use. Do not execute untrusted code without appropriate isolation and restrictions.

## Academic Information

**Course:** SWE3004 — Software Design and Development Project  
**Semester:** Fall Semester 2026–2027  
**Institution:** Vellore Institute of Technology

