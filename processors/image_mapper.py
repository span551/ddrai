import json
import os
import re


class ImageMapper:

    def __init__(self, merged_path, inspection_path, thermal_path):

        with open(merged_path) as f:
            self.merged = json.load(f)

        with open(inspection_path) as f:
            self.inspection = json.load(f)

        with open(thermal_path) as f:
            self.thermal = json.load(f)

    def extract_page_number(self, img_path):
        match = re.search(r'page_(\d+)', img_path)
        return int(match.group(1)) if match else None

    def run(self, output_path):

        inspection_images = self.inspection.get("images", [])
        thermal_images = self.thermal.get("images", [])

        inspection_pages = self.inspection.get("pages", [])
        thermal_pages = self.thermal.get("pages", [])

        for area in self.merged:

            area_name = area["area"].lower()

            area["inspection_images"] = []
            area["thermal_images"] = []

            # 🔥 MATCH INSPECTION IMAGES
            for img in inspection_images:
                page_num = self.extract_page_number(img)

                if page_num and page_num <= len(inspection_pages):
                    page_text = inspection_pages[page_num - 1]["text"].lower()

                    if area_name in page_text:
                        area["inspection_images"].append(img)

            # 🔥 MATCH THERMAL IMAGES
            for img in thermal_images:
                page_num = self.extract_page_number(img)

                if page_num and page_num <= len(thermal_pages):
                    page_text = thermal_pages[page_num - 1]["text"].lower()

                    if area_name in page_text:
                        area["thermal_images"].append(img)

            # 🚨 FALLBACK (if nothing found)
            if not area["inspection_images"]:
                area["inspection_images"] = inspection_images[:2]

            if not area["thermal_images"]:
                area["thermal_images"] = thermal_images[:2]

        # SAVE
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.merged, f, indent=4)

        print("✅ Smart image mapping completed")
