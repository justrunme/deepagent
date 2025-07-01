# DeepAgent: Autonomous Agents and Tool Discovery with MCP

[![DeepAgent CI](https://github.com/justrunme/deepagent/actions/workflows/test.yml/badge.svg)](https://github.com/justrunme/deepagent/actions/workflows/test.yml)

This project demonstrates how an autonomous agent (DeepAgent) can discover, connect to, and utilize Machine-Centric Protocol (MCP) servers to execute tasks. It focuses on authorization, memory, and dynamic action based on discovered capabilities.

## Concept: DeepAgent + MCP Discovery & Authorization

The core idea is to showcase an autonomous agent that can:
1. Receive tasks from a user.
2. Independently find suitable tools (MCP Servers).
3. Connect to these servers.
4. Execute actions (if authorized).
5. Remember server capabilities for future use.

## What is an MCP Server in this context?

An MCP Server is a remote tool or service that provides an interface for executing actions (tools, APIs, CLI wrappers, etc.) via the Machine-Centric Protocol. Essentially, it's an endpoint with a description of its capabilities (e.g., `/capabilities`, `/execute`, `/auth`).

## Technological Implementation

### Architecture:

```
deepagent/
├── main.py                      # Core logic: accepts a task and executes the pipeline
├── mcp/
│   ├── discovery.py             # Discovers MCP servers on the network or from a registry
│   ├── client.py                # Universal MCP client (GET capabilities, POST execute)
│   ├── memory.json              # Cache of capabilities of known MCP servers
│   └── auth.py                  # Handles authorization (including user prompts)
├── tools/
│   ├── shell_wrapper.py         # Invokes commands if the MCP server is a shell tool
│   └── http_executor.py         # Wrapper for invoking external REST APIs
├── examples/
│   └── run_task_translate.py    # Example task: translate text using a discovered MCP
└── README.md                    # Project documentation and approach explanation
```

### MCP Server (Simple FastAPI Example):

A basic `mcp_server.py` is provided at the root of the project to simulate an MCP server. It exposes `/capabilities` and `/execute` endpoints, demonstrating how authorization can be required.

### Authorization Layer

A simple approach is implemented:
1. The MCP Server indicates `requires_auth: true` in its `/capabilities` response.
2. DeepAgent, based on this, prompts the user for `credentials.json` (or a token).
3. (Optional) Credentials can be stored securely.
4. When calling `/execute`, DeepAgent inserts an `Authorization: Bearer <token>` header.

### DeepAgent Features:

*   **Persistent Memory:** DeepAgent now remembers discovered MCP server capabilities and stores them in `memory.json` for future use.
*   **Re-selection:** Automatically re-selects suitable servers.
*   **Caching:** Caches successful calls.
*   **Auth Prompt:** Prompts the user for authorization on `401` errors.
*   **Reporting:** Reports on successful/failed execution.

## Testing

Comprehensive testing is implemented using `pytest` and `pytest-cov` for code coverage:
*   **Unit Tests:** For discovery, authentication, and execution logic.
*   **Integration Tests:** Running a mock MCP server (`tests/mock_mcp_server.py`) and testing end-to-end tasks.
*   **Code Coverage:** Measures test coverage and reports it to Codecov.
*   **Negative Cases:** Handling unauthorized access, unknown commands, timeouts.

## Future Ideas:

*   MCP server registry (centralized catalog of MCP endpoints)
*   UI for monitoring the agent
*   GPT-agent that generates tasks and uses MCP
