import pytest
import os
import json
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

TEST_MEMORY_FILE = "deepagent/mcp/test_memory.json"

def test_persistent_memory(monkeypatch):
    # Ensure the test memory file is clean before starting
    if os.path.exists(TEST_MEMORY_FILE):
        os.remove(TEST_MEMORY_FILE)

    # Set the environment variable for this test using monkeypatch
    monkeypatch.setenv("DEEPAGENT_MEMORY", TEST_MEMORY_FILE)

    # First run: discover and save capabilities
    agent1 = DeepAgent()
    agent1.run_task("echo Initial run")

    assert os.path.exists(TEST_MEMORY_FILE)
    with open(TEST_MEMORY_FILE, 'r') as f:
        data = json.load(f)
        assert "http://localhost:8000" in data
        assert "mock-mcp" == data["http://localhost:8000"]["name"]

    # Second run: memory should be loaded, no new discovery
    agent2 = DeepAgent()
    # We can't directly assert that _discover_and_cache_capabilities wasn't called
    # but we can check if the cache is populated from the file
    assert "http://localhost:8000" in agent2.mcp_capabilities_cache

    # Clean up the test memory file
    os.remove(TEST_MEMORY_FILE)
    # monkeypatch.delenv("DEEPAGENT_MEMORY") # monkeypatch automatically cleans up env vars
