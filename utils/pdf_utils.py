import pdfplumber
import os
from PIL import Image


def extract_text_by_page(pdf_path):
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({
                "page": i + 1,
                "text": text
            })

    return pages


# 🔥 NEW IMAGE EXTRACTION (PAGE-BASED)
def extract_images_from_pdf(pdf_path, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    image_paths = []

    with pdfplumber.open(pdf_path) as pdf:

        for i, page in enumerate(pdf.pages):

            try:
                # Convert FULL PAGE to image
                im = page.to_image(resolution=200)

                image_path = os.path.abspath(
                    os.path.join(output_folder, f"page_{i+1}.png")
                )

                im.save(image_path, format="PNG")

                image_paths.append(image_path)

            except Exception as e:
                print("❌ Page render failed:", e)

    return image_paths
