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
    return {"Authorization": f"Token {token}"}

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


def login(username: str, password: str = None) -> Dict[str, Any]:
    """
    Login or auto-register with username.
    If password is not provided, username will be used as password.
    If user doesn't exist, it will be created automatically.
    """
    if password is None:
        password = username

    response = _make_request('POST', '/login', json={
        'username': username,
        'password': password
    })

    if 'token' in response:
        _save_token(response['token'], username)
        print(f"✅ {response.get('message', 'Authenticated')} '{username}'")

    return response


def submit_results(challenge_id: int, **results) -> Dict[str, Any]:
    """
    Submit only the results (lightweight, no code execution on server).
    """
    response = _make_request('POST', '/submit-results',
                            headers=_get_headers(),
                            json={'challenge_id': challenge_id, 'results': results})

    passed_emoji = "✅" if response.get('passed') else "❌"
    print(f"\n{passed_emoji} Score: {response.get('score', 0)}/{response.get('max_score', 100)}")
    print(f"Feedback: {response.get('feedback', 'No feedback')}\n")

    return response


# ==================== CHALLENGE 35 INDIVIDUAL TASK EVALUATION ====================

def evaluate_task1(alpha_vqe_result: float, beta_vqe_result: float) -> Dict[str, Any]:
    """
    Evaluate and submit Task 1 (VQE) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        alpha_vqe_result: Alpha molecule VQE ground state energy
        beta_vqe_result: Beta molecule VQE ground state energy

    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=351,  # Task 1
        alpha_vqe_result=alpha_vqe_result,
        beta_vqe_result=beta_vqe_result
    )


def evaluate_task2(alpha_gap_ev: float, beta_gap_ev: float,
                   alpha_homo_lumo: float, beta_homo_lumo: float) -> Dict[str, Any]:
    """
    Evaluate and submit Task 2 (HOMO-LUMO) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        alpha_gap_ev: Alpha HOMO-LUMO gap in eV
        beta_gap_ev: Beta HOMO-LUMO gap in eV
        alpha_homo_lumo: Alpha HOMO-LUMO gap in Hartree
        beta_homo_lumo: Beta HOMO-LUMO gap in Hartree

    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=352,  # Task 2
        alpha_gap_ev=alpha_gap_ev,
        beta_gap_ev=beta_gap_ev,
        alpha_homo_lumo=alpha_homo_lumo,
        beta_homo_lumo=beta_homo_lumo
    )


def evaluate_task3(alpha_index: int, beta_index: int, fidelity: float) -> Dict[str, Any]:
    """
    Evaluate and submit Task 3 (QSD) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        alpha_index: Index of best matching alpha state
        beta_index: Index of best matching beta state
        fidelity: Fidelity between the matched states

    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=353,  # Task 3
        alpha_index=alpha_index,
        beta_index=beta_index,
        fidelity=fidelity
    )


def evaluate_task4(final_energy_beta: float) -> Dict[str, Any]:
    """
    Evaluate and submit Task 4 (Final Energy Beta) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        final_energy_beta: Final energy for beta molecule

    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=354,  # Task 4
        final_energy_beta=final_energy_beta
    )


def evaluate_task5(final_energy_perturbed: float) -> Dict[str, Any]:
    """
    Evaluate and submit Task 5 (Final Energy Perturbed) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        final_energy_perturbed: Final energy for perturbed system

    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=355,
        final_energy_perturbed=final_energy_perturbed
    )
    
def evaluate_task6(task361_predictions, task361_y_test_hidden) -> Dict[str, Any]:
    """
    Evaluate and submit Task 5 (Final Energy Perturbed) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        final_energy_perturbed: Final energy for perturbed system

    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=361,
        task361_predictions=task361_predictions,
        task361_y_test_hidden=task361_y_test_hidden
    )

def evaluate_task7(task362_generated_images, task362_test_clean, task362_generated_shapes) -> Dict[str, Any]:
    """
    Evaluate and submit Task 5 (Final Energy Perturbed) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        final_energy_perturbed: Final energy for perturbed system
    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=362,
        task362_generated_images=task362_generated_images,
        task362_test_clean=task362_test_clean,
        task362_generated_shapes=task362_generated_shapes
    )
    
def evaluate_task8(task363_total_rewards) -> Dict[str, Any]:
    """
    Evaluate and submit Task 8 (Total Rewards) for Challenge 35.
    Returns ACCEPTED or REJECTED (binary).

    Args:
        task363_total_rewards: Total rewards for task 363

    Returns:
        Dictionary with evaluation results
    """
    return submit_results(
        challenge_id=363,
        task363_total_rewards=task363_total_rewards
    )
