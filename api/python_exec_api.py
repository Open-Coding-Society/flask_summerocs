# /api/python_exec_api.py
from flask import Blueprint, request, jsonify
import subprocess, tempfile, os

python_exec_api = Blueprint('python_exec_api', __name__, url_prefix='/run')

@python_exec_api.route('/python', methods=['POST'])
def run_python():
    """
    Executes submitted Python code in a short-lived subprocess.
    Use only inside the Docker container for sandboxing.
    """
    data = request.get_json()
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"output": "⚠️ No code provided."}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode())
        tmp.flush()

        try:
            result = subprocess.run(
                ["python3", tmp.name],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "⏱️ Execution timed out (5 s limit)."
        except Exception as e:
            output = f"Error running code: {str(e)}"
        finally:
            os.unlink(tmp.name)

    return jsonify({"output": output})
