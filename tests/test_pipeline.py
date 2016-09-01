from src.grader.pipeline import run_pipeline
import os, json

def test_pipeline_demo(tmp_path):
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    outputs = run_pipeline(
        exam_id='cs101_midterm',
        scans_dir=os.path.join(base, 'sample_data/scans'),
        rubric_path=os.path.join(base, 'rubrics/cs101_midterm.yaml'),
        answer_key_path=os.path.join(base, 'sample_data/key/cs101_midterm_key.json'),
        ocr_fallback_dir=os.path.join(base, 'sample_data/ocr_output'),
        db_path=os.path.join(tmp_path, 'grader.sqlite3'),
        out_dir=os.path.join(tmp_path, 'reports'),
        students=['sample_short_001']
    )
    assert os.path.exists(outputs['json'])
