"""
API Server for Qiskit Grader - Halloween Challenge
Compatible with grader_qiskit_client.py
"""

from flask import Flask, request, jsonify
from functools import wraps
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Simulación de base de datos (en producción usa una DB real)
users_db = {}
challenges_db = {
    1: {"id": 1, "name": "Challenge 1", "description": "First challenge", "max_score": 100},
    2: {"id": 2, "name": "Challenge 2", "description": "Second challenge", "max_score": 100},
    3: {"id": 3, "name": "Challenge 3", "description": "Third challenge", "max_score": 100},
    4: {"id": 4, "name": "Challenge 4", "description": "Fourth challenge", "max_score": 100},
    5: {"id": 5, "name": "Challenge 5", "description": "Fifth challenge", "max_score": 100},
}
submissions_db = []


# ==================== DECORADORES ====================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_db.get(data['username'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# ==================== RUTAS DE AUTENTICACIÓN ====================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 400

    users_db[username] = {
        'username': username,
        'email': email,
        'password': generate_password_hash(password),
        'created_at': datetime.datetime.utcnow().isoformat(),
        'total_score': 0,
        'challenges_completed': []
    }

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'message': 'Registration successful',
        'token': token,
        'username': username
    }), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = users_db.get(username)

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'username': username
    }), 200


@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'user': {
            'username': current_user['username'],
            'email': current_user['email'],
            'total_score': current_user['total_score'],
            'challenges_completed': len(current_user['challenges_completed'])
        }
    }), 200


# ==================== RUTAS DE CHALLENGES ====================

@app.route('/api/challenges', methods=['GET'])
@token_required
def get_challenges(current_user):
    challenges_list = []

    for ch_id, ch_data in challenges_db.items():
        # Buscar mejor score del usuario para este challenge
        user_submissions = [s for s in submissions_db
                           if s['username'] == current_user['username']
                           and s['challenge_id'] == ch_id]

        best_score = max([s['score'] for s in user_submissions], default=0)
        completed = ch_id in current_user['challenges_completed']

        challenges_list.append({
            'id': ch_id,
            'name': ch_data['name'],
            'description': ch_data['description'],
            'max_score': ch_data['max_score'],
            'best_score': best_score,
            'completed': completed
        })

    return jsonify({'challenges': challenges_list}), 200


@app.route('/api/challenges/<int:challenge_id>', methods=['GET'])
@token_required
def get_challenge(current_user, challenge_id):
    challenge = challenges_db.get(challenge_id)

    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404

    return jsonify({'challenge': challenge}), 200


# ==================== RUTAS DE SUBMISSIONS ====================

@app.route('/api/submit', methods=['POST'])
@token_required
def submit_solution(current_user):
    data = request.get_json()

    challenge_id = data.get('challenge_id')
    code = data.get('code')

    if not challenge_id or not code:
        return jsonify({'error': 'Missing challenge_id or code'}), 400

    if challenge_id not in challenges_db:
        return jsonify({'error': 'Invalid challenge_id'}), 404

    # Aquí iría la lógica de evaluación del código
    # Por ahora, simulamos una evaluación
    score, passed, feedback = evaluate_code(challenge_id, code)

    submission = {
        'id': len(submissions_db) + 1,
        'username': current_user['username'],
        'challenge_id': challenge_id,
        'code': code,
        'score': score,
        'passed': passed,
        'feedback': feedback,
        'submitted_at': datetime.datetime.utcnow().isoformat()
    }

    submissions_db.append(submission)

    # Actualizar score del usuario
    user_submissions = [s for s in submissions_db
                       if s['username'] == current_user['username']
                       and s['challenge_id'] == challenge_id]
    best_score = max([s['score'] for s in user_submissions])

    if passed and challenge_id not in current_user['challenges_completed']:
        current_user['challenges_completed'].append(challenge_id)

    # Recalcular total score
    total_score = 0
    for ch_id in challenges_db.keys():
        ch_submissions = [s for s in submissions_db
                         if s['username'] == current_user['username']
                         and s['challenge_id'] == ch_id]
        if ch_submissions:
            total_score += max([s['score'] for s in ch_submissions])

    current_user['total_score'] = total_score

    return jsonify({
        'submission_id': submission['id'],
        'score': score,
        'max_score': challenges_db[challenge_id]['max_score'],
        'passed': passed,
        'feedback': feedback
    }), 200


@app.route('/api/submissions', methods=['GET'])
@token_required
def get_submissions(current_user):
    challenge_id = request.args.get('challenge_id', type=int)

    user_submissions = [s for s in submissions_db
                       if s['username'] == current_user['username']]

    if challenge_id:
        user_submissions = [s for s in user_submissions
                          if s['challenge_id'] == challenge_id]

    return jsonify({'submissions': user_submissions}), 200


@app.route('/api/submissions/<int:submission_id>', methods=['GET'])
@token_required
def get_submission(current_user, submission_id):
    submission = next((s for s in submissions_db if s['id'] == submission_id), None)

    if not submission:
        return jsonify({'error': 'Submission not found'}), 404

    if submission['username'] != current_user['username']:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'submission': submission}), 200


# ==================== RUTAS DE LEADERBOARD ====================

@app.route('/api/leaderboard', methods=['GET'])
@token_required
def get_leaderboard(current_user):
    limit = request.args.get('limit', default=50, type=int)

    # Ordenar usuarios por score
    sorted_users = sorted(
        [{'username': u['username'],
          'total_score': u['total_score'],
          'challenges_completed': len(u['challenges_completed'])}
         for u in users_db.values()],
        key=lambda x: (-x['total_score'], -x['challenges_completed'])
    )

    # Encontrar posición del usuario actual
    user_position = next(
        (i + 1 for i, u in enumerate(sorted_users)
         if u['username'] == current_user['username']),
        None
    )

    return jsonify({
        'leaderboard': sorted_users[:limit],
        'user_position': user_position
    }), 200


@app.route('/api/progress', methods=['GET'])
@token_required
def get_progress(current_user):
    user_submissions = [s for s in submissions_db
                       if s['username'] == current_user['username']]

    return jsonify({
        'total_score': current_user['total_score'],
        'challenges_completed': len(current_user['challenges_completed']),
        'total_challenges': len(challenges_db),
        'total_submissions': len(user_submissions)
    }), 200


@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    return jsonify({
        'total_users': len(users_db),
        'total_challenges': len(challenges_db),
        'total_submissions': len(submissions_db)
    }), 200


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'API is running'
    }), 200


# ==================== FUNCIONES AUXILIARES ====================

def evaluate_code(challenge_id, code):
    """
    Evalúa el código enviado.
    Aquí debes implementar tu lógica de evaluación específica.
    """
    # Ejemplo básico de evaluación
    try:
        # Aquí iría tu lógica de evaluación real
        # Por ahora retornamos valores de ejemplo

        if len(code) < 10:
            return 0, False, "Code too short"

        # Simulación: asignamos un score aleatorio
        score = min(100, len(code) % 101)
        passed = score >= 70
        feedback = "Good job!" if passed else "Keep trying!"

        return score, passed, feedback

    except Exception as e:
        return 0, False, f"Error evaluating code: {str(e)}"


# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(debug=True)
