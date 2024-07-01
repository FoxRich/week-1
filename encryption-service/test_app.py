import pytest
from app import app, db
from models import User
from data_loader import load_methods
import random
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            load_methods()  # Загружаем методы
            yield client

def test_add_user(client):
    random_login = generate_random_string(10)
    random_secret = generate_random_string(10)
    
    response = client.post('/users', json={
        'login': random_login,
        'secret': random_secret
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User added successfully'
    print(f"Test Add User: login={random_login}, secret={random_secret} - Passed")

def test_get_users(client):
    random_login = generate_random_string(10)
    random_secret = generate_random_string(10)
    
    client.post('/users', json={
        'login': random_login,
        'secret': random_secret
    })
    response = client.get('/users')
    assert response.status_code == 200
    assert any(user['login'] == random_login for user in response.json)
    print(f"Test Get Users: login={random_login}, secret={random_secret} - Passed")

def test_encrypt_vigenere(client):
    random_login = generate_random_string(10)
    random_secret = generate_random_string(10)
    
    user = User(login=random_login, secret=random_secret)
    db.session.add(user)
    db.session.commit()
    
    response = client.post('/encrypt', json={
        "user_id": user.id,
        "method_id": 1,
        "data_in": "Hello World",
        "json_params": {
            "key": generate_random_string(10)  # Длина ключа не должна превышать 10 символов
        }
    })
    
    assert response.status_code == 200
    assert 'encrypted_data' in response.json
    assert 'session_id' in response.json
    print(f"Test Encrypt Vigenere: login={random_login}, secret={random_secret} - Passed")

def test_encrypt_shift(client):
    random_login = generate_random_string(10)
    random_secret = generate_random_string(10)
    
    user = User(login=random_login, secret=random_secret)
    db.session.add(user)
    db.session.commit()
    
    response = client.post('/encrypt', json={
        "user_id": user.id,
        "method_id": 2,
        "data_in": "Hello World",
        "json_params": {
            "shift": 3
        }
    })
    
    assert response.status_code == 200
    assert 'encrypted_data' in response.json
    assert 'session_id' in response.json
    print(f"Test Encrypt Shift: login={random_login}, secret={random_secret} - Passed")

def test_decrypt_vigenere(client):
    random_login = generate_random_string(10)
    random_secret = generate_random_string(10)
    
    user = User(login=random_login, secret=random_secret)
    db.session.add(user)
    db.session.commit()
    
    key = generate_random_string(10)
    
    encrypt_response = client.post('/encrypt', json={
        "user_id": user.id,
        "method_id": 1,
        "data_in": "Hello World",
        "json_params": {
            "key": key
        }
    })
    
    encrypted_data = encrypt_response.json['encrypted_data']
    
    decrypt_response = client.post('/decrypt', json={
        "user_id": user.id,
        "method_id": 1,
        "data_in": encrypted_data,
        "json_params": {
            "key": key
        }
    })
    
    assert decrypt_response.status_code == 200
    assert decrypt_response.json['decrypted_data'].upper() == "HELLO WORLD"  # Приводим к верхнему регистру
    print(f"Test Decrypt Vigenere: login={random_login}, secret={random_secret} - Passed")

def test_decrypt_shift(client):
    random_login = generate_random_string(10)
    random_secret = generate_random_string(10)
    
    user = User(login=random_login, secret=random_secret)
    db.session.add(user)
    db.session.commit()
    
    encrypt_response = client.post('/encrypt', json={
        "user_id": user.id,
        "method_id": 2,
        "data_in": "Hello World",
        "json_params": {
            "shift": 3
        }
    })
    
    encrypted_data = encrypt_response.json['encrypted_data']
    
    decrypt_response = client.post('/decrypt', json={
        "user_id": user.id,
        "method_id": 2,
        "data_in": encrypted_data,
        "json_params": {
            "shift": 3
        }
    })
    
    assert decrypt_response.status_code == 200
    assert decrypt_response.json['decrypted_data'].upper() == "HELLO WORLD"  # Приводим к верхнему регистру
    print(f"Test Decrypt Shift: login={random_login}, secret={random_secret} - Passed")

def test_brute_force_shift(client):
    random_login = generate_random_string(10)
    random_secret = generate_random_string(10)
    
    user = User(login=random_login, secret=random_secret)
    db.session.add(user)
    db.session.commit()
    
    encrypt_response = client.post('/encrypt', json={
        "user_id": user.id,
        "method_id": 2,
        "data_in": "Hello World",
        "json_params": {
            "shift": 3
        }
    })
    
    assert encrypt_response.status_code == 200
    encrypted_data = encrypt_response.json['encrypted_data']
    
    brute_force_response = client.post('/bruteforce/shift', json={
        "data_in": encrypted_data
    })
    
    assert brute_force_response.status_code == 200
    possible_decryptions = brute_force_response.json['possible_decryptions']
    assert "HELLO WORLD" in [text.upper() for text in possible_decryptions]  # Приводим к верхнему регистру
    print(f"Test Brute Force Shift: login={random_login}, secret={random_secret} - Passed")
