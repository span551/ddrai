import pdfplumber
import os
from PIL import Image
import io


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


def extract_images_from_pdf(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    image_paths = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):

            if not page.images:
                continue

            for img_index, img in enumerate(page.images):

                try:
                    x0, top, x1, bottom = (
                        img["x0"], img["top"], img["x1"], img["bottom"]
                    )

                    cropped = page.crop((x0, top, x1, bottom)).to_image()

                    img_bytes = cropped.original

                    # Convert to PIL
                    pil_img = Image.open(io.BytesIO(img_bytes))

                    width, height = pil_img.size

                    # ✅ FILTER small icons
                    if width < 200 or height < 200:
                        continue

                    image_name = f"page{page_index+1}_img{img_index+1}.png"
                    image_path = os.path.join(output_folder, image_name)

                    pil_img.save(image_path)

                    image_paths.append(image_path)

                except Exception:
                    continue

    return image_paths
