"""
Sistema de evaluación de código para cada challenge.
Añade aquí la lógica específica para evaluar cada ejercicio.
"""

import time
import sys
from io import StringIO
import traceback


class CodeEvaluator:
    """
    Clase base para evaluar código de submissions.
    """

    @staticmethod
    def evaluate_challenge_1(code: str) -> tuple[int, bool, str, float]:
        """
        Evalúa el Challenge 1.

        Returns:
            tuple: (score, passed, feedback, execution_time)
        """
        start_time = time.time()

        try:
            # Aquí va tu lógica específica para el Challenge 1
            # Ejemplo básico:

            local_scope = {}
            exec(code, {}, local_scope)

            # Verifica que exista una función específica
            if 'solution' not in local_scope:
                return 0, False, "No se encontró la función 'solution'", time.time() - start_time

            solution_func = local_scope['solution']

            # Test cases
            test_cases = [
                (1, 2),
                (5, 10),
                (0, 0),
            ]

            passed_tests = 0
            for test_input, expected in test_cases:
                result = solution_func(test_input)
                if result == expected:
                    passed_tests += 1

            score = int((passed_tests / len(test_cases)) * 100)
            passed = score >= 70
            feedback = f"Pasaste {passed_tests}/{len(test_cases)} tests. "

            if passed:
                feedback += "¡Excelente trabajo!"
            else:
                feedback += "Sigue intentando."

            execution_time = time.time() - start_time
            return score, passed, feedback, execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Error al evaluar: {str(e)}\n{traceback.format_exc()}"
            return 0, False, error_msg, execution_time

    @staticmethod
    def evaluate_challenge_2(code: str) -> tuple[int, bool, str, float]:
        """
        Evalúa el Challenge 2.
        """
        start_time = time.time()

        try:
            # Implementa aquí la lógica para Challenge 2
            # Este es un ejemplo genérico

            local_scope = {}
            exec(code, {}, local_scope)

            # Tu lógica de evaluación específica
            score = 80  # Ejemplo
            passed = True
            feedback = "Challenge 2 completado"

            execution_time = time.time() - start_time
            return score, passed, feedback, execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Error: {str(e)}"
            return 0, False, error_msg, execution_time

    @staticmethod
    def evaluate_challenge_3(code: str) -> tuple[int, bool, str, float]:
        """
        Evalúa el Challenge 3.
        """
        start_time = time.time()

        try:
            # Implementa aquí la lógica para Challenge 3
            local_scope = {}
            exec(code, {}, local_scope)

            score = 75
            passed = True
            feedback = "Challenge 3 completado"

            execution_time = time.time() - start_time
            return score, passed, feedback, execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            return 0, False, f"Error: {str(e)}", execution_time

    @staticmethod
    def evaluate_challenge_4(code: str) -> tuple[int, bool, str, float]:
        """
        Evalúa el Challenge 4.
        """
        start_time = time.time()

        try:
            local_scope = {}
            exec(code, {}, local_scope)

            score = 85
            passed = True
            feedback = "Challenge 4 completado"

            execution_time = time.time() - start_time
            return score, passed, feedback, execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            return 0, False, f"Error: {str(e)}", execution_time

    @staticmethod
    def evaluate_challenge_5(code: str) -> tuple[int, bool, str, float]:
        """
        Evalúa el Challenge 5.
        """
        start_time = time.time()

        try:
            local_scope = {}
            exec(code, {}, local_scope)

            score = 90
            passed = True
            feedback = "Challenge 5 completado"

            execution_time = time.time() - start_time
            return score, passed, feedback, execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            return 0, False, f"Error: {str(e)}", execution_time

    @staticmethod
    def evaluate(challenge_id: int, code: str) -> tuple[int, bool, str, float]:
        """
        Método principal para evaluar código según el challenge.

        Args:
            challenge_id: ID del challenge
            code: Código a evaluar

        Returns:
            tuple: (score, passed, feedback, execution_time)
        """
        evaluators = {
            1: CodeEvaluator.evaluate_challenge_1,
            2: CodeEvaluator.evaluate_challenge_2,
            3: CodeEvaluator.evaluate_challenge_3,
            4: CodeEvaluator.evaluate_challenge_4,
            5: CodeEvaluator.evaluate_challenge_5,
        }

        evaluator = evaluators.get(challenge_id)

        if not evaluator:
            return 0, False, f"No hay evaluador para challenge {challenge_id}", 0.0

        try:
            return evaluator(code)
        except Exception as e:
            return 0, False, f"Error crítico en evaluación: {str(e)}", 0.0


# Función helper para capturar stdout durante la ejecución
def capture_stdout(func, *args, **kwargs):
    """Captura el stdout durante la ejecución de una función"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        result = func(*args, **kwargs)
        output = sys.stdout.getvalue()
        return result, output
    finally:
        sys.stdout = old_stdout
