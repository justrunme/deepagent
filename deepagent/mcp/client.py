import requests
import json

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_capabilities(self):
        try:
            response = requests.get(f"{self.base_url}/capabilities")
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching capabilities from {self.base_url}: {e}")
            return None

    def execute(self, command: str, auth_token: str = None):
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        try:
            response = requests.post(f"{self.base_url}/execute", json={"command": command}, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error executing command on {self.base_url}: {e}")
            return None

if __name__ == "__main__":
    # Example Usage (for testing purposes)
    # You would typically run mcp_server.py in a separate terminal
    # uvicorn mcp_server:app --reload --port 8000
    
    # Test with a local server
    client = MCPClient("http://localhost:8000")

    print("--- Testing Capabilities ---")
    capabilities = client.get_capabilities()
    if capabilities:
        print(json.dumps(capabilities, indent=2))

    print("\n--- Testing Execution (Unauthorized) ---")
    unauthorized_result = client.execute("echo Hello")
    if unauthorized_result:
        print(json.dumps(unauthorized_result, indent=2))

    print("\n--- Testing Execution (Authorized) ---")
    # In a real scenario, you'd get this token from an auth process
    # For this example, any non-empty string will work with our simple mcp_server.py
    authorized_result = client.execute("ls -l", auth_token="dummy_token_123")
    if authorized_result:
        print(json.dumps(authorized_result, indent=2))
