import json
import os
from utils.pdf_utils import extract_images_from_pdf, extract_text_by_page


class InspectionExtractor:

    def __init__(self, pdf_path, output_dir):
        self.pdf_path = pdf_path
        self.output_dir = output_dir

    def extract(self):

        print("🔍 Extracting Inspection Report...")

        pages = extract_text_by_page(self.pdf_path)

        image_folder = os.path.join(self.output_dir, "images")

        images = extract_images_from_pdf(
            self.pdf_path,
            image_folder,
            min_size=200,
            max_images=80
        )

        data = {
            "pages": pages,
            "images": images
        }

        output_path = os.path.join(self.output_dir, "inspection.json")

        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Inspection extraction complete")

        return output_path
