import streamlit as st
import os
import tempfile
import json

from extractors.inspection_extractor import InspectionExtractor
from extractors.thermal_extractor import ThermalExtractor
from processors.merger_validator import DataMergerValidator
from processors.image_mapper import ImageMapper
from llm.ddr_generator import DDRGenerator
from report.docx_builder import DDRReportBuilder


st.set_page_config(page_title="AI DDR Generator", layout="wide")

st.title("🏠 AI DDR Report Generator")

inspection_file = st.file_uploader("Upload Inspection Report", type=["pdf"])
thermal_file = st.file_uploader("Upload Thermal Report", type=["pdf"])


if st.button("Generate DDR Report"):

    if not inspection_file or not thermal_file:
        st.error("Please upload both files")
        st.stop()

    with tempfile.TemporaryDirectory() as temp_dir:

        input_dir = os.path.join(temp_dir, "input")
        os.makedirs(input_dir)

        inspection_path = os.path.join(input_dir, "inspection.pdf")
        thermal_path = os.path.join(input_dir, "thermal.pdf")

        with open(inspection_path, "wb") as f:
            f.write(inspection_file.read())

        with open(thermal_path, "wb") as f:
            f.write(thermal_file.read())

        st.info("🔍 Running extraction...")

        # =========================
        # STEP 1 — EXTRACTION
        # =========================
        insp = InspectionExtractor(inspection_path)
        insp.run(os.path.join(temp_dir, "inspection"))

        therm = ThermalExtractor(thermal_path)
        therm.run(os.path.join(temp_dir, "thermal"))

        # =========================
        # 🔥 DEBUG STEP 2 — VERIFY IMAGES
        # =========================
        st.subheader("🔍 Debug: Extracted Data")

        try:
            with open(os.path.join(temp_dir, "inspection/inspection_data.json")) as f:
                inspection_json = json.load(f)
                st.write("📸 Inspection Images:", inspection_json.get("images", []))

            with open(os.path.join(temp_dir, "thermal/thermal_data.json")) as f:
                thermal_json = json.load(f)
                st.write("🌡 Thermal Images:", thermal_json.get("images", []))

        except Exception as e:
            st.error(f"Error reading JSON: {e}")

        # =========================
        # STEP 2 — MERGE
        # =========================
        merger = DataMergerValidator(
            os.path.join(temp_dir, "inspection/inspection_data.json"),
            os.path.join(temp_dir, "thermal/thermal_data.json")
        )
        merger.run(os.path.join(temp_dir, "merged.json"))

        # =========================
        # STEP 3 — LLM
        # =========================
        api_key = st.secrets["GROQ_API_KEY"]

        generator = DDRGenerator(api_key)
        generator.generate(
            os.path.join(temp_dir, "merged.json"),
            os.path.join(temp_dir, "llm.json")
        )

        # =========================
        # STEP 4 — IMAGE MAPPING
        # =========================
        mapper = ImageMapper(
            os.path.join(temp_dir, "merged.json"),
            os.path.join(temp_dir, "inspection/inspection_data.json"),
            os.path.join(temp_dir, "thermal/thermal_data.json")
        )
        mapper.run(os.path.join(temp_dir, "final.json"))

        # 🔥 DEBUG FINAL JSON
        st.subheader("🧠 Debug: Final Mapped Data")

        try:
            with open(os.path.join(temp_dir, "final.json")) as f:
                final_json = json.load(f)
                st.write(final_json)
        except Exception as e:
            st.error(f"Error reading final JSON: {e}")

        # =========================
        # STEP 5 — DOCX
        # =========================
        output_doc = os.path.join(temp_dir, "DDR_Report.docx")

        builder = DDRReportBuilder(
            os.path.join(temp_dir, "final.json"),
            os.path.join(temp_dir, "llm.json")
        )
        builder.build(output_doc)

        st.success("✅ DDR Generated!")

        with open(output_doc, "rb") as f:
            st.download_button(
                "📥 Download DDR Report",
                f,
                file_name="DDR_Report.docx"
            )
