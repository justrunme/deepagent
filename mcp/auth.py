import json
import os

AUTH_FILE = "credentials.json"

def get_auth_token(server_name: str):
    """Retrieves an authentication token for a given server. Prompts the user if not found."""
    credentials = {}
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            credentials = json.load(f)

    token = credentials.get(server_name)
    if not token:
        print(f"\nAuthorization required for {server_name}. (Normally, this would prompt the user for input.)")
        # For now, returning a dummy token to avoid blocking on input()
        token = "dummy_token_for_testing"
        credentials[server_name] = token
        with open(AUTH_FILE, "w") as f:
            json.dump(credentials, f, indent=2)
        print(f"Dummy token for {server_name} saved to {AUTH_FILE}.")
    return token

if __name__ == "__main__":
    # Example usage
    token = get_auth_token("shell-mcp")
    print(f"Retrieved token: {token}")

    # To test prompting again, delete credentials.json
    # if os.path.exists(AUTH_FILE):
    #     os.remove(AUTH_FILE)
    #     print(f"\n{AUTH_FILE} removed. Next call will prompt again.")
    # token = get_auth_token("shell-mcp")
    # print(f"Retrieved token: {token}")

