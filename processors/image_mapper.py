import json
import os
import re
from collections import defaultdict


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

    def assign_pages_to_areas(self, pages, images):

        area_names = [area["area"].lower() for area in self.merged]

        page_to_area = {}

        for i, page in enumerate(pages):

            text = page["text"].lower()

            scores = {}

            for area in area_names:
                scores[area] = text.count(area)

            # 🔥 pick best matching area
            best_area = max(scores, key=scores.get)

            # if no match → skip
            if scores[best_area] == 0:
                continue

            page_to_area[i + 1] = best_area

        # map images
        area_images = defaultdict(list)

        for img in images:
            page_num = self.extract_page_number(img)

            if page_num in page_to_area:
                area = page_to_area[page_num]
                area_images[area].append(img)

        return area_images

    def run(self, output_path):

        inspection_images = self.inspection.get("images", [])
        thermal_images = self.thermal.get("images", [])

        inspection_pages = self.inspection.get("pages", [])
        thermal_pages = self.thermal.get("pages", [])

        # 🔥 assign images smartly
        insp_map = self.assign_pages_to_areas(inspection_pages, inspection_images)
        therm_map = self.assign_pages_to_areas(thermal_pages, thermal_images)

        for area in self.merged:

            area_name = area["area"].lower()

            area["inspection_images"] = insp_map.get(area_name, [])
            area["thermal_images"] = therm_map.get(area_name, [])

            # 🚨 fallback if empty
            if not area["inspection_images"]:
                area["inspection_images"] = inspection_images[:2]

            if not area["thermal_images"]:
                area["thermal_images"] = thermal_images[:2]

        # SAVE
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.merged, f, indent=4)

        print("✅ Smart area-based mapping completed")
