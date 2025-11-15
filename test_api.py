import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_categories():
    """Test categories endpoint"""
    print("\n=== Testing Categories ===")
    response = requests.get(f"{BASE_URL}/categories")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_classification(sender, subject, body):
    """Test email classification"""
    print(f"\n=== Testing Classification ===")
    print(f"Sender: {sender}")
    print(f"Subject: {subject}")
    print(f"Body: {body[:50]}...")
    
    email = {
        "sender": sender,
        "subject": subject,
        "body": body
    }
    
    response = requests.post(f"{BASE_URL}/classify", json=email)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    # Test health check
    test_health()
    
    # Test categories
    test_categories()
    
    # Test different email classifications
    test_emails = [
        {
            "sender": "hr@company.com",
            "subject": "Application Received",
            "body": "Thank you for your application. We have received your resume and will review it shortly."
        },
        {
            "sender": "recruiter@company.com",
            "subject": "Interview Invitation",
            "body": "We are pleased to invite you for an interview. Please let us know your availability for next week."
        },
        {
            "sender": "hiring@company.com",
            "subject": "Application Status Update",
            "body": "Unfortunately, we have decided to move forward with other candidates. We appreciate your interest in our company."
        },
        {
            "sender": "marketing@example.com",
            "subject": "Special Promotion - 50% Off",
            "body": "Dear Customer, we have a special promotion for you. Get 50% off on all products this weekend only!"
        }
    ]
    
    for email in test_emails:
        test_classification(email["sender"], email["subject"], email["body"])
