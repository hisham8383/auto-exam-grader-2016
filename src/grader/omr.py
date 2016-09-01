"""OMR utilities (bubble detection).

This is a **template-driven** OMR: we assume fixed positions for bubbles per question.
To keep it 2014–2018 style and simple, we don't rely on ML — we sample grayscale
intensity at expected bubble centers and treat 'darker' as filled.

For a real deployment, calibrate positions using fiducial marks on the sheet.
"""
from typing import Dict, List, Tuple

def detect_bubbles_from_template(image_path: str, template: Dict[str, List[Tuple[int,int]]]):
    """Stub implementation: returns the first option for each question to simulate OMR.
    Replace with OpenCV/Pillow sampling where you test pixel intensity around each (x,y).
    """
    results = {}
    for qid, centers in template.items():
        # naive: choose index 0 as 'filled'
        idx = 0
        results[qid] = idx
    return results
