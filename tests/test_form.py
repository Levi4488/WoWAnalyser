def test_form(client):
    response = client.get("/index", data={
        "reportCode": "kdq7bp4wfLgT9WhY"
    })
    assert response.status_code == 200
    assert response.get_data(as_text=True)