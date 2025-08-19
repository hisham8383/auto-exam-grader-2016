# Automated Exam Paper Grading System

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)
[![Tesseract OCR](https://img.shields.io/badge/OCR-Tesseract-purple.svg)](https://github.com/tesseract-ocr/tesseract)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A lightweight **rule‑based grading pipeline** that digitizes scanned exam sheets, extracts answers (OCR/OMR), applies a rubric, and generates reports. Designed to showcase practical automation of academic workflows and digital transformation.

> **Context:** Built originally to automate grading workflows in higher education. In practice, this approach **cut turnaround time by \~80%** versus manual grading in large courses.

---

## 🔧 Features

* **OCR (short answers):** Tesseract via `pytesseract` with a JSON fallback for demos.
* **OMR (multiple choice):** Template/grid‑based bubble reading (deterministic; no ML).
* **Rubric engine:** MCQ + short answer (keyword match + `difflib` similarity).
* **Storage & reports:** SQLite persistence; CSV/JSON/HTML reports.
* **Interfaces:** CLI with `click`, optional Flask web UI for uploads/results.

---

## 📸 Screenshot / Demo

Add a screenshot or GIF here to make the repo pop on first view:

```
/docs/screenshot.png
/docs/demo.gif
```

---

## 📁 Project Structure

```
exam-grader/
├─ README.md
├─ requirements.txt
├─ rubrics/
│  ├─ cs101_midterm.yaml
│  └─ cs101_mcq.yaml
├─ sample_data/
│  ├─ key/cs101_midterm_key.json
│  └─ ocr_output/sample_short_001.json
├─ src/
│  ├─ grader/               # OCR/OMR, rubric engine, pipeline, storage, reports
│  └─ webapp/               # Minimal Flask app (upload + results)
├─ tests/
└─ reports/
```

---

## 🚀 Quickstart

### 1) Install system deps (optional for live OCR)

**macOS**

```bash
brew install tesseract
```

**Ubuntu/Debian**

```bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr
```

### 2) Install Python deps

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Initialize DB

```bash
python -m src.grader.cli init-db
```

### 4) Grade (demo using JSON fallback)

```bash
python -m src.grader.cli grade \
  --exam-id cs101_midterm \
  --scans ./sample_data/scans \
  --ocr-fallback ./sample_data/ocr_output \
  --rubric ./rubrics/cs101_midterm.yaml \
  --answer-key ./sample_data/key/cs101_midterm_key.json
```

Outputs will appear in `./reports` (CSV/JSON/HTML), results saved to `grader.sqlite3`.

### 5) Web UI (optional)

```bash
FLASK_APP=src/webapp/app.py flask run
# open http://127.0.0.1:5000
```

---

## 🧠 How It Works

1. **Ingestion:** Read scans (PNG/JPG) or JSON fallback.
2. **Extraction:** OCR short answers; OMR bubble detection via template.
3. **Scoring:** Apply rubric + answer key (MCQ and short answer).
4. **Storage & Reporting:** Persist to SQLite; export CSV/JSON/HTML.

---

## 🛠️ CLI Reference

```bash
# Initialize the local SQLite database
python -m src.grader.cli init-db --db grader.sqlite3

# Grade an exam batch
python -m src.grader.cli grade \
  --exam-id cs101_midterm \
  --scans ./sample_data/scans \
  --ocr-fallback ./sample_data/ocr_output \
  --rubric ./rubrics/cs101_midterm.yaml \
  --answer-key ./sample_data/key/cs101_midterm_key.json \
  --db grader.sqlite3 \
  --out reports \
  --students sample_short_001
```

---

## 🧪 Tests

```bash
pytest -q
```

---

## 🗺️ Roadmap

* Add multi‑select MCQ & numeric tolerance rubric types
* Improve OMR with OpenCV sampling around bubble centers
* GitHub Actions CI (pytest) + badges
* Docker Compose demo with Tesseract installed

---

## 📚 Tech Stack

* **Python 3.6+**, **Flask**
* **Tesseract OCR** (`pytesseract`)
* **SQLite**, **pandas** for reporting
* **PyYAML**, **click** for DX

---

## 📝 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE).

---

## 🙌 Acknowledgments

* Inspired by early EdTech automation approaches.
* Thanks to the open‑source Tesseract community.
