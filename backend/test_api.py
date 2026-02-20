import requests

BASE_URL = "http://localhost:8000/api"

def test_register():
    print("Testing registration...")
    url = f"{BASE_URL}/auth/register"
    data = {
        "username": "testuser",
        "password": "test123",
        "role": "user"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    print("\nTesting login...")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing API endpoints")
    print("=" * 50)
    
    register_success = test_register()
    login_success = test_login()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Register: {'SUCCESS' if register_success else 'FAILED'}")
    print(f"Login: {'SUCCESS' if login_success else 'FAILED'}")
    print("=" * 50)
