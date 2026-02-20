import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register():
    print("Testing registration with detailed output...")
    url = f"{BASE_URL}/auth/register"
    data = {
        "username": "testuser",
        "password": "test123",
        "role": "user"
    }
    
    try:
        print(f"POST {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Response: {response.text}")
        
        if response.status_code != 201:
            print(f"Error details: {response.status_code}")
            try:
                error_json = response.json()
                print(f"Error JSON: {json.dumps(error_json, indent=2)}")
            except:
                pass
        return response.status_code == 201
    except Exception as e:
        print(f"Exception: {e}")
        return False

def test_login():
    print("\nTesting login with detailed output...")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        print(f"POST {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        response = requests.post(url, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            print(f"Error details: {response.status_code}")
            try:
                error_json = response.json()
                print(f"Error JSON: {json.dumps(error_json, indent=2)}")
            except:
                pass
        return response.status_code == 200
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing API endpoints with detailed output")
    print("=" * 60)
    
    register_success = test_register()
    login_success = test_login()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"Register: {'SUCCESS' if register_success else 'FAILED'}")
    print(f"Login: {'SUCCESS' if login_success else 'FAILED'}")
    print("=" * 60)
