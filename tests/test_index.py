from flask import session


def test_index(client):
    with client:
        response = client.post("/index", data={"reportCode": "kdq7bp4wfLgT9WhY"}, follow_redirects=True)
        # session is still accessible
        assert session["reportCode"] == "kdq7bp4wfLgT9WhY"
        # Check that there was one redirect response.
        assert len(response.history) == 1
        # check that the path changed
        assert response.request.path == '/boss-selection'
        assert response.status_code == 200
        assert response.get_data(as_text=True)
    # session is no longer accessible
    