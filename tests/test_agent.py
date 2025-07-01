import pytest
from deepagent.main import DeepAgent

# Assuming mcp_server.py is running at http://localhost:8000
# For a proper integration test, you would typically start and stop the mock server
# within the test suite using pytest fixtures or similar.

def test_discover_and_execute():
    agent = DeepAgent()
    # The mock server does not require auth, so get_auth_token will return a dummy token
    # and the execute call should succeed.
    result = agent.run_task("echo Hello")
    assert "Executed: echo Hello" in result.get("result", "")

def test_translate_command():
    agent = DeepAgent()
    result = agent.run_task("translate This is a test")
    assert "Executed: translate This is a test" in result.get("result", "")
