#!/usr/bin/env python3
"""
Test script for Student Performance Prediction API
Run this after starting your FastAPI server to test the endpoints
"""

import requests
import json
from typing import Dict, Any

# API base URL (adjust if running on different host/port)
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints with sample data."""
    
    print("🧪 Testing Student Performance Prediction API")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1️⃣  Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Health check
    print("\n2️⃣  Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Model info
    print("\n3️⃣  Testing model info...")
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            model_info = response.json()
            print(f"   Model Type: {model_info.get('model_type')}")
            print(f"   Features Count: {model_info.get('features_count')}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Prediction with valid data (low-income student)
    print("\n4️⃣  Testing prediction with low-income student data...")
    low_income_student = {
        "hours_studied": 4.0,
        "attendance": 75.0,
        "parental_involvement": "Low",
        "access_to_resources": "Low",
        "sleep_hours": 6.5,
        "previous_scores": 65.0,
        "tutoring_sessions": 0.5,
        "family_income": "Low",
        "parental_education_level": "High School",
        "internet_access": "No",
        "physical_activity": 1.5
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=low_income_student,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   📊 Predicted Score: {result['predicted_score']}")
            print(f"   📈 Performance Level: {result['performance_level']}")
            print(f"   💡 Recommendations: {len(result['recommendations'])} items")
            print(f"   ⚠️  Risk Factors: {len(result['equity_risk_factors'])} items")
            print(f"   🎯 Support Needed: {result['mission_insights']['support_needed']}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Prediction with privileged student data
    print("\n5️⃣  Testing prediction with privileged student data...")
    privileged_student = {
        "hours_studied": 8.0,
        "attendance": 95.0,
        "parental_involvement": "High",
        "access_to_resources": "High",
        "sleep_hours": 8.0,
        "previous_scores": 85.0,
        "tutoring_sessions": 3.0,
        "family_income": "High",
        "parental_education_level": "Postgraduate",
        "internet_access": "Yes",
        "physical_activity": 4.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=privileged_student,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   📊 Predicted Score: {result['predicted_score']}")
            print(f"   📈 Performance Level: {result['performance_level']}")
            print(f"   💡 Recommendations: {len(result['recommendations'])} items")
            print(f"   ⚠️  Risk Factors: {len(result['equity_risk_factors'])} items")
            print(f"   🎯 Support Needed: {result['mission_insights']['support_needed']}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Invalid data (should trigger validation errors)
    print("\n6️⃣  Testing with invalid data (should fail)...")
    invalid_data = {
        "hours_studied": -5.0,  # Invalid: negative
        "attendance": 150.0,    # Invalid: > 100
        "parental_involvement": "Invalid",  # Invalid: not in allowed values
        "access_to_resources": "Low",
        "sleep_hours": 8.0,
        "previous_scores": 85.0,
        "tutoring_sessions": 3.0,
        "family_income": "Medium",
        "parental_education_level": "College",
        "internet_access": "Yes",
        "physical_activity": 4.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 422:
            print("   ✅ Validation working correctly - rejected invalid data")
            error_response = response.json()
            print(f"   Error details: {len(error_response.get('detail', []))} validation errors")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎯 Testing completed!")

def test_data_type_constraints():
    """Test data type and range constraints."""
    print("\n🔢 Testing Data Type and Range Constraints")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "Hours studied too high",
            "data": {"hours_studied": 25.0},  # Max is 20
            "should_fail": True
        },
        {
            "name": "Attendance negative",
            "data": {"attendance": -10.0},  # Min is 0
            "should_fail": True
        },
        {
            "name": "Sleep hours too low",
            "data": {"sleep_hours": 1.0},  # Min is 3
            "should_fail": True
        },
        {
            "name": "Invalid parental involvement",
            "data": {"parental_involvement": "Very High"},
            "should_fail": True
        }
    ]
    
    base_valid_data = {
        "hours_studied": 6.0,
        "attendance": 85.0,
        "parental_involvement": "Medium",
        "access_to_resources": "Medium",
        "sleep_hours": 7.0,
        "previous_scores": 75.0,
        "tutoring_sessions": 2.0,
        "family_income": "Medium",
        "parental_education_level": "College",
        "internet_access": "Yes",
        "physical_activity": 3.0
    }
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣  Testing: {test_case['name']}")
        
        # Create test data by updating base data
        test_data = base_valid_data.copy()
        test_data.update(test_case['data'])
        
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if test_case['should_fail']:
                if response.status_code == 422:
                    print("   ✅ Correctly rejected invalid data")
                else:
                    print(f"   ❌ Should have failed but got status: {response.status_code}")
            else:
                if response.status_code == 200:
                    print("   ✅ Correctly accepted valid data")
                else:
                    print(f"   ❌ Should have succeeded but got status: {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting API Tests")
    print("💡 Make sure your FastAPI server is running on http://localhost:8000")
    print("   Run: uvicorn prediction:app --reload")
    print()
    
    # Run the tests
    test_api_endpoints()
    test_data_type_constraints()
    
    print("\n✅ All tests completed!")
    print("🌐 You can also test manually at: http://localhost:8000/docs")