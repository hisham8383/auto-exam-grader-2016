from flask import Flask, render_template, request, redirect, url_for
import os, json
from ..grader.pipeline import run_pipeline

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # minimal: write uploaded file if provided
        file = request.files.get('scan')
        stub = request.form.get('student_stub', 'sample_short_001')
        scans_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sample_data/scans'))
        os.makedirs(scans_dir, exist_ok=True)
        if file and file.filename:
            out_path = os.path.join(scans_dir, file.filename)
            file.save(out_path)
        # Run pipeline in demo mode (OCR JSON)
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        outputs = run_pipeline(
            exam_id='cs101_midterm',
            scans_dir=scans_dir,
            rubric_path=os.path.join(base, 'rubrics/cs101_midterm.yaml'),
            answer_key_path=os.path.join(base, 'sample_data/key/cs101_midterm_key.json'),
            ocr_fallback_dir=os.path.join(base, 'sample_data/ocr_output'),
            db_path=os.path.join(base, 'grader.sqlite3'),
            out_dir=os.path.join(base, 'reports'),
            students=[stub]
        )
        return redirect(url_for('results'))
    return render_template('upload.html')

@app.route('/results')
def results():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    details_path = os.path.join(base, 'reports/details.json')
    data = []
    if os.path.exists(details_path):
        with open(details_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    return render_template('results.html', results=data)

# Jinja layout base
@app.context_processor
def inject_layout():
    return {}
