import json
import os


class ImageMapper:

    def __init__(self, merged_path, inspection_path, thermal_path):
        with open(merged_path) as f:
            self.merged = json.load(f)

        with open(inspection_path) as f:
            self.inspection = json.load(f)

        with open(thermal_path) as f:
            self.thermal = json.load(f)

    # 🔹 Hardcoded mapping (based on PDF)
    def get_inspection_image_map(self):

        images = self.inspection["images"]

        return {
            "Hall": images[0:11],
            "Bedroom": images[11:19],
            "Master Bedroom": images[19:30],
            "Kitchen": images[30:37],
            "Master Bedroom Wall": images[37:48],
            "Parking Area": images[48:57],
            "Common Bathroom": images[57:64],
        }

    # 🔹 Map thermal images
    def get_thermal_image_map(self, areas):

        images = self.thermal["images"]
        mapping = {area: [] for area in areas}

        for i, img in enumerate(images):
            area = areas[i % len(areas)]
            mapping[area].append(img)

        return mapping

    def run(self, output_path):

        areas = [entry["area"] for entry in self.merged]

        inspection_map = self.get_inspection_image_map()
        thermal_map = self.get_thermal_image_map(areas)

        final_data = []

        for entry in self.merged:

            area = entry["area"]

            entry["inspection_images"] = inspection_map.get(area, ["Image Not Available"])
            entry["thermal_images"] = thermal_map.get(area, ["Image Not Available"])

            # If empty → mark explicitly
            if not entry["inspection_images"]:
                entry["inspection_images"] = ["Image Not Available"]

            if not entry["thermal_images"]:
                entry["thermal_images"] = ["Image Not Available"]

            final_data.append(entry)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(final_data, f, indent=4)

        print("✅ Image mapping complete")

        return final_data
