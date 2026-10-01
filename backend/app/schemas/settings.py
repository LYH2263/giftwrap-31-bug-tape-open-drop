from pydantic import BaseModel, Field

class SettingsUpdate(BaseModel):
    overlap: float | None = Field(default=None, gt=0)
    tape_allowance_m: float | None = Field(default=None, ge=0)
