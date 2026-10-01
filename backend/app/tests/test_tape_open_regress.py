"""Regression: opening a saved run (list or detail) must serve the pinned
write-time tape values — never zeroed, never restamped from live settings."""
from app.services.tape_open_view import pinned_tape_view, tape_projection


def test_detail_open_keeps_pinned_tape_when_on():
    raw = {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}
    out = pinned_tape_view(raw)
    assert out["tape_on"] is True
    assert out["tape_m"] == 1.25
    assert out["tape_allowance_m"] == 0.1


def test_open_never_mutates_the_stored_record():
    raw = {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}
    pinned_tape_view(raw)
    tape_projection(raw)
    assert raw == {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}


def test_projection_mirrors_pinned_values():
    raw = {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}
    proj = tape_projection(raw)
    assert proj == {"tape_on": True, "tape_allowance_m": 0.1, "tape_m": 1.25, "paper_m2": 0.31}


def test_tape_off_reads_back_zero():
    raw = {"tape_on": False, "tape_m": 0, "tape_allowance_m": None, "paper_m2": 0.31}
    out = pinned_tape_view(raw)
    assert out["tape_on"] is False
    assert out["tape_m"] == 0
    assert tape_projection(raw)["tape_m"] == 0
