import requests

class HTTPExecutor:
    def execute_request(self, method: str, url: str, headers: dict = None, data: dict = None):
        # This is a placeholder. In a real scenario, this would make actual HTTP requests.
        print(f"[HTTPExecutor] Executing {method} request to {url}")
        print(f"Headers: {headers}")
        print(f"Data: {data}")
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                return {"status": "error", "message": f"Unsupported HTTP method: {method}"}
            
            response.raise_for_status()
            return {"status": "success", "output": response.json()}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"HTTP request failed: {e}"}

if __name__ == "__main__":
    executor = HTTPExecutor()
    # Example GET
    result_get = executor.execute_request("GET", "https://jsonplaceholder.typicode.com/todos/1")
    print(result_get)

    # Example POST
    result_post = executor.execute_request("POST", "https://jsonplaceholder.typicode.com/posts", 
                                         data={"title": "foo", "body": "bar", "userId": 1})
    print(result_post)