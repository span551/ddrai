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

    def run(self, output_path):

        inspection_images = self.inspection.get("images", [])
        thermal_images = self.thermal.get("images", [])

        areas = self.merged

        total_areas = len(areas)

        # 🔥 DISTRIBUTE IMAGES EVENLY
        def split_images(images):
            if not images:
                return [[] for _ in range(total_areas)]

            chunk_size = max(1, len(images) // total_areas)

            chunks = []
            for i in range(total_areas):
                start = i * chunk_size
                end = (i + 1) * chunk_size if i < total_areas - 1 else len(images)
                chunks.append(images[start:end])

            return chunks

        insp_chunks = split_images(inspection_images)
        therm_chunks = split_images(thermal_images)

        # 🔥 ASSIGN TO AREAS
        for i, area in enumerate(areas):
            area["inspection_images"] = insp_chunks[i]
            area["thermal_images"] = therm_chunks[i]

        # SAVE
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(areas, f, indent=4)

        print("✅ Images mapped to areas")
