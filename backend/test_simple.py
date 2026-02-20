import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register_simple():
    print("Testing registration with simple password...")
    url = f"{BASE_URL}/auth/register"
    data = {
        "username": "testuser",
        "password": "123",
        "role": "user"
    }
    
    try:
        print(f"POST {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("SUCCESS!")
            return True
        else:
            print("FAILED!")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    test_register_simple()
