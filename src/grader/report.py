"""Reporting helpers: CSV + simple HTML."""
import os, json
import pandas as pd
from typing import List, Dict, Any

def write_csv(results: List[Dict[str, Any]], out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for r in results:
        flat = {
            "student_id": r["student_id"],
            "exam_id": r["exam_id"],
            "total_score": r["total_score"],
        }
        rows.append(flat)
    df = pd.DataFrame(rows)
    csv_path = os.path.join(out_dir, "summary.csv")
    df.to_csv(csv_path, index=False)
    return csv_path

def write_json(results: List[Dict[str, Any]], out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "details.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return path

def write_html(results: List[Dict[str, Any]], out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    html_rows = []
    for r in results:
        html_rows.append(f"""<tr>
<td>{r['student_id']}</td>
<td>{r['exam_id']}</td>
<td>{r['total_score']}</td>
<td><pre style='white-space: pre-wrap'>{json.dumps(r['details'], ensure_ascii=False)}</pre></td>
</tr>""")
    html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Results</title>
<style>table{{border-collapse:collapse}}td,th{{border:1px solid #ddd;padding:8px}}</style>
</head><body>
<h1>Exam Results</h1>
<table>
<thead><tr><th>Student</th><th>Exam</th><th>Total</th><th>Details</th></tr></thead>
<tbody>
{''.join(html_rows)}
</tbody></table>
</body></html>"""
    path = os.path.join(out_dir, "results.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path
