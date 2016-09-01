from src.grader import omr

def test_omr_stub():
    tpl = {'Q1': [(10,10),(20,10),(30,10)], 'Q2': [(10,20),(20,20),(30,20)]}
    res = omr.detect_bubbles_from_template('dummy.png', tpl)
    assert res['Q1'] == 0 and res['Q2'] == 0
