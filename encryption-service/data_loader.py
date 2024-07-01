from models import Method, db

def load_methods():
    methods = [
        {"id": 1, "caption": "Vigenere Cipher", "json_params": {}, "description": "Encrypts using Vigenere Cipher."},
        {"id": 2, "caption": "Shift Cipher", "json_params": {"shift": 3}, "description": "Encrypts using Shift Cipher with shift of 3."}
    ]

    for method in methods:
        existing_method = db.session.get(Method, method["id"])
        if not existing_method:
            new_method = Method(**method)
            db.session.add(new_method)

    db.session.commit()
