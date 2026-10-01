from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(box_id: int = Query(...), overlap: float | None = None, wrap_style: str = "cross",
            save: bool = False, tape: bool = Query(False),
            tape_allowance_m: float | None = Query(None, ge=0)):
    return estimate_service.run_estimate(box_id, overlap, wrap_style, save, "", tape, tape_allowance_m)
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(
        body.box_id, body.overlap, body.wrap_style, body.save, body.note,
        body.tape, body.tape_allowance_m)
