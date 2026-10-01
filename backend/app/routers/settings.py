from fastapi import APIRouter
from app.schemas.settings import SettingsUpdate
from app.repositories import settings_repo
router = APIRouter()
@router.get("/settings")
def settings(): return settings_repo.get_all()
@router.put("/settings")
def update_settings(body: SettingsUpdate):
    if body.overlap is not None:
        settings_repo.set_setting("overlap", body.overlap)
    if body.tape_allowance_m is not None:
        settings_repo.set_setting("tape_allowance_m", body.tape_allowance_m)
    return settings_repo.get_all()
