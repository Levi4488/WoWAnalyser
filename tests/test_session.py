from flask import session


def test_access_session(client):
    with client:
        client.post("/index", data={"reportCode": "kdq7bp4wfLgT9WhY"})
        # session is still accessible
        assert session["reportCode"] == "kdq7bp4wfLgT9WhY"

    # session is no longer accessible