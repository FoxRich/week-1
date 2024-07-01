from flask import request, jsonify
from models import User, Method, Session, db
from utils import vigenere_cipher, vigenere_decipher, shift_cipher, shift_decipher, vigenere_brute_force, shift_brute_force
import time
import datetime

def configure_routes(app):

    @app.route('/users', methods=['POST'])
    def add_user():
        data = request.json
        if not data or 'login' not in data or 'secret' not in data:
            return jsonify({'message': 'Invalid input'}), 400
        if len(data['login']) < 3 or len(data['login']) > 10 or len(data['secret']) < 3 or len(data['secret']) > 10:
            return jsonify({'message': 'Invalid length for login or secret'}), 400
        user = User.query.filter_by(login=data['login']).first()
        if user:
            return jsonify({'message': 'User already exists'}), 400
        user = User(login=data['login'], secret=data['secret'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([{'user_id': user.id, 'login': user.login} for user in users]), 200

    @app.route('/methods', methods=['GET'])
    def get_methods():
        return jsonify([{'id': method.id, 'caption': method.caption, 'json_params': method.json_params, 'description': method.description} for method in Method.query.all()]), 200

    @app.route('/encrypt', methods=['POST'])
    def encrypt():
        try:
            data = request.json
            if not data or 'user_id' not in data or 'method_id' not in data or 'data_in' not in data:
                return jsonify({'message': 'Invalid input'}), 400

            user_id = data['user_id']
            method_id = data['method_id']
            data_in = data['data_in']

            user = db.session.get(User, user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            method = db.session.get(Method, method_id)
            if not method:
                return jsonify({'message': 'Method not found'}), 404

            if len(data_in) > 10000:
                return jsonify({'message': 'Input data too long'}), 400

            if method.caption == 'Vigenere Cipher':
                if 'key' not in data['json_params']:
                    return jsonify({'message': 'Missing key for Vigenere Cipher'}), 400
                encrypted_data = vigenere_cipher(data_in, data['json_params']['key'])
            elif method.caption == 'Shift Cipher':
                encrypted_data = shift_cipher(data_in, method.json_params['shift'])
            else:
                return jsonify({'message': 'Unsupported method'}), 400

            session = Session(
                user_id=user_id,
                method_id=method_id,
                data_in=data_in,
                data_out=encrypted_data,
                action_type='encryption',
                status='completed',
                created_at=datetime.datetime.now(datetime.UTC),  # Установите текущую дату и время
                time_op=0  # Simplified for example purposes
            )
            db.session.add(session)
            db.session.commit()

            return jsonify({'session_id': session.id, 'encrypted_data': encrypted_data}), 200

        except Exception as e:
            return jsonify({'message': 'An error occurred during encryption', 'error': str(e)}), 500

    @app.route('/decrypt', methods=['POST'])
    def decrypt():
        try:
            data = request.json
            if not data or 'user_id' not in data or 'method_id' not in data or 'data_in' not in data:
                return jsonify({'message': 'Invalid input'}), 400

            user_id = data['user_id']
            method_id = data['method_id']
            data_in = data['data_in']

            user = db.session.get(User, user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            method = db.session.get(Method, method_id)
            if not method:
                return jsonify({'message': 'Method not found'}), 404

            if len(data_in) > 10000:
                return jsonify({'message': 'Input data too long'}), 400

            if method.caption == 'Vigenere Cipher':
                if 'key' not in data['json_params']:
                    return jsonify({'message': 'Missing key for Vigenere Cipher'}), 400
                decrypted_data = vigenere_decipher(data_in, data['json_params']['key'])
            elif method.caption == 'Shift Cipher':
                decrypted_data = shift_decipher(data_in, method.json_params['shift'])
            else:
                return jsonify({'message': 'Unsupported method'}), 400

            session = Session(
                user_id=user_id,
                method_id=method_id,
                data_in=data_in,
                data_out=decrypted_data,
                action_type='decryption',
                status='completed',
                created_at=datetime.datetime.now(datetime.UTC),  # Установите текущую дату и время
                time_op=0  # Simplified for example purposes
            )
            db.session.add(session)
            db.session.commit()

            return jsonify({'session_id': session.id, 'decrypted_data': decrypted_data}), 200

        except Exception as e:
            return jsonify({'message': 'An error occurred during decryption', 'error': str(e)}), 500

    @app.route('/sessions/<int:session_id>', methods=['GET'])
    def get_session(session_id):
        session = db.session.get(Session, session_id)
        if not session:
            return jsonify({'message': 'Session not found'}), 404
        return jsonify({
            'id': session.id,
            'user_id': session.user_id,
            'method_id': session.method_id,
            'data_in': session.data_in,
            'data_out': session.data_out,
            'action_type': session.action_type,
            'status': session.status,
            'created_at': session.created_at,
            'time_op': session.time_op
        }), 200

    @app.route('/sessions/<int:session_id>', methods=['DELETE'])
    def delete_session(session_id):
        try:
            data = request.json
            if not data or 'secret' not in data:
                return jsonify({'message': 'Invalid input'}), 400

            session = db.session.get(Session, session_id)
            if not session:
                return jsonify({'message': 'Session not found'}), 404

            user = db.session.get(User, session.user_id)
            if not user or user.secret != data['secret']:
                return jsonify({'message': 'Unauthorized'}), 403

            db.session.delete(session)
            db.session.commit()
            return jsonify({'message': 'Session deleted successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'An error occurred while deleting session', 'error': str(e)}), 500

    @app.route('/bruteforce/vigenere', methods=['POST'])
    def brute_force_vigenere():
        try:
            data = request.json
            if not data or 'data_in' not in data:
                return jsonify({'message': 'Invalid input'}), 400

            data_in = data['data_in']
            possible_decryptions = vigenere_brute_force(data_in)

            return jsonify({'possible_decryptions': possible_decryptions}), 200

        except Exception as e:
            return jsonify({'message': 'An error occurred during brute force', 'error': str(e)}), 500

    @app.route('/bruteforce/shift', methods=['POST'])
    def brute_force_shift():
        try:
            data = request.json
            if not data or 'data_in' not in data:
                return jsonify({'message': 'Invalid input'}), 400

            data_in = data['data_in']
            possible_decryptions = shift_brute_force(data_in)

            return jsonify({'possible_decryptions': possible_decryptions}), 200

        except Exception as e:
            return jsonify({'message': 'An error occurred during brute force', 'error': str(e)}), 500
