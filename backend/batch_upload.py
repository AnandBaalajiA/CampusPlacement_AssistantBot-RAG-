"""
Batch upload multiple feedback PDFs
"""
import requests
import os
from pathlib import Path
import time

BASE_URL = "http://localhost:5000/api"

def upload_all_pdfs(directory):
    """Upload all PDFs from a directory"""
    # Get all PDF files
    pdf_files = list(Path(directory).glob("*.pdf"))
    total_files = len(pdf_files)
    
    print("=" * 70)
    print(f"BATCH PDF UPLOAD - Found {total_files} PDF files")
    print("=" * 70)
    
    successful = 0
    failed = 0
    total_chunks = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{i}/{total_files}] Uploading: {pdf_path.name}")
        print(f"Size: {pdf_path.stat().st_size / 1024:.2f} KB")
        
        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{BASE_URL}/pdf/upload", 
                    files=files,
                    timeout=300  # 5 minute timeout for large files
                )
            
            if response.status_code == 201:
                result = response.json()
                chunks = result.get('chunks_count', 0)
                doc_id = result.get('document_id', 'N/A')
                
                print(f"✓ SUCCESS")
                print(f"  Document ID: {doc_id}")
                print(f"  Chunks created: {chunks}")
                
                successful += 1
                total_chunks += chunks
            else:
                print(f"✗ FAILED: {response.text}")
                failed += 1
        
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            failed += 1
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 70)
    print("UPLOAD SUMMARY")
    print("=" * 70)
    print(f"Total files: {total_files}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total chunks created: {total_chunks}")
    print("=" * 70)

if __name__ == "__main__":
    # Update this path to your feedback PDFs folder
    feedback_dir = input("Enter path to feedback PDFs folder: ").strip()
    
    if not feedback_dir:
        feedback_dir = r"D:\PPBot\dataset"  # Default path
    
    if os.path.exists(feedback_dir):
        print(f"\nScanning directory: {feedback_dir}")
        upload_all_pdfs(feedback_dir)
    else:
        print(f"Error: Directory not found: {feedback_dir}")
