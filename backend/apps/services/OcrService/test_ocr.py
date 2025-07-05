#!/usr/bin/env python3
"""
Test script for the OCR service
"""

import requests
import json
import os
from pathlib import Path


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


def test_languages():
    """Test the languages endpoint"""
    try:
        response = requests.get("http://localhost:8000/api/v1/languages")
        print(f"Languages: {response.status_code}")
        if response.status_code == 200:
            languages = response.json()
            print(f"Supported languages: {len(languages)}")
            for lang in languages[:5]:  # Show first 5
                print(f"  - {lang['code']}: {lang['name']}")
        return response.status_code == 200
    except Exception as e:
        print(f"Languages test failed: {e}")
        return False


def test_pdf_processing(pdf_path):
    """Test PDF processing"""
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return False

    try:
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            data = {"language": "en"}
            response = requests.post(
                "http://localhost:8000/api/v1/process-pdf", files=files, data=data
            )

        print(f"PDF processing: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Filename: {result['filename']}")
            print(f"Pages processed: {len(result['pages'])}")
            print(f"Processing time: {result['processing_time']['total_seconds']:.2f}s")

            # Show first page text (truncated)
            if result["pages"]:
                first_page = result["pages"][0]
                # Extract text from items
                items = first_page.get("items", [])
                if items:
                    # Combine all text from items
                    text_parts = [item["text"] for item in items]
                    full_text = " ".join(text_parts)
                    text = (
                        full_text[:200] + "..." if len(full_text) > 200 else full_text
                    )
                    print(f"First page text: {text}")

                    # Calculate average confidence
                    confidences = [item["confidence"] for item in items]
                    avg_confidence = (
                        sum(confidences) / len(confidences) if confidences else 0
                    )
                    print(f"Average confidence: {avg_confidence:.2f}")
                    print(f"Items detected: {len(items)}")
                else:
                    print("No text items detected on first page")
        else:
            print(f"Error: {response.text}")

        return response.status_code == 200
    except Exception as e:
        print(f"PDF processing test failed: {e}")
        return False


def test_image_processing(image_path):
    """Test image processing"""
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return False

    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            data = {"language": "en"}
            response = requests.post(
                "http://localhost:8000/api/v1/process-image", files=files, data=data
            )

        print(f"Image processing: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Filename: {result['filename']}")
            print(f"Processing time: {result['processing_time']['total_seconds']:.2f}s")

            if result["pages"]:
                first_page = result["pages"][0]
                # Extract text from items
                items = first_page.get("items", [])
                if items:
                    # Combine all text from items
                    text_parts = [item["text"] for item in items]
                    full_text = " ".join(text_parts)
                    text = (
                        full_text[:200] + "..." if len(full_text) > 200 else full_text
                    )
                    print(f"Extracted text: {text}")

                    # Calculate average confidence
                    confidences = [item["confidence"] for item in items]
                    avg_confidence = (
                        sum(confidences) / len(confidences) if confidences else 0
                    )
                    print(f"Average confidence: {avg_confidence:.2f}")
                    print(f"Items detected: {len(items)}")
                else:
                    print("No text items detected")
        else:
            print(f"Error: {response.text}")

        return response.status_code == 200
    except Exception as e:
        print(f"Image processing test failed: {e}")
        return False


def test_specific_page_processing(pdf_path, page_number=1):
    """Test processing a specific page"""
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return False

    try:
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            data = {"language": "en", "page_number": page_number}
            response = requests.post(
                "http://localhost:8000/api/v1/process-pdf", files=files, data=data
            )

        print(f"Specific page processing (page {page_number}): {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Filename: {result['filename']}")
            print(f"Pages processed: {len(result['pages'])}")

            if result["pages"]:
                page = result["pages"][0]
                items = page.get("items", [])
                print(f"Items detected on page {page_number}: {len(items)}")

                if items:
                    # Show first few items
                    for i, item in enumerate(items[:3]):
                        print(
                            f"  Item {i+1}: '{item['text']}' (confidence: {item['confidence']:.2f})"
                        )
        else:
            print(f"Error: {response.text}")

        return response.status_code == 200
    except Exception as e:
        print(f"Specific page processing test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=== OCR Service Test Suite ===\n")

    # Test 1: Health check
    print("1. Testing health check...")
    health_ok = test_health_check()
    print()

    # Test 2: Languages
    print("2. Testing languages endpoint...")
    languages_ok = test_languages()
    print()

    # Test 3: PDF processing (if PDF exists)
    pdf_path = "test_document.pdf"
    if os.path.exists(pdf_path):
        print("3. Testing PDF processing...")
        pdf_ok = test_pdf_processing(pdf_path)
        print()

        # Test 3.5: Specific page processing
        print("3.5. Testing specific page processing...")
        specific_page_ok = test_specific_page_processing(pdf_path, 1)
        print()
    else:
        print("3. Skipping PDF test (no test_document.pdf found)")
        pdf_ok = True
        specific_page_ok = True
        print()

    # Test 4: Image processing (if image exists)
    image_path = os.path.join("images", "test_document_page_1.jpg")
    if os.path.exists(image_path):
        print("4. Testing image processing...")
        image_ok = test_image_processing(image_path)
        print()
    else:
        print("4. Skipping image test (no test_image.jpg found)")
        image_ok = True
        print()

    # Summary
    print("=== Test Summary ===")
    print(f"Health check: {'✓' if health_ok else '✗'}")
    print(f"Languages: {'✓' if languages_ok else '✗'}")
    print(f"PDF processing: {'✓' if pdf_ok else '✗'}")
    if os.path.exists(pdf_path):
        print(f"Specific page processing: {'✓' if specific_page_ok else '✗'}")
    print(f"Image processing: {'✓' if image_ok else '✗'}")

    all_passed = health_ok and languages_ok and pdf_ok and image_ok
    if os.path.exists(pdf_path):
        all_passed = all_passed and specific_page_ok

    print(f"\nOverall: {'✓ All tests passed' if all_passed else '✗ Some tests failed'}")


if __name__ == "__main__":
    main()
