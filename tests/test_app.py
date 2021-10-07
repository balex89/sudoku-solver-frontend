def test_validate(client):
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype
    }
    response = client.get(path="/validate",
                          query_string={"numbers": "10000000"
                                                   "020000000"
                                                   "003000000"
                                                   "000400000"
                                                   "000050000"
                                                   "000006000"
                                                   "000000700"
                                                   "000000080"
                                                   "000000009"},
                          headers=headers)
    assert isinstance(response.json.get("is_valid"), bool) is True
    assert response.status_code == 200
    assert response.mimetype == mimetype
