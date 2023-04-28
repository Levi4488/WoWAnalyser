def test_boss_selection(client):
    with client.session_transaction() as session:
        # set a report code without going through the index route
        session["reportCode"] = "kdq7bp4wfLgT9WhY"
    # session is saved now
    response = client.post("/boss-selection", data={"bossName": "Leymor", "bossEncounterId": "2582", "bossDifficulty": "Normal",
                           "bossStartTime": "10305", "bossEndTime": "36377", "time": "00:26", "averageItemLevel": "332"},follow_redirects=True)
    assert session["reportCode"] == "kdq7bp4wfLgT9WhY"
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # check that the path changed
    assert response.request.path == '/player-selection'
    assert response.status_code == 200
    assert response.get_data(as_text=True)
