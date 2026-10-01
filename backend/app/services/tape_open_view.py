"""Read-path tape view: saved runs are pinned at write time.

List and detail both read the persisted result verbatim — tape_m,
tape_allowance_m and paper_m2 are never recomputed, zeroed, or restamped
from live settings when a run is opened. Changing the system default
allowance (or the tape default) afterwards must not reshape old runs.
"""
from __future__ import annotations
from copy import deepcopy


def pinned_run_view(result: dict) -> dict:
    """Return the stored run result verbatim (deep copy) for list and detail."""
    if not isinstance(result, dict):
        return result
    return deepcopy(result)


def tape_projection(result: dict) -> dict:
    """Detail projection: the pinned tape/paper values the run was written with."""
    if not isinstance(result, dict):
        return {}
    return {
        "tape_on": result.get("tape_on"),
        "tape_allowance_m": result.get("tape_allowance_m"),
        "tape_m": result.get("tape_m"),
        "paper_m2": result.get("paper_m2"),
    }
