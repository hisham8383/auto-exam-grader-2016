from src.grader import rubric as R

def test_similarity_basic():
    assert R.similarity('abc', 'abc') == 1.0
    assert R.similarity('abc', 'abd') > 0.5

def test_score_mcq():
    pts, meta = R.score_mcq('A', 'A', 1.0)
    assert pts == 1.0
    pts2, meta2 = R.score_mcq('B', 'A', 1.0)
    assert pts2 == 0.0

def test_score_short_answer():
    pts, meta = R.score_short_answer('keeps order of equals', 'does not change the relative order of equal elements', ['relative order','equal elements'], 0.4, 1.0)
    assert pts == 1.0
