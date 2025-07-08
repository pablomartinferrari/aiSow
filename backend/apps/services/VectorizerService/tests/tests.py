import os
import requests
import fitz  # PyMuPDF
import uuid


def extract_first_n_pages(input_pdf, output_pdf, n_pages=25):
    doc = fitz.open(input_pdf)
    new_doc = fitz.open()
    if n_pages is None or n_pages == -1:
        n_pages = len(doc)
    for i in range(min(n_pages, len(doc))):
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()
    print(f"Saved first {n_pages} pages to {output_pdf}")


def test_vectorize_pdf(pdf_path, n_pages=3, expect_scale=True):
    # Always extract first n pages to a temp file unless n_pages is None or -1
    if n_pages is None or n_pages == -1:
        small_pdf = pdf_path
    else:
        small_pdf = pdf_path.replace(".pdf", f"_first{n_pages}.pdf")
        extract_first_n_pages(pdf_path, small_pdf, n_pages)
    url = "http://localhost:8000/api/v1/vectorize"
    project_id = str(uuid.uuid4())
    print(f"Using project_id: {project_id}")
    with open(small_pdf, "rb") as f:
        files = {"file": (os.path.basename(small_pdf), f, "application/pdf")}
        data = {"project_id": project_id}
        response = requests.post(url, files=files, data=data)
    assert (
        response.status_code == 200
    ), f"Failed with status {response.status_code}: {response.text}"
    result = response.json()
    print("VectorizerService Results:")
    print(f"Fallback: {result.get('fallback', False)}")
    print(f"Lines: {len(result.get('lines', []))}")
    print(f"Texts: {len(result.get('texts', []))}")
    print(f"Paths: {len(result.get('paths', []))}")
    if result.get("lines"):
        print("Sample line:", result["lines"][0])
    if result.get("texts"):
        print("Sample text:", result["texts"][0])
    if result.get("paths"):
        print("Sample path:", result["paths"][0])
    assert not result.get(
        "fallback", False
    ), "PDF was not vectorized (fallback triggered)"
    assert (
        len(result.get("lines", [])) > 0 or len(result.get("paths", [])) > 0
    ), "No vector geometry extracted"
    assert len(result.get("texts", [])) > 0, "No vector text extracted"
    if expect_scale:
        # New model: result['scales'] is a list of per-page scale info dicts
        scales = result.get("scales")
        assert (
            scales is not None
        ), "No 'scales' field in response, but one was expected."
        assert isinstance(
            scales, list
        ), f"'scales' should be a list, got {type(scales)}"
        assert len(scales) > 0, "No per-page scale info found in 'scales' list."
        for i, page_scale in enumerate(scales):
            assert (
                "page" in page_scale
            ), f"Missing 'page' in page_scale entry {i}: {page_scale}"
            assert (
                "scale" in page_scale
            ), f"Missing 'scale' in page_scale entry {i}: {page_scale}"
            # Accept NTS (Not to Scale) or a string/float scale
            if not page_scale.get("nts", False):
                scale_val = page_scale["scale"]
                assert scale_val is not None, f"Scale for page {i} is None."
                print(f"Page {page_scale['page']} scale: {scale_val}")
            else:
                print(f"Page {page_scale['page']} is NTS (Not to Scale)")
    print("Test passed!")


if __name__ == "__main__":
    # To vectorize the whole document, pass n_pages=None or n_pages=-1
    test_vectorize_pdf("tests/test_data.pdf", n_pages=5, expect_scale=True)
