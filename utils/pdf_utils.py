import fitz  # PyMuPDF
import os
import hashlib
import pdfplumber


def is_duplicate(image_bytes, seen_hashes):
    img_hash = hashlib.md5(image_bytes).hexdigest()
    if img_hash in seen_hashes:
        return True
    seen_hashes.add(img_hash)
    return False


def extract_images_from_pdf(pdf_path, output_folder, min_size=200, max_images=100):

    doc = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    image_paths = []
    seen_hashes = set()

    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):

            if len(image_paths) >= max_images:
                print(f"⚠️ Reached max image limit: {max_images}")
                return image_paths

            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            width = base_image["width"]
            height = base_image["height"]

            # ❌ FILTER 1: Skip tiny images
            if width < min_size or height < min_size:
                continue

            # ❌ FILTER 2: Remove duplicates
            if is_duplicate(image_bytes, seen_hashes):
                continue

            image_name = f"page_{page_index+1}_img_{img_index+1}.png"
            image_path = os.path.join(output_folder, image_name)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_path)

    print(f"🖼️ Extracted {len(image_paths)} filtered images")
    return image_paths


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
