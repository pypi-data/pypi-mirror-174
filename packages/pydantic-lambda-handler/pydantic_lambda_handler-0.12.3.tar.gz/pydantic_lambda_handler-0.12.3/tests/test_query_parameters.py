def test_no_query(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query")
    assert response.status_code == 200, response.json()
    assert response.json() == [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


def test_query(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query", params={"skip": 1})
    assert response.status_code == 200, response.json()
    assert response.json() == [{"item_name": "Bar"}, {"item_name": "Baz"}]


def test_missing_query(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query_required")
    assert response.status_code == 422, response.json()
    assert response.json() == {
        "detail": [{"loc": ["query", "secret"], "msg": "field required", "type": "value_error.missing"}]
    }


def test_query_param(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query_param", params={"meat": "solid"})
    assert response.status_code == 200, response.json()
    assert response.json() == {"sausages": "solid"}


def test_query_multivalue_param(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query_multivalue_param", params={"sausages": [5, 6, 7, 8]})
    assert response.status_code == 200, response.json()
    assert response.json() == {"sausages": [5, 6, 7, 8]}


def test_query_param_float(requests_client, base_url):
    response = requests_client.get(f"{base_url}/query_float", params={"item_name": "4"})
    assert response.status_code == 200, response.json()
    assert response.json() == {"item_name": 4.0}
