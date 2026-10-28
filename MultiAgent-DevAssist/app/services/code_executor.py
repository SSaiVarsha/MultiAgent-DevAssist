import subprocess
import tempfile
import os


def execute_code(language: str, code: str):

    language = language.lower().strip()

    if language == "python":
        return execute_python(code)

    elif language == "java":
        return execute_java(code)

    elif language == "cpp":
        return execute_cpp(code)

    elif language == "javascript":
        return execute_javascript(code)

    return {
        "success": False,
        "output": "",
        "error": f"{language} execution is not implemented yet."
    }


def execute_python(code: str):

    temp_file = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(code)
            temp_file = file.name

        process = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": process.returncode == 0,
            "output": process.stdout,
            "error": process.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": "Execution stopped: time limit exceeded."
        }

    except Exception as error:

        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def execute_java(code: str):

    temp_dir = None

    try:

        temp_dir = tempfile.mkdtemp(
            prefix="devassist_java_"
        )

        java_file = os.path.join(
            temp_dir,
            "Main.java"
        )

        with open(
            java_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(code)

        compile_process = subprocess.run(
            [
                "javac",
                java_file
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if compile_process.returncode != 0:

            return {
                "success": False,
                "output": compile_process.stdout,
                "error": compile_process.stderr
            }

        run_process = subprocess.run(
            [
                "java",
                "-cp",
                temp_dir,
                "Main"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": run_process.returncode == 0,
            "output": run_process.stdout,
            "error": run_process.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": "Execution stopped: time limit exceeded."
        }

    except Exception as error:

        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:

        if temp_dir and os.path.exists(temp_dir):

            for root, dirs, files in os.walk(
                temp_dir,
                topdown=False
            ):

                for name in files:
                    try:
                        os.remove(
                            os.path.join(root, name)
                        )
                    except:
                        pass

                for name in dirs:
                    try:
                        os.rmdir(
                            os.path.join(root, name)
                        )
                    except:
                        pass

            try:
                os.rmdir(temp_dir)
            except:
                pass


def execute_cpp(code: str):

    temp_dir = None

    try:

        temp_dir = tempfile.mkdtemp(
            prefix="devassist_cpp_"
        )

        cpp_file = os.path.join(
            temp_dir,
            "main.cpp"
        )

        executable = os.path.join(
            temp_dir,
            "main.exe"
        )

        with open(
            cpp_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(code)

        # MSYS2 UCRT64 compiler
        gpp_path = r"E:\msys64\ucrt64\bin\g++.exe"

        # Give the compiler access to its UCRT64 tools and libraries
        environment = os.environ.copy()

        environment["PATH"] = (
            r"E:\msys64\ucrt64\bin;"
            + environment.get("PATH", "")
        )

        compile_process = subprocess.run(
            [
                gpp_path,
                cpp_file,
                "-o",
                executable
            ],
            capture_output=True,
            text=True,
            timeout=10,
            env=environment
        )

        if compile_process.returncode != 0:

            return {
                "success": False,
                "output": compile_process.stdout,
                "error": compile_process.stderr
            }

        # Run the generated Windows executable
        run_environment = environment.copy()

        run_process = subprocess.run(
            [
                executable
            ],
            capture_output=True,
            text=True,
            timeout=10,
            env=run_environment
        )

        return {
            "success": run_process.returncode == 0,
            "output": run_process.stdout,
            "error": run_process.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": "Execution stopped: time limit exceeded."
        }

    except Exception as error:

        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:

        if temp_dir and os.path.exists(temp_dir):

            for root, dirs, files in os.walk(
                temp_dir,
                topdown=False
            ):

                for name in files:
                    try:
                        os.remove(
                            os.path.join(root, name)
                        )
                    except:
                        pass

                for name in dirs:
                    try:
                        os.rmdir(
                            os.path.join(root, name)
                        )
                    except:
                        pass

            try:
                os.rmdir(temp_dir)
            except:
                pass


def execute_javascript(code: str):

    temp_file = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".js",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(code)
            temp_file = file.name

        process = subprocess.run(
            [
                "node",
                temp_file
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": process.returncode == 0,
            "output": process.stdout,
            "error": process.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": "Execution stopped: time limit exceeded."
        }

    except Exception as error:

        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)