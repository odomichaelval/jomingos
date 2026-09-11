#!/usr/bin/env python
"""
Jomingos API DISCOVERY TOOL
Run this to find all your Django REST Framework endpoints
This will help build the correct React frontend
"""

import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("🔍 Jomingos API DISCOVERY TOOL")
print("=" * 70)

# Step 1: Check if Django server is running
print("\n[1️⃣] Checking if Django server is running...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"   ✅ Server is running! (Status: {response.status_code})")
except requests.ConnectionError:
    print("   ❌ Server is NOT running!")
    print("\n   Please start your Django server first:")
    print("   ┌─────────────────────────────────────────┐")
    print("   │  python manage.py runserver            │")
    print("   └─────────────────────────────────────────┘")
    exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Step 2: Discover API endpoints
print("\n[2️⃣] Discovering API endpoints...")

# Common Django REST Framework endpoint patterns
endpoints_to_try = [
    # Root endpoints
    ("/api/", "API Root"),
    ("/api-auth/", "API Auth"),
    
    # Authentication endpoints
    ("/api/accounts/", "Accounts List"),
    ("/api/accounts/login/", "Login"),
    ("/api/accounts/logout/", "Logout"),
    ("/api/accounts/register/", "Register"),
    ("/api/accounts/me/", "Current User"),
    ("/api/accounts/change-password/", "Change Password"),
    ("/api/accounts/refresh/", "Token Refresh"),
    ("/api/token/", "JWT Token"),
    ("/api/token/refresh/", "JWT Refresh"),
    
    # App endpoints
    ("/api/patients/", "Patients List"),
    ("/api/patients/?page=1", "Patients Paginated"),
    ("/api/care-notes/", "Care Notes"),
    ("/api/medications/", "Medications"),
    ("/api/vitals/", "Vital Signs"),
    ("/api/tasks/", "Tasks"),
    ("/api/family/", "Family Members"),
    ("/api/dashboard/", "Dashboard"),
    ("/api/dashboard/stats/", "Dashboard Stats"),
    
    # Documentation
    ("/swagger/", "Swagger UI"),
    ("/swagger/?format=openapi", "OpenAPI Spec"),
    ("/redoc/", "ReDoc"),
]

print("\n   Testing endpoints...")
working_endpoints = []

for endpoint, description in endpoints_to_try:
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=3)
        if response.status_code != 404:
            working_endpoints.append({
                "url": endpoint,
                "status": response.status_code,
                "description": description,
                "sample_data": response.text[:200] if response.text else "Empty"
            })
            print(f"   ✅ FOUND: {endpoint} (Status: {response.status_code})")
        else:
            print(f"   ❌ Not found: {endpoint}")
    except requests.Timeout:
        print(f"   ⏱️ Timeout: {endpoint}")
    except Exception as e:
        print(f"   ⚠️ Error: {endpoint} - {str(e)[:50]}")

# Step 3: Check authentication by trying to register a test user
print("\n[3️⃣] Testing authentication flow...")

test_user = {
    "username": "test_Jomingos_user",
    "email": "test@Jomingos.com",
    "password": "TestPassword123!",
    "password2": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

# Try different registration endpoints
register_endpoints = [
    "/api/accounts/register/",
    "/api/register/",
    "/api/auth/register/",
]

for reg_endpoint in register_endpoints:
    try:
        response = requests.post(f"{BASE_URL}{reg_endpoint}", json=test_user, timeout=5)
        if response.status_code in [200, 201]:
            print(f"   ✅ Registration works at: {reg_endpoint}")
            print(f"   Response: {json.dumps(response.json(), indent=2)[:300]}")
            break
        elif response.status_code == 400:
            print(f"   ⚠️ Registration endpoint exists at {reg_endpoint} but validation failed")
            print(f"   Response: {response.text[:200]}")
    except:
        pass

# Step 4: Save results
print("\n[4️⃣] Saving discovery results...")

results = {
    "timestamp": __import__('datetime').datetime.now().isoformat(),
    "base_url": BASE_URL,
    "working_endpoints": working_endpoints,
    "total_found": len(working_endpoints)
}

with open("api_discovery_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"   ✅ Results saved to: api_discovery_results.json")

# Step 5: Summary
print("\n" + "=" * 70)
print("📊 DISCOVERY SUMMARY")
print("=" * 70)
print(f"   ✅ Working endpoints found: {len(working_endpoints)}")
print("\n   Working endpoints list:")
for ep in working_endpoints:
    print(f"   • {ep['url']} → {ep['description']}")

print("\n" + "=" * 70)
print("🎯 NEXT STEPS")
print("=" * 70)
print("""
1. Copy the output above and share it with me
2. I will adjust the React frontend to match your exact API
3. Then we'll build the complete Jomingos Healthcare Dashboard

Your React frontend will be created in the 'Jomingos-react' folder.
""")
print("=" * 70)