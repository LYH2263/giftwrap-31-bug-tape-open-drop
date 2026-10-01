from pydantic import BaseModel, Field

class EstimateRequest(BaseModel):
    box_id: int
    overlap: float | None = None
    wrap_style: str = "cross"
    save: bool = False
    note: str = ""
    tape: bool = False
    tape_allowance_m: float | None = Field(default=None, ge=0)
