import re
import json
import os
from utils.pdf_utils import extract_images_from_pdf, extract_text_by_page


class InspectionExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pages = extract_text_by_page(pdf_path)

    def get_full_text(self):
        return "\n".join([p["text"] for p in self.pages])

    def extract_impacted_areas(self, text):
        areas = []

        pattern = r"Impacted Area (\d+)(.*?)(?=Impacted Area \d+|SUMMARY TABLE)"
        matches = re.findall(pattern, text, re.DOTALL)

        for num, content in matches:
            area_data = {
                "area_id": int(num),
                "negative": None,
                "positive": None
            }

            neg_match = re.search(r"Negative side Description(.*?)(Photo|Positive)", content, re.DOTALL)
            pos_match = re.search(r"Positive side Description(.*?)(Photo)", content, re.DOTALL)

            if neg_match:
                area_data["negative"] = neg_match.group(1).strip()

            if pos_match:
                area_data["positive"] = pos_match.group(1).strip()

            areas.append(area_data)

        return areas

    def extract_summary(self, text):
        summary = []

        pattern = r"\d+\s+Observed(.*?)\n"
        matches = re.findall(pattern, text)

        for m in matches:
            summary.append(m.strip())

        return summary

    def run(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        text = self.get_full_text()

        data = {
            "impacted_areas": self.extract_impacted_areas(text),
            "summary": self.extract_summary(text)
        }

        # Extract images
        image_paths = extract_images_from_pdf(
            self.pdf_path,
            os.path.join(output_dir, "images")
        )

        data["images"] = image_paths

        # Save JSON
        with open(os.path.join(output_dir, "inspection_data.json"), "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Inspection extraction complete")

        return data
