def test_retribution_overview(client):
    with client.session_transaction() as session:
        # set a report code without going through the index route
        session["reportCode"] = "kdq7bp4wfLgT9WhY"
        session['sourceId'] = "7"
        session['bossStartTime'] = "10305"
        session['bossEndTime'] = "36377"
        session['totalTime'] = 26072
        session['bossEncounterId'] = "2582"
        session['bossDifficulty'] = "Normal"
        session['bossName'] = "Leymor"
        session['playerName'] = "Levypal"
        session['playerType'] = "Paladin"
        session['playerSpec'] = "Retribution"
        session['playerItemLevel'] = "372"
        session['playerPotionUse'] = "0"
        session['playerHealthstoneUse'] = "0"
    # session is saved now
    response = client.get("/retribution-overview")
    assert response.status_code == 200
    assert response.get_data(as_text=True)