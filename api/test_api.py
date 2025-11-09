#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test 1: Register a user
print("=" * 60)
print("TEST 1: Registering a test user...")
print("=" * 60)

import time
register_data = {
    "email": f"test{int(time.time())}@jerrygfit.com",
    "username": f"testuser{int(time.time())}",
    "password": "Test12345",
    "full_name": "Test User"
}

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
except Exception as e:
    print(f"Registration error: {e}")
    if hasattr(e, 'response'):
        print(f"Response: {e.response.text}")
    print()

# Test 2: Login with the user
print("=" * 60)
print("TEST 2: Logging in...")
print("=" * 60)

login_data = {
    "username": register_data["username"],
    "password": "Test12345"
}

try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_data,  # OAuth2PasswordRequestForm expects form data
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")

    if response.status_code == 200:
        access_token = result.get("access_token")
        print(f"\n✅ Login successful! Access token: {access_token[:50]}...")

        # Test 3: Get current user
        print("\n" + "=" * 60)
        print("TEST 3: Getting current user info...")
        print("=" * 60)

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Test 4: Get analytics
        print("\n" + "=" * 60)
        print("TEST 4: Getting analytics...")
        print("=" * 60)

        response = requests.get(f"{BASE_URL}/analytics", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Test 5: Get tasks
        print("\n" + "=" * 60)
        print("TEST 5: Getting tasks...")
        print("=" * 60)

        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Test 6: Create a task
        print("\n" + "=" * 60)
        print("TEST 6: Creating a task...")
        print("=" * 60)

        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "TODO",
            "priority": "MEDIUM"
        }

        response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Test 7: Get projects
        print("\n" + "=" * 60)
        print("TEST 7: Getting projects...")
        print("=" * 60)

        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 60)

except Exception as e:
    print(f"Login error: {e}")
    if hasattr(e, 'response'):
        print(f"Response: {e.response.text}")
