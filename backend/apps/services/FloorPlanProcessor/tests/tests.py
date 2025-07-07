import os
import requests
import json


def test_floorplan_processor(image_path, ocr_results, expected_labels):
    url = "http://localhost:8000/api/v1/process"
    with open(image_path, "rb") as f:
        files = {"file": (os.path.basename(image_path), f, "image/png")}
        data = {"ocr_json": json.dumps(ocr_results)}
        response = requests.post(url, files=files, data=data)
    assert (
        response.status_code == 200
    ), f"Failed with status {response.status_code}: {response.text}"
    result = response.json()
    print("FloorPlanProcessor Results:")
    for room in result["rooms"]:
        print(room)
    # Check that all expected labels are present in the output
    for label in expected_labels:
        found = False
        for room in result["rooms"]:
            if room["label"].strip().lower() == label.strip().lower():
                found = True
                break
        assert found, f"Expected room label '{label}' not found in output."
    print(f"Test passed for {image_path}")


if __name__ == "__main__":
    ocr_results = [
        {
            "text": "Hello",
            "bounding_box": {"x": 1311, "y": 574, "width": 89, "height": 37},
            "confidence": 0.95,
        },
        {
            "text": "Room A",
            "bounding_box": {"x": 1491, "y": 1136, "width": 375, "height": 121},
            "confidence": 0.90,
        },
        {
            "text": "Room B",
            "bounding_box": {"x": 3569, "y": 1131, "width": 385, "height": 126},
            "confidence": 0.85,
        },
        {
            "text": "Room C",
            "bounding_box": {"x": 1491, "y": 2383, "width": 384, "height": 111},
            "confidence": 0.80,
        },
        {
            "text": "Room D",
            "bounding_box": {"x": 3574, "y": 2383, "width": 384, "height": 111},
            "confidence": 0.75,
        },
    ]
    expected_labels = ["Hello", "Room A", "Room B", "Room C", "Room D"]
    test_floorplan_processor("test_plan.png", ocr_results, expected_labels)
