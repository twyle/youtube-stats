import json

def test_register_user_no_data(test_client):
    resp = test_client.post('/api/v1/auth/register', json={})
    assert resp.status_code == 400
    
def test_register_user_incomplete_data(test_client, generate_user_no_email):
    resp = test_client.post('/api/v1/auth/register', json=generate_user_no_email)
    assert resp.status_code == 400
    
def test_register_user(test_client, generate_user_data):
    resp = test_client.post('/api/v1/auth/register', json=generate_user_data)
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data['first_name'] == generate_user_data['first_name']
    assert data['last_name'] == generate_user_data['last_name']
    assert data['email_address'] == generate_user_data['email_address']
    assert 'password' not in data
    assert 'activation_token' in data
    
def test_register_duplicate_user(test_client):
    user_data = {
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'email_address': 'test@gmail.com',
        'password': 'test'
    }
    resp = test_client.post('/api/v1/auth/register', json=user_data)
    assert resp.status_code == 201
    resp = test_client.post('/api/v1/auth/register', json=user_data)
    assert resp.status_code == 409
