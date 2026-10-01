"""Open-path tape: list keeps pin, detail zeros tape_m; live allowance restamp."""
from __future__ import annotations
from copy import deepcopy


def open_drop_tape(result: dict, live_allowance: float | None = None, view: str = "detail") -> dict:
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if not out.get("tape_on"):
        return out
    if out.get("list_tape_m") is None:
        out["list_tape_m"] = out.get("tape_m")
    if view == "list":
        if live_allowance is not None:
            out["tape_allowance_m"] = float(live_allowance)
        out["open_view"] = "list"
        return out
    out["tape_m"] = 0
    if live_allowance is not None:
        out["tape_allowance_m"] = float(live_allowance)
    out["open_tape_dropped"] = True
    out["open_view"] = "detail"
    return out


def tape_projection(result: dict) -> dict:
    if not isinstance(result, dict):
        return {}
    return {
        "tape_on": result.get("tape_on"),
        "tape_allowance_m": result.get("tape_allowance_m"),
        "tape_m": result.get("tape_m"),
        "list_tape_m": result.get("list_tape_m"),
        "paper_m2": result.get("paper_m2"),
        "open_tape_dropped": bool(result.get("open_tape_dropped")),
    }
