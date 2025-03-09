#!/usr/bin/env python3
"""
BurnAI API Test Script

This script tests the BurnAI API endpoints to ensure they are working correctly.
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def test_root_endpoint():
    """Test the root endpoint."""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_health_endpoint():
    """Test the health endpoint."""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_counties_endpoint():
    """Test the counties endpoint."""
    print("\n=== Testing Counties Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/api/counties")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        counties = response.json()
        print(f"Found {len(counties)} counties")
        if counties:
            print(f"First county: {json.dumps(counties[0], indent=2)}")
    else:
        print(f"Response: {response.text}")
    return response.status_code == 200

def test_county_detail_endpoint(county_id="sf"):
    """Test the county detail endpoint."""
    print(f"\n=== Testing County Detail Endpoint for {county_id} ===")
    response = requests.get(f"{API_BASE_URL}/api/counties/{county_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")
    return response.status_code == 200

def test_weather_endpoint(county_id="sf"):
    """Test the weather endpoint."""
    print(f"\n=== Testing Weather Endpoint for {county_id} ===")
    response = requests.get(f"{API_BASE_URL}/api/data/weather/{county_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")
    return response.status_code == 200

def test_assessment_endpoint(county_id="sf"):
    """Test the assessment endpoint."""
    print(f"\n=== Testing Assessment Endpoint for {county_id} ===")
    response = requests.get(f"{API_BASE_URL}/api/counties/{county_id}/assessment")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")
    return response.status_code == 200

def test_fire_points_endpoint(county_id="sf"):
    """Test the fire points endpoint."""
    print(f"\n=== Testing Fire Points Endpoint for {county_id} ===")
    response = requests.get(f"{API_BASE_URL}/api/data/fire-points/{county_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")
    return response.status_code == 200

def test_refresh_endpoint():
    """Test the refresh endpoint."""
    print("\n=== Testing Refresh Endpoint ===")
    response = requests.post(f"{API_BASE_URL}/api/data/refresh")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")
    return response.status_code == 200

def main():
    """Run all tests."""
    print("=== BurnAI API Test Script ===")
    print(f"API Base URL: {API_BASE_URL}")
    
    # Run tests
    tests = [
        test_root_endpoint,
        test_health_endpoint,
        test_counties_endpoint,
        test_county_detail_endpoint,
        test_weather_endpoint,
        test_assessment_endpoint,
        test_fire_points_endpoint,
        test_refresh_endpoint
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"Error: {str(e)}")
            results.append((test.__name__, False))
    
    # Print summary
    print("\n=== Test Summary ===")
    success_count = sum(1 for _, result in results if result)
    print(f"Passed: {success_count}/{len(results)}")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    # Return exit code based on success
    return 0 if success_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(main()) 