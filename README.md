# Automated Exam Paper Grading System (2014–2018 style)

A lightweight, **rule-based grading pipeline** that digitizes scanned exam sheets, extracts answers, applies a rubric, and generates reports. 
This repo reflects technologies and approaches common in the **2014–2018** timeframe (Python 3.6/3.7, Tesseract OCR, Flask).

> Origin: Built as a university project at UMass to **reduce grading time by ~80%** by automating scanning, OCR/OMR, rubric scoring, and report generation.

---

## Features

- **OCR** of short-answer fields via [Tesseract](https://github.com/tesseract-ocr/tesseract) (with a JSON fallback for demos).
- **OMR** (bubble detection) via simple template/grid sampling (no ML; deterministic and explainable).
- **Rubric engine** supporting:
  - Multiple Choice (single answer)
  - Short Answer (keyword & similarity via `difflib`)
- **SQLite** storage (portable DB) and **CSV/HTML** reports.
- **CLI** (via `click`) and a minimal **Flask** web UI for uploads and results view.

## Repo Layout

```
exam-grader-2018/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ LICENSE
├─ docker/
│  └─ Dockerfile
├─ rubrics/
│  ├─ cs101_midterm.yaml
│  └─ cs101_mcq.yaml
├─ sample_data/
│  ├─ scans/                # (Put PNG/JPG scans here if using real OCR/OMR)
│  ├─ key/
│  │  └─ cs101_midterm_key.json
│  └─ ocr_output/           # Demo JSON extracted answers (fallback to run end-to-end)
│     └─ sample_short_001.json
├─ src/
│  ├─ grader/
│  │  ├─ __init__.py
│  │  ├─ version.py
│  │  ├─ ocr.py
│  │  ├─ omr.py
│  │  ├─ rubric.py
│  │  ├─ storage.py
│  │  ├─ report.py
│  │  ├─ pipeline.py
│  │  └─ cli.py
│  └─ webapp/
│     ├─ app.py
│     ├─ static/styles.css
│     └─ templates/{index,upload,results}.html
├─ tests/
│  ├─ test_rubric.py
│  ├─ test_pipeline.py
│  └─ test_omr.py
└─ reports/
```

## Quickstart

### 1) Python & Tesseract
- Python **3.6+** (tested 3.10 too).
- Install Tesseract on your OS (if you want live OCR). Otherwise the pipeline can run on the **JSON demo**.

**macOS (brew):**
```
brew install tesseract
```
**Ubuntu/Debian:**
```
sudo apt-get update && sudo apt-get install -y tesseract-ocr
```

### 2) Install Python deps
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Initialize DB
```
python -m src.grader.cli init-db
```

### 4) Run grading (demo JSON fallback)
```
python -m src.grader.cli grade --exam-id cs101_midterm \
  --scans ./sample_data/scans \
  --ocr-fallback ./sample_data/ocr_output \
  --rubric ./rubrics/cs101_midterm.yaml \
  --answer-key ./sample_data/key/cs101_midterm_key.json
```

Reports are written to `./reports` and results persisted in `./grader.sqlite3`.

### 5) Web UI (optional)
```
FLASK_APP=src/webapp/app.py flask run
# open http://127.0.0.1:5000
```

## How it works

1. **Ingestion:** Scans are read (PNG/JPG) and optionally **OCR/OMR** applied.
2. **Scoring:** Answers compared to **Rubric** and **Answer Key** (MCQ + Short Answer).
3. **Storage:** Results stored in **SQLite**.
4. **Reporting:** CSV and simple HTML generated in `./reports`.

> Design choice: This project intentionally avoids heavy ML to mirror a **2014–2018** university project—favoring deterministic, maintainable code with clear rules.

## Demo Data

`sample_data/ocr_output/sample_short_001.json` contains a single student's parsed answers to demonstrate the pipeline without Tesseract.

## Academic Integrity & Notes

- This repo is for showcasing **digital transformation** skills (automation, OCR/OMR, data pipelines) typical of the 2014–2018 era.
- You can expand with additional rubric types (multi-select, numeric ranges) and add real scans to run end-to-end.

---

© 2025 Hisham Alhussain. Licensed under MIT.
