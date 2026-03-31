import re
import json
import os
from utils.pdf_utils import extract_images_from_pdf, extract_text_by_page


class ThermalExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pages = extract_text_by_page(pdf_path)

    def parse_thermal_data(self, text):
        scans = []

        pattern = r"Hotspot\s*:\s*([\d.]+).*?Coldspot\s*:\s*([\d.]+).*?Thermal image\s*:\s*(\S+)"
        matches = re.findall(pattern, text, re.DOTALL)

        for i, (hot, cold, img) in enumerate(matches):
            scans.append({
                "scan_id": i + 1,
                "hotspot": float(hot),
                "coldspot": float(cold),
                "image_name": img
            })

        return scans

    def run(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        text = "\n".join([p["text"] for p in self.pages])

        data = {
            "thermal_scans": self.parse_thermal_data(text)
        }

        # Extract images
        image_paths = extract_images_from_pdf(
            self.pdf_path,
            os.path.join(output_dir, "images")
        )

        data["images"] = image_paths

        # Save JSON
        with open(os.path.join(output_dir, "thermal_data.json"), "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Thermal extraction complete")

        return data
