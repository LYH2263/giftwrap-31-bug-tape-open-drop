from app.engines.wrap_math import paper_area, ribbon_estimate, tape_estimate
import pytest

def test_book_box():
    r = paper_area(0.30, 0.20, 0.15, 1.15)
    assert r["box_surface"] == 0.27
    assert r["paper_m2"] == 0.31

def test_ribbon_cross():
    rb = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    assert rb["ribbon_m"] > 0.5

def test_tape_formula():
    t = tape_estimate(0.30, 0.20, 0.2)
    assert t["tape_m"] == 1.2
    assert t["allowance_m"] == 0.2

def test_tape_zero_allowance():
    assert tape_estimate(0.30, 0.20, 0)["tape_m"] == 1.0

def test_tape_uses_only_length_and_width():
    # height is not even an input to the tape formula
    assert tape_estimate(0.30, 0.20, 0.1)["tape_m"] == 1.1

def test_tape_negative_allowance():
    with pytest.raises(ValueError):
        tape_estimate(0.30, 0.20, -0.01)
