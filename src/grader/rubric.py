"""Rubric and scoring utilities (MCQ + Short Answer)."""
from typing import Dict, Any, List, Tuple
import difflib
import yaml

def load_rubric(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def score_mcq(student_choice: str, correct_choice: str, points: float = 1.0) -> Tuple[float, Dict[str, Any]]:
    earned = points if student_choice.strip() == correct_choice.strip() else 0.0
    return earned, {"expected": correct_choice, "got": student_choice, "points": earned}

def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def score_short_answer(student_answer: str, expected_answer: str, keywords_any: List[str], min_similarity: float, points: float = 1.0):
    sim = similarity(student_answer, expected_answer)
    keyword_hit = any(kw.lower() in student_answer.lower() for kw in (keywords_any or []))
    earned = points if (sim >= min_similarity or keyword_hit) else 0.0
    return earned, {"similarity": round(sim, 3), "keyword_hit": keyword_hit, "expected": expected_answer, "got": student_answer, "points": earned}
