def test_player_selection(client):
    with client.session_transaction() as session:
        # set a report code without going through the index route
        session["reportCode"] = "kdq7bp4wfLgT9WhY"
        session['bossStartTime'] = "10305"
        session['bossEndTime'] = "36377"
        session['bossEncounterId'] = "2582"
        session['bossName'] = "Leymor"
        session['bossDifficulty'] = "Normal"
        session['time'] = "00:26"
        session['averageItemLevel'] = "332"
    # session is saved now
    response = client.post("/player-selection", data={"sourceId": "7", "playerName": "Levypal", "playerType": "Paladin",
                           "playerSpec": "Retribution", "playerItemLevel": "372", "playerPotionUse": "0", "playerHealthstoneUse": "0"}, follow_redirects=True)
    assert session["reportCode"] == "kdq7bp4wfLgT9WhY"
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # check that the path changed
    assert response.request.path == '/retribution-overview'
    assert response.status_code == 200
    assert response.get_data(as_text=True)