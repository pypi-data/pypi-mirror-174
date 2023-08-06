def test_error(requests_client, base_url):
    response = requests_client.get(f"{base_url}/error")
    assert response.status_code == 418, response.json()
    assert response.json() == {"detail": [{"msg": "nope", "type": "ValueError"}]}
