import json


# def test_activate_user_account_get_rather_post(test_client):
#     resp = test_client.post('/api/v1/auth/activate')
#     assert resp.status_code == 405

def test_activate_user_account_no_data(test_client):
    resp = test_client.get('/api/v1/auth/activate')
    assert resp.status_code == 400
    
def test_activate_user_account_invalid_id(test_client):
    resp = test_client.get('/api/v1/auth/activate?user_id=100&activation_token=fake_token')
    assert resp.status_code == 404
    
def test_activate_user_account(test_client):
    user_data = {
        'first_name': 'first_name_activate',
        'last_name': 'last_name_activate',
        'email_address': 'email_address_activate',
        'password': 'password'
    }
    resp = test_client.post('/api/v1/auth/register', json=user_data)
    assert resp.status_code == 201
    data = json.loads(resp.data)
    user_id = data['id']
    activation_token = data['activation_token']
    resp = test_client.get(f'/api/v1/auth/activate?user_id={user_id}&activation_token={activation_token}')
    assert resp.status_code == 200
    
def test_activate_active_account(test_client):
    user_data = {
        'first_name': 'first_name_activated',
        'last_name': 'last_name_activated',
        'email_address': 'activated@gmail.com',
        'password': 'password'
    }
    resp = test_client.post('/api/v1/auth/register', json=user_data)
    assert resp.status_code == 201
    data = json.loads(resp.data)
    user_id = data['id']
    activation_token = data['activation_token']
    resp = test_client.get(f'/api/v1/auth/activate?user_id={user_id}&activation_token={activation_token}')
    assert resp.status_code == 200
    resp = test_client.get(f'/api/v1/auth/activate?user_id={user_id}&activation_token={activation_token}')
    assert resp.status_code == 403
    
    
def test_activate_user_invalid_token(test_client):
    user_data = {
        'first_name': 'first_name_activate',
        'last_name': 'last_name_activate',
        'email_address': 'invalidtoken@gmail.com',
        'password': 'password'
    }
    resp = test_client.post('/api/v1/auth/register', json=user_data)
    assert resp.status_code == 201
    data = json.loads(resp.data)
    user_id = data['id']
    activation_token = 'invalid token'
    resp = test_client.get(f'/api/v1/auth/activate?user_id={user_id}&activation_token={activation_token}')
    assert resp.status_code == 403
    