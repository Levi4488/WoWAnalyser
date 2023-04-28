def test_redirect(client):
    response = client.post(
        '/index', data={"reportCode": "kdq7bp4wfLgT9WhY"}, follow_redirects=True)
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # check that the path changed
    assert response.request.path == '/boss-selection'
