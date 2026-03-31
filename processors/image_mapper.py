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

    # ✅ Distribute inspection images area-wise
    def map_inspection_images(self):

        images = self.inspection.get("images", [])
        areas = self.merged

        mapping = {area["area"]: [] for area in areas}

        if not images:
            return mapping

        per_area = max(1, len(images) // len(areas))

        for i, area in enumerate(areas):
            start = i * per_area
            end = (i + 1) * per_area if i < len(areas) - 1 else len(images)

            mapping[area["area"]] = images[start:end]

        return mapping

    # ✅ Distribute thermal images area-wise
    def map_thermal_images(self):

        thermal_data = self.thermal.get("thermal_data", [])
        areas = self.merged

        mapping = {area["area"]: [] for area in areas}

        if not thermal_data:
            return mapping

        per_area = max(1, len(thermal_data) // len(areas))

        for i, area in enumerate(areas):
            start = i * per_area
            end = (i + 1) * per_area if i < len(areas) - 1 else len(thermal_data)

            imgs = []
            for item in thermal_data[start:end]:
                if "image" in item:
                    imgs.append(item["image"])

            mapping[area["area"]] = imgs

        return mapping

    def run(self, output_path):

        inspection_map = self.map_inspection_images()
        thermal_map = self.map_thermal_images()

        # ✅ Attach images to merged data
        for area in self.merged:
            name = area["area"]

            area["inspection_images"] = inspection_map.get(name, [])
            area["thermal_images"] = thermal_map.get(name, [])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(self.merged, f, indent=4)

        print("✅ Image mapping completed")
