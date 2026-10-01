"""Regression that currently asserts the buggy open-path zeros tape_m on detail."""
from app.services.tape_open_view import open_drop_tape


def test_detail_open_zeros_tape_when_on():
    raw = {"tape_on": True, "tape_m": 1.25, "tape_allowance_m": 0.1, "paper_m2": 0.31}
    out = open_drop_tape(raw, view="detail")
    assert out["tape_on"] is True
    assert out["tape_m"] == 0
