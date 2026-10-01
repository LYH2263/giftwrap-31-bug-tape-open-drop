from fastapi import HTTPException
from app.engines.wrap_math import paper_area, ribbon_estimate, tape_estimate
from app.repositories import boxes, history, settings_repo

def run_estimate(box_id: int, overlap: float | None, wrap_style: str, save: bool, note: str,
                 tape: bool = False, tape_allowance_m: float | None = None):
    box = boxes.get_box(box_id)
    if not box:
        raise HTTPException(404)
    if box.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty box")
    ov = float(overlap) if overlap is not None else settings_repo.get_overlap()
    calc = paper_area(box["length"], box["width"], box["height"], ov)
    ribbon = ribbon_estimate(box["length"], box["width"], box["height"], wrap_style)
    if tape:
        # Freeze the resolved numeric allowance (never None/"default") so later
        # settings changes cannot recompute a saved run.
        eff = float(tape_allowance_m) if tape_allowance_m is not None else settings_repo.get_tape_allowance_m()
        if eff < 0:
            raise HTTPException(422, "negative tape allowance")
        t = tape_estimate(box["length"], box["width"], eff)
        tape_part = {"tape_on": True, "tape_allowance_m": eff, "tape_m": t["tape_m"]}
    else:
        tape_part = {"tape_on": False, "tape_allowance_m": None, "tape_m": 0}
    payload = {**calc, "ribbon": ribbon, "box_id": box_id, **tape_part}
    # Insert stays the last step: any validation failure above leaves no row.
    run_id = history.insert_run(box_id, ov, payload, note) if save else None
    return {"box": box, "run_id": run_id, **calc, "ribbon": ribbon, **tape_part}
