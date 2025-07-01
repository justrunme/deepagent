import json
import sys
import os

print("DEBUG: Starting deepagent/main.py execution.")
sys.stdout.flush()

from deepagent.mcp.discovery import MCPDiscovery
from deepagent.mcp.client import MCPClient
from deepagent.mcp.auth import get_auth_token

MEMORY_FILE = os.environ.get("DEEPAGENT_MEMORY", os.path.join(os.path.dirname(__file__), 'mcp', 'memory.json'))

print("DeepAgent main.py loaded")
sys.stdout.flush()

class DeepAgent:
    def __init__(self):
        print("DeepAgent initialized")
        sys.stdout.flush()
        self.discovery = MCPDiscovery()
        self.mcp_clients = {}
        self.mcp_capabilities_cache = self._load_memory()

    def _load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: {MEMORY_FILE} is corrupted. Starting with empty memory.")
                    return {}
        return {}

    def _save_memory(self):
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.mcp_capabilities_cache, f, indent=2)

    def _get_mcp_client(self, base_url: str):
        if base_url not in self.mcp_clients:
            self.mcp_clients[base_url] = MCPClient(base_url)
        return self.mcp_clients[base_url]

    def _discover_and_cache_capabilities(self):
        print("Discovering MCP servers...")
        sys.stdout.flush()
        server_urls = self.discovery.discover_servers()
        print(f"Discovered URLs: {server_urls}")
        sys.stdout.flush()
        for url in server_urls:
            client = self._get_mcp_client(url)
            capabilities = client.get_capabilities()
            if capabilities:
                self.mcp_capabilities_cache[url] = capabilities
                print(f"Cached capabilities for {url}: {capabilities.get('name')}")
                sys.stdout.flush()
            else:
                print(f"Failed to get capabilities from {url}")
                sys.stdout.flush()
        self._save_memory() # Save after discovery

    def run_task(self, task_description: str):
        print(f"\nDeepAgent received task: '{task_description}'")
        sys.stdout.flush()

        if not self.mcp_capabilities_cache:
            self._discover_and_cache_capabilities()
            if not self.mcp_capabilities_cache:
                print("No MCP servers discovered or no capabilities found. Cannot perform task.")
                sys.stdout.flush()
                return None # Return None if no servers found

        # Simple task parsing: assume task_description is a command for now
        command_to_execute = task_description.split()[0] # e.g., "translate" from "translate 'hello'"

        found_server = None
        server_url = None

        # Find a suitable MCP server based on capabilities
        for url, capabilities in self.mcp_capabilities_cache.items():
            if command_to_execute in capabilities.get("commands", []):
                found_server = capabilities.get("name")
                server_url = url
                print(f"Found suitable MCP server: {found_server} at {server_url}")
                sys.stdout.flush()
                break
        
        if not found_server:
            print(f"No MCP server found that can handle command: '{command_to_execute}'")
            sys.stdout.flush()
            return None # Return None if no suitable server found

        client = self._get_mcp_client(server_url)
        auth_token = None

        if self.mcp_capabilities_cache[server_url].get("requires_auth"):
            print(f"Server {found_server} requires authentication.")
            sys.stdout.flush()
            auth_token = get_auth_token(found_server)
            if not auth_token:
                print("Authentication failed or token not provided. Cannot execute command.")
                sys.stdout.flush()
                return None # Return None if authentication fails

        print(f"Executing command '{task_description}' on {found_server}...")
        sys.stdout.flush()
        result = client.execute(task_description, auth_token)

        if result:
            print("Task execution result:")
            sys.stdout.flush()
            print(json.dumps(result, indent=2))
            sys.stdout.flush()
            return result # <--- ADDED THIS RETURN STATEMENT
        else:
            print("Task execution failed.")
            sys.stdout.flush()
            return None # Return None on execution failure

if __name__ == "__main__":
    agent = DeepAgent()
    # Example task
    agent.run_task("echo Hello from DeepAgent")
    agent.run_task("ls -la")
    agent.run_task("translate 'Bonjour' to English")