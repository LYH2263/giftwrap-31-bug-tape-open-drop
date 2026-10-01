"""Open-path tape: list and detail both serve the write-time pinned values.

tape_on / tape_allowance_m / tape_m are frozen when the run is inserted.
Reading a run back — list summary or detail open — must never recompute them
from live settings, and must never zero tape_m while tape_on is still true.
"""
from __future__ import annotations
from copy import deepcopy


def pinned_tape_view(result: dict) -> dict:
    """Return the stored result exactly as written (defensive copy only)."""
    if not isinstance(result, dict):
        return result
    return deepcopy(result)


def tape_projection(result: dict) -> dict:
    """Detail projection: the pinned tape fields exactly as written."""
    if not isinstance(result, dict):
        return {}
    return {
        "tape_on": result.get("tape_on"),
        "tape_allowance_m": result.get("tape_allowance_m"),
        "tape_m": result.get("tape_m"),
        "paper_m2": result.get("paper_m2"),
    }
