def test_with_headers(requests_client, base_url):
    headers = {"user_agent": "user_123"}
    response = requests_client.get(f"{base_url}/with_headers", headers=headers)
    assert response.status_code == 200, response.json()
    assert response.json() == {"user_agent": "user_123"}


def test_with_headers_default(requests_client, base_url):
    response = requests_client.get(f"{base_url}/with_headers")
    assert response.status_code == 200, response.json()
    assert response.json() == {"user_agent": None}


def test_with_header_alias(requests_client, base_url):
    headers = {"UserId": "user_123"}
    response = requests_client.get(f"{base_url}/with_headers_alias", headers=headers)
    assert response.status_code == 200, response.json()
    assert response.json() == {"user_agent": "user_123"}
