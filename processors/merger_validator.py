import json
import os


class DataMergerValidator:

    def __init__(self, inspection_path, thermal_path):
        with open(inspection_path) as f:
            self.inspection = json.load(f)

        with open(thermal_path) as f:
            self.thermal = json.load(f)

    # 🔹 Map area names manually (based on PDF)
    def map_area_names(self):
        return [
            "Hall",
            "Bedroom",
            "Master Bedroom",
            "Kitchen",
            "Master Bedroom Wall",
            "Parking Area",
            "Common Bathroom"
        ]

    # 🔹 Map thermal scans to areas (simple distribution)
    def map_thermal_to_areas(self, areas):
        scans = self.thermal["thermal_scans"]

        mapping = {area: [] for area in areas}

        for i, scan in enumerate(scans):
            area = areas[i % len(areas)]  # distribute evenly
            mapping[area].append(scan)

        return mapping

    # 🔹 Detect severity from thermal
    def evaluate_thermal_severity(self, scan):
        diff = scan["hotspot"] - scan["coldspot"]

        if diff > 5:
            return "High"
        elif diff > 3:
            return "Moderate"
        else:
            return "Low"

    # 🔹 Main merge logic
    def merge(self):

        areas_raw = self.inspection["impacted_areas"]
        area_names = self.map_area_names()
        thermal_map = self.map_thermal_to_areas(area_names)

        merged = []

        for i, area_data in enumerate(areas_raw):

            area_name = area_names[i] if i < len(area_names) else f"Area {i+1}"

            entry = {
                "area": area_name,
                "inspection_issues": [],
                "thermal_findings": [],
                "conflicts": [],
                "missing": []
            }

            # 🔸 Add inspection issues
            if area_data["negative"]:
                entry["inspection_issues"].append(area_data["negative"])

            if area_data["positive"]:
                entry["inspection_issues"].append(area_data["positive"])

            # 🔸 Add thermal data
            if area_name in thermal_map and thermal_map[area_name]:
                for scan in thermal_map[area_name]:
                    severity = self.evaluate_thermal_severity(scan)

                    entry["thermal_findings"].append({
                        "hotspot": scan["hotspot"],
                        "coldspot": scan["coldspot"],
                        "severity": severity
                    })

                    # 🔴 Conflict logic
                    if "dampness" in str(area_data["negative"]).lower() and severity == "High":
                        entry["conflicts"].append(
                            "Thermal indicates severe moisture but inspection marked general dampness"
                        )
            else:
                entry["missing"].append("Thermal Data Not Available")

            # 🔸 Missing inspection
            if not entry["inspection_issues"]:
                entry["missing"].append("Inspection Data Not Available")

            merged.append(entry)

        return merged

    def run(self, output_path):

        merged_data = self.merge()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(merged_data, f, indent=4)

        print("✅ Data merging + validation complete")

        return merged_data
