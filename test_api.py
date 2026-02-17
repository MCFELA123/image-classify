"""
Test the Fruit Classification API
"""
import requests
import json


def test_health():
    """Test health check endpoint"""
    print("Testing health check endpoint...")
    response = requests.get('http://localhost:5000/api/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)


def test_get_classes():
    """Test get classes endpoint"""
    print("Testing get classes endpoint...")
    response = requests.get('http://localhost:5000/api/classes')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)


def test_classify_image(image_path):
    """Test image classification endpoint"""
    print(f"Testing classification with image: {image_path}")
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post('http://localhost:5000/api/classify', files=files)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)


def test_get_history():
    """Test get history endpoint"""
    print("Testing get history endpoint...")
    response = requests.get('http://localhost:5000/api/history?limit=5')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)


def test_get_statistics():
    """Test get statistics endpoint"""
    print("Testing get statistics endpoint...")
    response = requests.get('http://localhost:5000/api/statistics')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)


if __name__ == "__main__":
    import sys
    
    print("🍎 Fruit Classification API Test Suite")
    print("=" * 50)
    
    # Test basic endpoints
    try:
        test_health()
        test_get_classes()
        test_get_statistics()
        test_get_history()
        
        # Test classification if image path provided
        if len(sys.argv) > 1:
            image_path = sys.argv[1]
            test_classify_image(image_path)
        else:
            print("\nTo test image classification, run:")
            print("  python test_api.py path/to/your/image.jpg")
        
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("Make sure the Flask server is running:")
        print("  python backend/app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
