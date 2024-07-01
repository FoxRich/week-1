# Encryption Service API

## Setup

1. Clone the repository.
2. Navigate to the project directory.
3. Install the required packages:
   ```bash
   pip install flask
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Endpoints

### Add User

- `POST /users`
- Request body:
  ```json
  {
    "login": "username",
    "secret": "123"
  }
  ```
- Response:
  ```json
  {
    "message": "User added successfully"
  }
  ```

### Get Users

- `GET /users`
- Response:
  ```json
  [
    {
      "user_id": 1,
      "login": "username"
    }
  ]
  ```

### Get Methods

- `GET /methods`
- Response:
  ```json
  [
    {
      "id": 1,
      "caption": "Vigenere Cipher",
      "json_params": {},
      "description": "Encrypts using Vigenere Cipher."
    },
    {
      "id": 2,
      "caption": "Shift Cipher",
      "json_params": { "shift": 3 },
      "description": "Encrypts using Shift Cipher with shift of 3."
    }
  ]
  ```

### Encrypt Data

- `POST /encrypt`
- Request body:
  ```json
  {
    "user_id": 1,
    "method_id": 1,
    "data_in": "HELLO",
    "json_params": {
      "key": "KEY"
    }
  }
  ```
- Response:
  ```json
  {
    "session_id": 1,
    "encrypted_data": "RIJVS"
  }
  ```

### Get Session

- `GET /sessions/{session_id}`
- Response:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "method_id": 1,
    "data_in": "HELLO",
    "data_out": "RIJVS",
    "status": "completed",
    "created_at": 1623860460.123456,
    "time_op": 0
  }
  ```

### Delete Session

- `DELETE /sessions/{session_id}`
- Request body:
  ```json
  {
    "user_id": 1,
    "secret": "123"
  }
  ```
- Response:
  ```json
  {
    "message": "Session deleted successfully"
  }
  ```

## Insomnia Collection

U can find Insomnia Collection at root project folder
