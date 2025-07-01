import sys
import os

print(f"DEBUG: Starting run_task_translate.py. CWD: {os.getcwd()}")
sys.stdout.flush()

try:
    print("DEBUG: Attempting to import DeepAgent...")
    sys.stdout.flush()
    from deepagent.main import DeepAgent
    print("DEBUG: Successfully imported DeepAgent.")
    sys.stdout.flush()

    print("DEBUG: Attempting to instantiate DeepAgent...")
    sys.stdout.flush()
    agent = DeepAgent()
    print("DEBUG: DeepAgent instantiated.")
    sys.stdout.flush()

    print("DEBUG: Running example: Translate 'Hello' to Spanish")
    sys.stdout.flush()
    agent.run_task("translate Hello to Spanish")

    print("\nDEBUG: Running example: List files")
    sys.stdout.flush()
    agent.run_task("ls -F")

except ImportError as e:
    print(f"ERROR: ImportError: {e}")
    sys.stdout.flush()
except Exception as e:
    print(f"ERROR: An unexpected error occurred: {e}")
    sys.stdout.flush()

print("DEBUG: End of run_task_translate.py.")
sys.stdout.flush()
