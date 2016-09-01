import click
import os
from . import storage
from .pipeline import run_pipeline

@click.group()
def cli():
    """Automated Exam Paper Grader (2014–2018 style)"""
    pass

@cli.command("init-db")
@click.option("--db", "db_path", default="grader.sqlite3", help="SQLite DB path")
def init_db(db_path):
    conn = storage.connect(db_path)
    storage.init_db(conn)
    click.echo(f"Initialized DB at {db_path}")

@cli.command("grade")
@click.option("--exam-id", required=True, help="Exam ID (e.g. cs101_midterm)")
@click.option("--scans", "scans_dir", default="./sample_data/scans", help="Directory with scan images")
@click.option("--ocr-fallback", "ocr_fallback_dir", default=None, help="Directory with OCR JSON fallbacks")
@click.option("--rubric", "rubric_path", required=True, help="Rubric YAML path")
@click.option("--answer-key", "answer_key_path", required=True, help="Answer key JSON path")
@click.option("--db", "db_path", default="grader.sqlite3", help="SQLite DB path")
@click.option("--out", "out_dir", default="reports", help="Reports directory")
@click.option("--students", multiple=True, help="Explicit list of student stubs (omit to infer from OCR JSON)")
def grade_cmd(exam_id, scans_dir, ocr_fallback_dir, rubric_path, answer_key_path, db_path, out_dir, students):
    students_list = list(students) if students else None
    outputs = run_pipeline(
        exam_id=exam_id,
        scans_dir=scans_dir,
        rubric_path=rubric_path,
        answer_key_path=answer_key_path,
        ocr_fallback_dir=ocr_fallback_dir,
        db_path=db_path,
        out_dir=out_dir,
        students=students_list
    )
    click.echo(f"Wrote: {outputs}")

if __name__ == "__main__":
    cli()
