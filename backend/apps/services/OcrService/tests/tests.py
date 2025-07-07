import os
import requests


def test_ocr_image(image_path, expected_results):
    url = "http://localhost:8000/api/v1/ocr"
    with open(image_path, "rb") as f:
        files = {"file": ("test_plan.png", f, "image/png")}
        response = requests.post(url, files=files)
    assert (
        response.status_code == 200
    ), f"Failed with status {response.status_code}: {response.text}"
    result = response.json()
    print("OCR Results:")
    for item in result["results"]:
        print(item)
    # Check that all expected results are present in the OCR output
    for expected in expected_results:
        found = False
        for item in result["results"]:
            if (
                item["text"].strip().lower() == expected["text"].strip().lower()
                and abs(item["bounding_box"]["x"] - expected["bounding_box"]["x"]) < 10
                and abs(item["bounding_box"]["y"] - expected["bounding_box"]["y"]) < 10
            ):
                found = True
                break
        assert (
            found
        ), f"Expected label '{expected['text']}' with bounding box near {expected['bounding_box']} not found."
    print(f"Test passed for {image_path}")


if __name__ == "__main__":
    # Example expected results for test_plan.png
    expected_results = [
        {
            "text": "Hello",
            "bounding_box": {"x": 1311, "y": 574, "width": 89, "height": 37},
        },
        {
            "text": "Room A",
            "bounding_box": {"x": 1491, "y": 1136, "width": 375, "height": 121},
        },
        {
            "text": "Room B",
            "bounding_box": {"x": 3569, "y": 1131, "width": 385, "height": 126},
        },
        {
            "text": "Room C",
            "bounding_box": {"x": 1491, "y": 2383, "width": 384, "height": 111},
        },
        {
            "text": "Room D",
            "bounding_box": {"x": 3574, "y": 2383, "width": 384, "height": 111},
        },
    ]
    test_ocr_image("test_plan.png", expected_results)
    # You can add a similar test for the PDF if your OCR supports PDF input
