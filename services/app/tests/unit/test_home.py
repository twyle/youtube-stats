
def test_health_check(test_client):
    response = test_client.get('/')

    assert response.status_code == 200
