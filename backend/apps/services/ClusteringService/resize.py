from PIL import Image


def resize_image_keep_aspect(input_path, output_path, max_side=4000):
    img = Image.open(input_path)
    width, height = img.size

    # Determine scale factor to keep max side <= max_side
    scale = max_side / max(width, height)

    if scale < 1:  # Only resize if image is bigger than max_side
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        print(f"Resized image from ({width}, {height}) to ({new_width}, {new_height})")
    else:
        print(f"Image size ({width}, {height}) is within the limit; no resize needed.")

    img.save(output_path)
    return output_path


# Example usage
resized_image_path = resize_image_keep_aspect(
    "C:\\dev\\ai-sow\\backend\\apps\\services\\ClusteringService\\images\\test_data_page_9.png",
    "C:\\dev\\ai-sow\\backend\\apps\\services\\ClusteringService\\images\\test_data_page_9_resized.png",
    max_side=4000,
)
