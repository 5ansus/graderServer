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
    def evaluate_challenge_35(code: str) -> tuple[int, bool, str, float]:
        """
        Evalúa el Challenge 35: A Halloween Carol - Quantum Chemistry Mystery

        Returns:
            tuple: (score, passed, feedback, execution_time)
        """
        start_time = time.time()

        try:
            # Crear un namespace para ejecutar el código
            local_scope = {}

            # Ejecutar el código del usuario
            exec(code, {}, local_scope)

            # Verificar que existan las funciones/variables requeridas
            required_items = [
                'alpha_vqe_result',
                'beta_vqe_result',
                'alpha_gap_ev',
                'beta_gap_ev',
                'alpha_homo_lumo',
                'beta_homo_lumo'
            ]

            missing = [item for item in required_items if item not in local_scope]

            if missing:
                feedback = f"❌ Faltan variables/resultados: {', '.join(missing)}\n"
                feedback += "Asegúrate de ejecutar todo el notebook y tener todos los resultados."
                return 0, False, feedback, time.time() - start_time

            # Extraer resultados
            alpha_vqe = local_scope.get('alpha_vqe_result')
            beta_vqe = local_scope.get('beta_vqe_result')
            alpha_gap = local_scope.get('alpha_gap_ev')
            beta_gap = local_scope.get('beta_gap_ev')
            alpha_homo_lumo = local_scope.get('alpha_homo_lumo')
            beta_homo_lumo = local_scope.get('beta_homo_lumo')

            # Sistema de puntuación
            score = 0
            feedback_parts = []

            # Task 1: VQE Analysis (30 puntos)
            if alpha_vqe is not None and beta_vqe is not None:
                # Verificar que los resultados sean razonables
                try:
                    alpha_energy = float(alpha_vqe.eigenvalue) if hasattr(alpha_vqe, 'eigenvalue') else float(alpha_vqe)
                    beta_energy = float(beta_vqe.eigenvalue) if hasattr(beta_vqe, 'eigenvalue') else float(beta_vqe)

                    # Los valores deben estar en un rango razonable para química cuántica
                    if -10 < alpha_energy < 0 and -10 < beta_energy < 0:
                        score += 30
                        feedback_parts.append("✅ Task 1 (VQE): Excelente! Energías calculadas correctamente.")
                    else:
                        score += 15
                        feedback_parts.append("⚠️ Task 1 (VQE): Energías calculadas pero parecen fuera de rango.")
                except:
                    score += 10
                    feedback_parts.append("⚠️ Task 1 (VQE): Resultados parciales.")
            else:
                feedback_parts.append("❌ Task 1 (VQE): No se encontraron resultados VQE.")

            # Task 2: HOMO-LUMO Gap (30 puntos)
            if alpha_gap is not None and beta_gap is not None:
                try:
                    alpha_gap_val = float(alpha_gap)
                    beta_gap_val = float(beta_gap)

                    # Los gaps deben ser positivos y razonables (0-10 eV típicamente)
                    if 0 < alpha_gap_val < 15 and 0 < beta_gap_val < 15:
                        score += 30
                        feedback_parts.append(f"✅ Task 2 (HOMO-LUMO): Perfecto! Alpha gap: {alpha_gap_val:.2f} eV, Beta gap: {beta_gap_val:.2f} eV")

                        # Bonus por interpretación correcta
                        if beta_gap_val < alpha_gap_val:
                            feedback_parts.append("   💡 Beta es más reactivo que Alpha (gap menor)")
                    else:
                        score += 15
                        feedback_parts.append("⚠️ Task 2 (HOMO-LUMO): Gaps calculados pero valores inusuales.")
                except:
                    score += 10
                    feedback_parts.append("⚠️ Task 2 (HOMO-LUMO): Error al procesar los gaps.")
            else:
                feedback_parts.append("❌ Task 2 (HOMO-LUMO): No se encontraron cálculos de gap.")

            # Task 3: QSD Analysis (40 puntos)
            # Este es el más complejo, verificamos que al menos se haya intentado
            qsd_indicators = ['V_alpha', 'V_beta', 'evals_alpha', 'evals_beta', 'fidelity_matrix']
            qsd_present = sum(1 for item in qsd_indicators if item in local_scope)

            if qsd_present >= 3:
                score += 40
                feedback_parts.append("✅ Task 3 (QSD): Excelente! Análisis de subespacio cuántico completado.")
            elif qsd_present >= 2:
                score += 25
                feedback_parts.append("⚠️ Task 3 (QSD): Análisis parcial de QSD.")
            elif qsd_present >= 1:
                score += 15
                feedback_parts.append("⚠️ Task 3 (QSD): Inicio de análisis QSD detectado.")
            else:
                feedback_parts.append("❌ Task 3 (QSD): No se encontró análisis QSD.")

            # Determinar si pasó
            passed = score >= 70

            # Construir feedback final
            feedback = "\n".join(feedback_parts)
            feedback += f"\n\n📊 Puntuación final: {score}/100"

            if passed:
                feedback += "\n🎃 ¡Felicidades! Has completado el Halloween Challenge."
            else:
                feedback += "\n💀 Sigue intentando. Revisa las tareas que faltan."

            execution_time = time.time() - start_time
            return score, passed, feedback, execution_time

        except SyntaxError as e:
            execution_time = time.time() - start_time
            return 0, False, f"❌ Error de sintaxis: {str(e)}", execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"❌ Error al evaluar: {str(e)}\n{traceback.format_exc()}"
            return 0, False, error_msg, execution_time

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
            35: CodeEvaluator.evaluate_challenge_35,
        }

        evaluator = evaluators.get(challenge_id)

        if not evaluator:
            return 0, False, f"❌ No hay evaluador para challenge {challenge_id}. Solo el Challenge 35 está disponible.", 0.0

        try:
            return evaluator(code)
        except Exception as e:
            return 0, False, f"❌ Error crítico en evaluación: {str(e)}", 0.0
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
