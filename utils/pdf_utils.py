import fitz  # PyMuPDF
import os
from PIL import Image
import io


def is_valid_image(image_bytes):

    try:
        img = Image.open(io.BytesIO(image_bytes))

        width, height = img.size

        # ❌ Filter small icons/logos
        if width < 200 or height < 200:
            return False

        # ❌ Filter very tiny file size
        if len(image_bytes) < 5000:
            return False

        return True

    except:
        return False


def extract_images_from_pdf(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    image_paths = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            ext = base_image["ext"]

            # ✅ APPLY FILTER
            if not is_valid_image(image_bytes):
                continue

            image_name = f"page{page_index+1}_img{img_index+1}.{ext}"
            image_path = os.path.join(output_folder, image_name)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_path)

    return image_paths


def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)

    pages = []
    for i, page in enumerate(doc):
        pages.append({
            "page": i + 1,
            "text": page.get_text()
        })

    return pages
