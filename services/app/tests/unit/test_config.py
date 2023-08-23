def test_config(test_app):
    assert test_app.config['TESTING'] is True
    assert test_app.config['SECRET_KEY'] == 'secret-key'