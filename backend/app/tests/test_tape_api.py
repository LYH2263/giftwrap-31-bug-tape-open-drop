def test_tape_off_matches_legacy(client):
    c, _ = client
    r = c.get("/api/estimate?box_id=1")
    assert r.status_code == 200
    d = r.json()
    assert d["paper_m2"] == 0.31
    assert d["ribbon"]["ribbon_m"] == 2.2
    assert d["tape_on"] is False
    assert d["tape_allowance_m"] is None
    assert d["tape_m"] == 0


def test_tape_on_default_allowance(client):
    c, _ = client
    off = c.get("/api/estimate?box_id=1").json()
    on = c.get("/api/estimate?box_id=1&tape=true").json()
    assert on["tape_on"] is True
    assert on["tape_allowance_m"] == 0.2
    assert on["tape_m"] == 1.2
    # tape never merges into paper, and ribbon is untouched
    assert on["paper_m2"] == off["paper_m2"] == 0.31
    assert on["ribbon"] == off["ribbon"]


def test_tape_on_explicit_allowance(client):
    c, _ = client
    d = c.get("/api/estimate?box_id=1&tape=true&tape_allowance_m=0.35").json()
    assert d["tape_allowance_m"] == 0.35
    assert d["tape_m"] == 1.35
    assert d["paper_m2"] == 0.31


def test_negative_allowance_rejected_and_not_persisted(client):
    c, history = client
    r = c.post("/api/estimate", json={"box_id": 1, "save": True, "tape": True,
                                      "tape_allowance_m": -1})
    assert r.status_code == 422
    assert history.list_runs() == []
    # negative allowance is invalid input even with tape off
    assert c.post("/api/estimate", json={"box_id": 1, "tape": False,
                                         "tape_allowance_m": -1}).status_code == 422
    assert c.get("/api/estimate?box_id=1&tape=true&tape_allowance_m=-0.5").status_code == 422
    assert history.list_runs() == []


def test_saved_run_freezes_tape_and_paper(client):
    c, history = client
    r = c.post("/api/estimate", json={"box_id": 1, "save": True, "tape": True})
    assert r.status_code == 200
    run_id = r.json()["run_id"]
    saved = c.get(f"/api/runs/{run_id}").json()
    assert saved["result"]["tape_on"] is True
    assert saved["result"]["tape_allowance_m"] == 0.2
    assert saved["result"]["tape_m"] == 1.2
    assert saved["result"]["paper_m2"] == 0.31


def test_default_change_pins_history_and_dry_calc_corroborates(client):
    c, _ = client
    run_id = c.post("/api/estimate", json={"box_id": 1, "save": True, "tape": True}).json()["run_id"]

    put = c.put("/api/settings", json={"tape_allowance_m": 0.9})
    assert put.status_code == 200
    assert put.json()["tape_allowance_m"] == "0.9"

    # history detail stays pinned at write-time values
    saved = c.get(f"/api/runs/{run_id}").json()["result"]
    assert saved["tape_m"] == 1.2
    assert saved["tape_allowance_m"] == 0.2
    assert saved["paper_m2"] == 0.31
    # list view pins too
    listed = c.get("/api/runs").json()["items"][0]["result"]
    assert listed["tape_m"] == 1.2
    assert listed["paper_m2"] == 0.31

    # dry calc without allowance uses the new default
    assert c.get("/api/estimate?box_id=1&tape=true").json()["tape_m"] == 1.9
    # same params as saved -> dry calc matches the stored record (互证)
    again = c.get("/api/estimate?box_id=1&tape=true&tape_allowance_m=0.2").json()
    assert again["tape_m"] == saved["tape_m"]
    assert again["paper_m2"] == saved["paper_m2"]
    assert again["ribbon"]["ribbon_m"] == saved["ribbon"]["ribbon_m"]


def test_dirty_box_and_missing_run(client):
    c, history = client
    # box 3 is the seeded dirty box
    assert c.get("/api/estimate?box_id=3&tape=true").status_code == 422
    assert history.list_runs() == []
    assert c.get("/api/runs/9999").status_code == 404


def test_settings_rejects_negative(client):
    c, _ = client
    assert c.put("/api/settings", json={"tape_allowance_m": -0.1}).status_code == 422
    assert c.get("/api/settings").json()["tape_allowance_m"] == "0.2"
