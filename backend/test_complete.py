"""
Complete API test suite for RAG Bot
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def print_separator():
    print("\n" + "=" * 60)

def test_health():
    """Test health endpoint"""
    print_separator()
    print("TEST 1: Health Check")
    print_separator()
    
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_readiness():
    """Test readiness endpoint"""
    print_separator()
    print("TEST 2: Readiness Check")
    print_separator()
    
    try:
        response = requests.get(f"{BASE_URL}/health/ready")
        print(f"✓ Status Code: {response.status_code}")
        print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_list_documents():
    """Test list documents"""
    print_separator()
    print("TEST 3: List Documents")
    print_separator()
    
    try:
        response = requests.get(f"{BASE_URL}/pdf/list")
        print(f"✓ Status Code: {response.status_code}")
        result = response.json()
        print(f"✓ Total Documents: {result.get('count', 0)}")
        if result.get('documents'):
            print(f"✓ Documents: {json.dumps(result['documents'], indent=2)}")
        else:
            print("✓ No documents uploaded yet")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_upload_pdf(pdf_path):
    """Test PDF upload"""
    print_separator()
    print(f"TEST 4: Upload PDF - {pdf_path}")
    print_separator()
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/pdf/upload", files=files)
        
        print(f"✓ Status Code: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Message: {result.get('message')}")
            print(f"✓ Document ID: {result.get('document_id')}")
            print(f"✓ Filename: {result.get('filename')}")
            print(f"✓ Chunks Created: {result.get('chunks_count')}")
            return True, result.get('document_id')
        else:
            print(f"✗ Error: {response.text}")
            return False, None
    except FileNotFoundError:
        print(f"✗ File not found: {pdf_path}")
        return False, None
    except Exception as e:
        print(f"✗ Error: {e}")
        return False, None

def test_query(question):
    """Test query endpoint"""
    print_separator()
    print(f"TEST 5: Ask Question - '{question}'")
    print_separator()
    
    try:
        data = {"query": question, "top_k": 5}
        response = requests.post(
            f"{BASE_URL}/query/ask",
            headers={"Content-Type": "application/json"},
            json=data
        )
        
        print(f"✓ Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Answer:\n{result.get('answer', 'No answer')}\n")
            print(f"✓ Chunks Used: {result.get('chunks_used', 0)}")
            print(f"✓ Sources: {len(result.get('sources', []))} sources")
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_delete_document(doc_id):
    """Test document deletion"""
    print_separator()
    print(f"TEST 6: Delete Document - {doc_id}")
    print_separator()
    
    try:
        response = requests.delete(f"{BASE_URL}/pdf/delete/{doc_id}")
        print(f"✓ Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ Message: {response.json().get('message')}")
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("RAG PLACEMENT PREP BOT - API TEST SUITE")
    print("=" * 60)
    
    # Test 1: Health
    if not test_health():
        print("\n✗ Health check failed. Is the server running?")
        sys.exit(1)
    
    # Test 2: Readiness
    test_readiness()
    
    # Test 3: List documents (before upload)
    test_list_documents()
    
    # Test 4: Upload PDF (optional - requires PDF file)
    pdf_path = input("\nEnter path to PDF file to upload (or press Enter to skip): ").strip()
    doc_id = None
    if pdf_path:
        success, doc_id = test_upload_pdf(pdf_path)
        if success:
            # Test list again after upload
            test_list_documents()
    
    # Test 5: Query (only if document uploaded)
    if pdf_path:
        question = input("\nEnter a question to ask (or press Enter for default): ").strip()
        if not question:
            question = "What is machine learning?"
        test_query(question)
    else:
        print("\nℹ Skipping query test - no document uploaded")
    
    # Test 6: Delete (optional)
    if doc_id:
        delete = input(f"\nDelete uploaded document {doc_id}? (y/n): ").strip().lower()
        if delete == 'y':
            test_delete_document(doc_id)
    
    print_separator()
    print("ALL TESTS COMPLETED!")
    print_separator()

if __name__ == "__main__":
    main()
