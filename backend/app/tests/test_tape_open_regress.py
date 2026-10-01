"""Regression: opening a saved run (list or detail) must keep the pinned tape values.

The read path used to zero tape_m on detail open and restamp the allowance
from live settings; these tests pin the fixed behavior.
"""
from app.services.tape_open_view import pinned_run_view, tape_projection


def test_open_keeps_pinned_tape_when_on():
    raw = {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}
    out = pinned_run_view(raw)
    assert out["tape_on"] is True
    assert out["tape_m"] == 1.25
    assert out["tape_allowance_m"] == 0.1
    assert out["paper_m2"] == 0.31
    # the stored payload is never mutated by the read path
    assert raw == {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}


def test_projection_mirrors_pinned_tape():
    raw = {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}
    assert tape_projection(raw) == {
        "tape_on": True,
        "tape_allowance_m": 0.1,
        "tape_m": 1.25,
        "paper_m2": 0.31,
    }


def test_tape_off_runs_read_back_zero():
    raw = {"tape_on": False, "tape_m": 0, "tape_allowance_m": None, "paper_m2": 0.31}
    out = pinned_run_view(raw)
    assert out["tape_on"] is False
    assert out["tape_m"] == 0
    assert out["tape_allowance_m"] is None
