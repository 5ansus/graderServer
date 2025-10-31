"""
PLEASE DO NOT CHANGE ANYTHING ON THIS FILE 

This file is the client of an API that will register all your progress. 

If you have any issues (and you didn't change anyting in this file) please contact the 
co-organizers of MadQFF'25 (purple or red username on discord)

As well, if you are an external, you will not have any access as the API will be 
close to you.
"""


import requests
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

BASE_URL = "https://UAMCPrA.pythonanywhere.com/api"
TOKEN_FILE = Path.home() / ".qiskit_grader_token"

class GraderError(Exception):
    """Excepción personalizada para errores del grader"""
    pass


def _get_token() -> Optional[str]:
    if TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE, 'r') as f:
                data = json.load(f)
                return data.get('token')
        except:
            return None
    return None


def _save_token(token: str, username: str):
    with open(TOKEN_FILE, 'w') as f:
        json.dump({'token': token, 'username': username}, f)
    os.chmod(TOKEN_FILE, 0o600)  # Permisos solo para el usuario


def _get_headers() -> Dict[str, str]:
    token = _get_token()
    if not token:
        raise GraderError(
            "Whoah, u are not authentificated. Use login('username', 'password') first :)"
        )
    return {"Authorization": f"Bearer {token}"}

def _make_request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    
    try:
        response = requests.request(method, url, **kwargs)
        
        if response.status_code == 401:
            raise GraderError(
                "Token token. Please redoo login()"
            )
        
        if response.status_code >= 400:
            error_msg = response.json().get('error', 'Error desconocido')
            raise GraderError(f"Error {response.status_code}: {error_msg}")
        
        return response.json()
    
    except requests.exceptions.ConnectionError:
        raise GraderError(
            f"Cannot connect to : {BASE_URL}\n"
            "Please contact with the co-organizers"
        )
    except requests.exceptions.Timeout:
        raise GraderError("Timeout")
    except json.JSONDecodeError:
        raise GraderError("Invalid response")


# ==================== AUTENTICACIÓN ====================

def register(username: str, email: str, password: str) -> Dict[str, Any]:
    response = _make_request('POST', '/register', json={
        'username': username,
        'email': email,
        'password': password
    })
    
    if 'token' in response:
        _save_token(response['token'], username)
        print(f"✅ Registered as '{username}' :) ")
    
    return response


def login(username: str, password: str) -> Dict[str, Any]:
    response = _make_request('POST', '/login', json={
        'username': username,
        'password': password
    })
    
    if 'token' in response:
        _save_token(response['token'], username)
        print(f"✅ Authentificaed as '{username}'")
    
    return response


def logout():
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        print("✅ Sesión closed")
    else:
        print("⚠️ No active account")


def whoami() -> Dict[str, Any]:
    return _make_request('GET', '/profile', headers=_get_headers())


# ==================== CHALLENGES ====================

def get_challenges() -> Dict[str, Any]:
    return _make_request('GET', '/challenges', headers=_get_headers())


def get_challenge(challenge_id: int) -> Dict[str, Any]:
    return _make_request('GET', f'/challenges/{challenge_id}', headers=_get_headers())


# ==================== SUBMISSIONS ====================

def submit(challenge_id: int, code: str) -> Dict[str, Any]:
    response = _make_request('POST', '/submit', 
                            headers=_get_headers(),
                            json={'challenge_id': challenge_id, 'code': code})
    
    passed_emoji = "✅" if response.get('passed') else "❌"
    print(f"\n{passed_emoji} Score: {response.get('score', 0)}/{response.get('max_score', 100)}")
    print(f"Feedback: {response.get('feedback', 'Sin feedback')}\n")
    
    return response


def submit_function(challenge_id: int, func):
    import inspect
    code = inspect.getsource(func)
    return submit(challenge_id, code)


def get_submissions(challenge_id: Optional[int] = None) -> Dict[str, Any]:
    params = {'challenge_id': challenge_id} if challenge_id else {}
    return _make_request('GET', '/submissions', 
                        headers=_get_headers(),
                        params=params)


def get_submission(submission_id: int) -> Dict[str, Any]:
    return _make_request('GET', f'/submissions/{submission_id}', 
                        headers=_get_headers())


# ==================== LEADERBOARD Y PROGRESO ====================

def get_leaderboard(limit: int = 50) -> Dict[str, Any]:
    return _make_request('GET', '/leaderboard', 
                        headers=_get_headers(),
                        params={'limit': limit})


def get_progress() -> Dict[str, Any]:
    return _make_request('GET', '/progress', headers=_get_headers())


def get_stats() -> Dict[str, Any]:
    return _make_request('GET', '/stats', headers=_get_headers())


# ==================== FUNCIONES HELPER ESPECÍFICAS ====================

def graderAHC1(code: str) -> Tuple[int, bool, str]:
    result = submit(1, code)
    return result['score'], result['passed'], result['feedback']


def graderAHC2(code: str) -> Tuple[int, bool, str]:
    result = submit(2, code)
    return result['score'], result['passed'], result['feedback']


def graderAHC3(code: str) -> Tuple[int, bool, str]:
    result = submit(3, code)
    return result['score'], result['passed'], result['feedback']


def graderAHC4(code: str) -> Tuple[int, bool, str]:
    result = submit(4, code)
    return result['score'], result['passed'], result['feedback']


def graderAHC5(code: str) -> Tuple[int, bool, str]:
    result = submit(5, code)
    return result['score'], result['passed'], result['feedback']


# ==================== UTILIDADES ====================

def configure(server_url: str = "https://UAMCPrA.pythonanywhere.com"):
    global BASE_URL
    BASE_URL = f"{server_url.rstrip('/')}/api"
    print(f"THIS IS NOT A METHOD U SHOULD BE USING AS A CLIENT")

def show_challenges():
    challenges = get_challenges()
    
    print("\n" + "="*70)
    print("============= CHALLENGES =================")
    print("="*70 + "\n")
    
    for ch in challenges['challenges']:
        status = "✅" if ch['completed'] else "⏳"
        score_str = f"{ch['best_score']}/{ch['max_score']}" if ch['best_score'] > 0 else "No intentado"
        
        print(f"{status} Challenge {ch['id']}: {ch['name']}")
        print(f"   Score: {score_str}")
        print()


def show_leaderboard(top: int = 10):
    leaderboard = get_leaderboard(limit=top)
    
    print("\n" + "="*70)
    print(" ============= LEADERBOARD ==========")
    print("="*70 + "\n")
    
    print(f"You are at: #{leaderboard['user_position']}\n")
    
    for i, user in enumerate(leaderboard['leaderboard'][:top], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"{medal} {i:2d}. {user['username']:20s} | {user['total_score']:4d} pts | {user['challenges_completed']} challenges")


def show_progress():
    progress = get_progress()
    profile = whoami()
    
    print("\n" + "="*70)
    print("📊 YOUR PROGRESS")
    print("="*70 + "\n")
    
    print(f"User: {profile['user']['username']}")
    print(f"Total Score: {progress['total_score']} puntos")
    print(f"Challenges completed: {progress['challenges_completed']}/{progress['total_challenges']}")
    print(f"Total submissions: {progress['total_submissions']}")
    
    if progress['total_challenges'] > 0:
        percentage = (progress['challenges_completed'] / progress['total_challenges']) * 100
        print(f"Progress: {percentage:.1f}%")
        
        # Barra de progreso
        bar_length = 50
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"[{bar}]")


# ==================== TESTING ====================

def test_connection() -> bool:
    try:
        response = requests.get(f"{BASE_URL.rsplit('/api', 1)[0]}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Conexión exitosa con {BASE_URL}")
            return True
        else:
            print(f"⚠️ Servidor respondió con código {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Conection error: {e}")
        print(f"URL tryout but not connected to (contact the co-organizers): {BASE_URL}")
        return False


