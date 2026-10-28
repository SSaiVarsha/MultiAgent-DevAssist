import os
import sys
import subprocess
import tempfile


def run_pytest(source_code: str, test_code: str):
    """
    Run generated pytest code against the user's source code.
    """

    temp_dir = tempfile.mkdtemp(
        prefix="devassist_tests_"
    )

    source_file = os.path.join(
        temp_dir,
        "main_under_test.py"
    )

    test_file = os.path.join(
        temp_dir,
        "test_generated.py"
    )

    try:

        # Save user's actual source code
        with open(
            source_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(source_code)

        # Save AI-generated tests
        with open(
            test_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(
    "import pytest\n"
    "from main_under_test import *\n\n" +
    test_code
)

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                test_file,
                "-v"
            ],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": "Test execution timed out after 30 seconds.",
            "return_code": -1
        }

    except Exception as e:

        return {
            "success": False,
            "output": "",
            "error": str(e),
            "return_code": -1
        }

    finally:

        try:
            if os.path.exists(test_file):
                os.remove(test_file)

            if os.path.exists(source_file):
                os.remove(source_file)

            os.rmdir(temp_dir)

        except Exception:
            pass