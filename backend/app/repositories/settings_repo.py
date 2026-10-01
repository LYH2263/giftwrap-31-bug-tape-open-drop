from app.config import DEFAULT_OVERLAP, DEFAULT_TAPE_ALLOWANCE
from app.db import connect

def get_all():
    c = connect()
    try:
        d = {r["key"]: r["value"] for r in c.execute("SELECT key,value FROM settings").fetchall()}
        d.setdefault("overlap", str(DEFAULT_OVERLAP))
        d.setdefault("tape_allowance_m", str(DEFAULT_TAPE_ALLOWANCE))
        return d
    finally:
        c.close()

def get_overlap():
    return float(get_all().get("overlap", DEFAULT_OVERLAP))

def get_tape_allowance_m():
    return float(get_all().get("tape_allowance_m", DEFAULT_TAPE_ALLOWANCE))

def set_setting(key: str, value: float):
    c = connect()
    try:
        c.execute(
            "INSERT INTO settings(key,value) VALUES(?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value)),
        )
        c.commit()
    finally:
        c.close()
