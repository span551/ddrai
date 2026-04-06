# 🏠 AI-Powered DDR Report Generator

An end-to-end AI system that converts **Inspection Reports** and **Thermal Reports** into a structured, client-ready **Detailed Diagnostic Report (DDR)**.

This project demonstrates **real-world AI pipeline design**, combining document processing, data validation, LLM reasoning, and automated report generation.

---

## 🚀 Features

* 📄 Extracts data from Inspection & Thermal PDFs
* 🧠 Merges and validates multi-source data
* ⚠️ Detects missing and conflicting information
* 🖼️ Extracts and places images contextually
* 🤖 Uses LLM for structured reasoning
* 📑 Generates professional **DOCX reports**
* 🌐 Deployed using Streamlit (interactive UI)

---

## 🧠 System Architecture

The system follows a **5-step modular pipeline**:

### 🔹 Step 1 — Data Extraction

* Extracts:

  * Text (area-wise observations)
  * Images (converted from PDF pages)
* Tools:

  * `pdfplumber`
  * `Pillow`

---

### 🔹 Step 2 — Data Merger & Validator

* Combines inspection + thermal data
* Handles:

  * Missing data → `"Not Available"`
  * Conflicts → explicitly flagged
  * Duplicate observations → removed

---

### 🔹 Step 3 — LLM Reasoning Engine

* Uses Groq API (LLaMA model)
* Generates structured JSON output:

  * Property summary
  * Root cause
  * Severity
  * Recommendations

---

### 🔹 Step 4 — Image Mapping Engine

* Maps images to respective areas
* Ensures:

  * Each area has visual context
  * Inspection + Thermal images shown together

---

### 🔹 Step 5 — Report Builder

* Generates final **DOCX DDR report**
* Includes:

  * Structured sections
  * Area-wise observations
  * Embedded images

---

## 📂 Project Structure

```
ai-ddr-system/
│
├── app.py
├── requirements.txt
│
├── extractors/
│   ├── inspection_extractor.py
│   └── thermal_extractor.py
│
├── processors/
│   ├── merger_validator.py
│   └── image_mapper.py
│
├── llm/
│   ├── ddr_generator.py
│   └── prompt_template.txt
│
├── report/
│   └── docx_builder.py
│
├── utils/
│   └── pdf_utils.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/span551/ai-ddr-system.git
cd ai-ddr-system
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Set API Key

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_api_key_here"
```

---

### 4️⃣ Run Locally

```bash
streamlit run app.py
```

---

## 🌐 Deployment

Deployed using **Streamlit Cloud**:

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Select repo + `app.py`
4. Add `GROQ_API_KEY` in secrets
5. Deploy 🚀

---

## 📊 Output Structure (DDR)

The generated report includes:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

---

## ⚠️ Key Design Decisions

* ✅ **Page-based image extraction** → ensures reliability
* ✅ **JSON intermediate output** → prevents LLM hallucination
* ✅ **Rule-based image mapping** → deterministic & stable
* ✅ **Validator layer** → handles missing/conflicting data

---

## 🧠 Challenges & Solutions

| Challenge                       | Solution                               |
| ------------------------------- | -------------------------------------- |
| PDF image extraction unreliable | Converted full pages to images         |
| Cloud path issues               | Used absolute paths + temp directories |
| LLM formatting inconsistency    | Forced structured JSON output          |
| Missing thermal data            | Explicitly marked as "Not Available"   |

---

## 🏆 What This Project Demonstrates

* Real-world **AI system design**
* Handling **imperfect/unstructured data**
* Combining **rule-based + LLM approaches**
* Building **production-ready pipelines**
* Deploying **AI apps on cloud**

---

## 📌 Future Improvements

* 🔍 Smart image-to-area mapping (AI-based)
* 🧠 Severity prediction using ML
* 📊 Dashboard view before report generation
* 📄 PDF export support
* 🧬 Image classification (thermal vs inspection)

---

## 👨‍💻 Author

Your Name
GitHub: https://github.com/your-username

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps!
