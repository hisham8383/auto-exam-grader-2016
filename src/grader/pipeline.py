"""End-to-end pipeline orchestration."""
import os, json, datetime
from typing import Dict, Any, List, Optional
from . import ocr as ocr_mod
from . import rubric as rubric_mod
from . import storage, report

def grade_student(
    student_stub: str,
    exam_id: str,
    rubric: Dict[str, Any],
    answer_key: Dict[str, Any],
    scans_dir: str,
    ocr_fallback_dir: Optional[str] = None,
) -> Dict[str, Any]:
    # Determine the student answers
    json_path = ocr_mod.detect_json_fallback(ocr_fallback_dir, student_stub)
    if json_path:
        data = ocr_mod.load_answers_from_json(json_path)
        student_id = data.get("student_id", student_stub)
        answers = data.get("answers", {})
    else:
        # Try OCR on image named {student_stub}.png or .jpg
        for ext in (".png", ".jpg", ".jpeg"):
            candidate = os.path.join(scans_dir, f"{student_stub}{ext}")
            if os.path.exists(candidate):
                answers = ocr_mod.extract_short_answers_from_image(candidate)
                student_id = student_stub
                break
        else:
            raise FileNotFoundError("No scan image or OCR fallback JSON found for " + student_stub)

    # Score
    points_per_question = rubric.get("points_per_question", 1)
    aq = answer_key["answers"]
    details = {}
    total = 0.0
    for q in rubric["questions"]:
        qid = q["id"]
        qtype = q["type"]
        student_answer = answers.get(qid, "")

        if qtype == "mcq":
            correct = aq[qid]
            earned, meta = rubric_mod.score_mcq(student_answer, correct, points_per_question)
        elif qtype == "short_answer":
            expected = aq[qid]
            kw = q.get("keywords_any", [])
            min_sim = float(q.get("min_similarity", 0.5))
            earned, meta = rubric_mod.score_short_answer(student_answer, expected, kw, min_sim, points_per_question)
        else:
            earned, meta = 0.0, {"error": f"Unknown type {qtype}"}

        details[qid] = {"answer": student_answer, **meta}
        total += earned

    return {
        "student_id": student_id,
        "exam_id": exam_id,
        "total_score": total,
        "details": details,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

def run_pipeline(
    exam_id: str,
    scans_dir: str,
    rubric_path: str,
    answer_key_path: str,
    ocr_fallback_dir: Optional[str] = None,
    db_path: str = "grader.sqlite3",
    out_dir: str = "reports",
    students: Optional[List[str]] = None
):
    rubric = rubric_mod.load_rubric(rubric_path)
    with open(answer_key_path, "r", encoding="utf-8") as f:
        answer_key = json.load(f)

    # If students list not provided, infer from OCR fallback JSONs
    if students is None and ocr_fallback_dir and os.path.isdir(ocr_fallback_dir):
        students = [os.path.splitext(f)[0] for f in os.listdir(ocr_fallback_dir) if f.endswith('.json')]

    results = []
    conn = storage.connect(db_path)
    storage.init_db(conn)
    storage.upsert_exam(conn, rubric.get("exam_id", exam_id), rubric.get("title", exam_id))

    for stub in (students or []):
        r = grade_student(stub, exam_id, rubric, answer_key, scans_dir, ocr_fallback_dir)
        storage.upsert_student(conn, r["student_id"])
        storage.insert_result(conn, r["student_id"], r["exam_id"], r["total_score"], json.dumps(r["details"]), r["created_at"])
        results.append(r)

    csv_path = report.write_csv(results, out_dir)
    json_path = report.write_json(results, out_dir)
    html_path = report.write_html(results, out_dir)

    return {"csv": csv_path, "json": json_path, "html": html_path, "count": len(results)}
