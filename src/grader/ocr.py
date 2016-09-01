"""OCR utilities.

Uses Tesseract via pytesseract if installed. For demo or non-image environments,
falls back to reading pre-extracted answers from JSON files.
"""
import json
import os
from typing import Dict, Any, Optional

try:
    import pytesseract  # type: ignore
    from PIL import Image
    TESS_AVAILABLE = True
except Exception:
    TESS_AVAILABLE = False

def extract_short_answers_from_image(image_path: str) -> Dict[str, str]:
    """Very simplified OCR stub.
    In a real setup (2014–2018 style), you'd template the answer boxes and crop them before OCR.
    Here we run OCR over the whole image as a placeholder.
    """
    if not TESS_AVAILABLE:
        raise RuntimeError("Tesseract is not available in this environment.")
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    # Extremely naive parser: expect lines like 'Q1: answer text'
    answers = {}
    for line in text.splitlines():
        line = line.strip()
        if len(line) < 3 or ":" not in line:
            continue
        qid, ans = line.split(":", 1)
        qid = qid.strip()
        ans = ans.strip()
        if qid and ans:
            answers[qid] = ans
    return answers

def load_answers_from_json(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_json_fallback(ocr_fallback_dir: Optional[str], student_stub: str) -> Optional[str]:
    """Returns path to JSON if present, else None."""
    if not ocr_fallback_dir:
        return None
    candidate = os.path.join(ocr_fallback_dir, f"{student_stub}.json")
    return candidate if os.path.exists(candidate) else None
