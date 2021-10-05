import json

def test_validate(client):

    response = client.get(path="/validate?numbers=100000000020000000003000000000400000000050000000006000000000700000000080000000009")

    assert response.json.get("is_valid") == True

    response = client.get(path="/validate?numbers=100000000010000000003000000000400000000050000000006000000000700000000080000000009")

    assert response.json.get("is_valid") == False