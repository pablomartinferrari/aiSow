#!/usr/bin/env python3
"""
Test script for the Pdf2Image service
"""

import requests
import os


def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_pdf_processing(pdf_path):
    """Test PDF to image conversion"""
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return False

    try:
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                "http://localhost:8000/api/v1/process-pdf", files=files
            )

        print(f"PDF processing: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Filename: {result['filename']}")
            print(f"Processing time: {result['processing_time']['total_seconds']:.2f}s")
            print(f"Image paths:")
            for img_path in result.get("image_paths", []):
                print(f"  - {img_path} (exists: {os.path.exists(img_path)})")
            print(f"Total images: {len(result.get('image_paths', []))}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"PDF processing test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=== Pdf2Image Service Test Suite ===\n")

    # Test 1: Health check
    print("1. Testing health check...")
    health_ok = test_health_check()
    print()

    # Test 2: PDF processing (if PDF exists)
    pdf_path = "test_document.pdf"
    if os.path.exists(pdf_path):
        print("2. Testing PDF to image conversion...")
        pdf_ok = test_pdf_processing(pdf_path)
        print()
    else:
        print("2. Skipping PDF test (no test_document.pdf found)")
        pdf_ok = True
        print()

    # Summary
    print("=== Test Summary ===")
    print(f"Health check: {'✓' if health_ok else '✗'}")
    print(f"PDF to image: {'✓' if pdf_ok else '✗'}")
    all_passed = health_ok and pdf_ok
    print(f"\nOverall: {'✓ All tests passed' if all_passed else '✗ Some tests failed'}")


if __name__ == "__main__":
    main()
