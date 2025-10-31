"""
Code evaluation system for each challenge.
Add specific logic here to evaluate each exercise.
"""

import time
import sys
from io import StringIO
import traceback


class CodeEvaluator:
    """
    Base class for evaluating submissions.
    """

    @staticmethod
    def evaluate_challenge_35_results(results: dict) -> tuple[int, bool, str, float]:
        """
        Evaluates Challenge 35 using ONLY results (no code execution).

        Args:
            results: Dictionary with required variables

        Returns:
            tuple: (score, passed, feedback, execution_time)
        """
        start_time = time.time()

        try:
            # Check that required variables exist
            required_items = [
                'alpha_vqe_result',
                'beta_vqe_result',
                'alpha_gap_ev',
                'beta_gap_ev',
                'alpha_homo_lumo',
                'beta_homo_lumo'
            ]

            missing = [item for item in required_items if item not in results]

            if missing:
                feedback = f"❌ Missing results: {', '.join(missing)}\n"
                feedback += "You must send all required variables."
                return 0, False, feedback, time.time() - start_time            # Extraer resultados
            alpha_vqe = results.get('alpha_vqe_result')
            beta_vqe = results.get('beta_vqe_result')
            alpha_gap = results.get('alpha_gap_ev')
            beta_gap = results.get('beta_gap_ev')
            alpha_homo_lumo = results.get('alpha_homo_lumo')
            beta_homo_lumo = results.get('beta_homo_lumo')

            # Scoring system
            score = 0
            feedback_parts = []

            # Reference values (approximate)
            ALPHA_VQE_REF = -2.1847  # Approximate ground state energy
            BETA_VQE_REF = 0.9375

            # Task 1: VQE Analysis (30 points)
            if alpha_vqe is not None and beta_vqe is not None:
                try:
                    alpha_energy = float(alpha_vqe)
                    beta_energy = float(beta_vqe)

                    # Check proximity to reference values
                    alpha_error = abs(alpha_energy - ALPHA_VQE_REF)
                    beta_error = abs(beta_energy - BETA_VQE_REF)

                    if alpha_error < 0.1 and beta_error < 0.1:
                        score += 30
                        feedback_parts.append("✅ Task 1 (VQE): Excellent! Very accurate energies.")
                    elif alpha_error < 0.5 and beta_error < 0.5:
                        score += 20
                        feedback_parts.append("⚠️ Task 1 (VQE): Good energies, but precision can be improved.")
                    else:
                        score += 10
                        feedback_parts.append("⚠️ Task 1 (VQE): Energies calculated but far from expected value.")
                except:
                    feedback_parts.append("❌ Task 1 (VQE): Error processing VQE energies.")
            else:
                feedback_parts.append("❌ Task 1 (VQE): VQE results not found.")            # Task 2: HOMO-LUMO Gap (30 points)
            if alpha_gap is not None and beta_gap is not None:
                try:
                    alpha_gap_val = float(alpha_gap)
                    beta_gap_val = float(beta_gap)

                    # Gaps should be positive and reasonable (0-15 eV typically)
                    if 0 < alpha_gap_val < 15 and 0 < beta_gap_val < 15:
                        score += 30
                        feedback_parts.append(f"✅ Task 2 (HOMO-LUMO): Perfect! Alpha gap: {alpha_gap_val:.2f} eV, Beta gap: {beta_gap_val:.2f} eV")

                        # Bonus for correct interpretation
                        if beta_gap_val < alpha_gap_val:
                            feedback_parts.append("   💡 Beta is more reactive than Alpha (smaller gap)")
                    else:
                        score += 15
                        feedback_parts.append("⚠️ Task 2 (HOMO-LUMO): Gaps calculated but unusual values.")
                except:
                    feedback_parts.append("❌ Task 2 (HOMO-LUMO): Error processing gaps.")
            else:
                feedback_parts.append("❌ Task 2 (HOMO-LUMO): Gap values not found.")

            # Task 3: Quantum State Divergence (40 points)
            if alpha_homo_lumo is not None and beta_homo_lumo is not None:
                try:
                    alpha_hl = float(alpha_homo_lumo)
                    beta_hl = float(beta_homo_lumo)

                    # Check consistency with gaps in eV
                    if alpha_gap is not None and beta_gap is not None:
                        expected_alpha = alpha_gap_val / 27.211  # eV to Hartree
                        expected_beta = beta_gap_val / 27.211

                        alpha_consistency = abs(alpha_hl - expected_alpha) < 0.01
                        beta_consistency = abs(beta_hl - expected_beta) < 0.01

                        if alpha_consistency and beta_consistency:
                            score += 40
                            feedback_parts.append("✅ Task 3 (QSD): Excellent! Complete and consistent analysis.")
                        else:
                            score += 25
                            feedback_parts.append("⚠️ Task 3 (QSD): Results present but inconsistencies in units.")
                    else:
                        score += 20
                        feedback_parts.append("⚠️ Task 3 (QSD): Values present but missing data for verification.")
                except:
                    score += 10
                    feedback_parts.append("⚠️ Task 3 (QSD): Error validating results.")
            else:
                feedback_parts.append("❌ Task 3 (QSD): Quantum state divergence analysis not found.")

            # Final feedback
            feedback = "\n".join(feedback_parts)
            passed = score >= 70

            if passed:
                feedback += f"\n\n🎉 CONGRATULATIONS! You completed the challenge with {score}/100 points."
            else:
                feedback += f"\n\n📚 You need ≥70 points to pass. You have {score}/100."

            return score, passed, feedback, time.time() - start_time

        except Exception as e:
            feedback = f"❌ Evaluation error: {str(e)}\n{traceback.format_exc()}"
            return 0, False, feedback, time.time() - start_time

    @staticmethod
    def evaluate_challenge_35(code: str) -> tuple[int, bool, str, float]:
        """
        Evaluates Challenge 35: A Halloween Carol - Quantum Chemistry Mystery

        Returns:
            tuple: (score, passed, feedback, execution_time)
        """
        start_time = time.time()

        try:
            # Create a namespace to execute the code
            local_scope = {}

            # Execute user code
            exec(code, {}, local_scope)

            # Check that required functions/variables exist
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
                feedback = f"❌ Missing variables/results: {', '.join(missing)}\n"
                feedback += "Make sure to run the entire notebook and have all results."
                return 0, False, feedback, time.time() - start_time

            # Extract results
            alpha_vqe = local_scope.get('alpha_vqe_result')
            beta_vqe = local_scope.get('beta_vqe_result')
            alpha_gap = local_scope.get('alpha_gap_ev')
            beta_gap = local_scope.get('beta_gap_ev')
            alpha_homo_lumo = local_scope.get('alpha_homo_lumo')
            beta_homo_lumo = local_scope.get('beta_homo_lumo')

            # Scoring system
            score = 0
            feedback_parts = []

            # Task 1: VQE Analysis (30 points)
            if alpha_vqe is not None and beta_vqe is not None:
                # Verify results are reasonable
                try:
                    alpha_energy = float(alpha_vqe.eigenvalue) if hasattr(alpha_vqe, 'eigenvalue') else float(alpha_vqe)
                    beta_energy = float(beta_vqe.eigenvalue) if hasattr(beta_vqe, 'eigenvalue') else float(beta_vqe)

                    # Values should be in reasonable range for quantum chemistry
                    if -10 < alpha_energy < 0 and -10 < beta_energy < 0:
                        score += 30
                        feedback_parts.append("✅ Task 1 (VQE): Excellent! Energies calculated correctly.")
                    else:
                        score += 15
                        feedback_parts.append("⚠️ Task 1 (VQE): Energies calculated but seem out of range.")
                except:
                    score += 10
                    feedback_parts.append("⚠️ Task 1 (VQE): Partial results.")
            else:
                feedback_parts.append("❌ Task 1 (VQE): VQE results not found.")

            # Task 2: HOMO-LUMO Gap (30 points)
            if alpha_gap is not None and beta_gap is not None:
                try:
                    alpha_gap_val = float(alpha_gap)
                    beta_gap_val = float(beta_gap)

                    # Gaps should be positive and reasonable (0-15 eV typically)
                    if 0 < alpha_gap_val < 15 and 0 < beta_gap_val < 15:
                        score += 30
                        feedback_parts.append(f"✅ Task 2 (HOMO-LUMO): Perfect! Alpha gap: {alpha_gap_val:.2f} eV, Beta gap: {beta_gap_val:.2f} eV")

                        # Bonus for correct interpretation
                        if beta_gap_val < alpha_gap_val:
                            feedback_parts.append("   💡 Beta is more reactive than Alpha (smaller gap)")
                    else:
                        score += 15
                        feedback_parts.append("⚠️ Task 2 (HOMO-LUMO): Gaps calculated but unusual values.")
                except:
                    score += 10
                    feedback_parts.append("⚠️ Task 2 (HOMO-LUMO): Error processing gaps.")
            else:
                feedback_parts.append("❌ Task 2 (HOMO-LUMO): Gap calculations not found.")

            # Task 3: QSD Analysis (40 points)
            # This is the most complex, verify at least an attempt was made
            qsd_indicators = ['V_alpha', 'V_beta', 'evals_alpha', 'evals_beta', 'fidelity_matrix']
            qsd_present = sum(1 for item in qsd_indicators if item in local_scope)

            if qsd_present >= 3:
                score += 40
                feedback_parts.append("✅ Task 3 (QSD): Excellent! Quantum subspace analysis completed.")
            elif qsd_present >= 2:
                score += 25
                feedback_parts.append("⚠️ Task 3 (QSD): Partial QSD analysis.")
            elif qsd_present >= 1:
                score += 15
                feedback_parts.append("⚠️ Task 3 (QSD): QSD analysis started detected.")
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
            error_msg = f"❌ Evaluation error: {str(e)}\n{traceback.format_exc()}"
            return 0, False, error_msg, execution_time

    @staticmethod
    def evaluate(challenge_id: int, code: str) -> tuple[int, bool, str, float]:
        """
        Main method to evaluate code according to challenge.

        Args:
            challenge_id: Challenge ID
            code: Code to evaluate

        Returns:
            tuple: (score, passed, feedback, execution_time)
        """
        evaluators = {
            35: CodeEvaluator.evaluate_challenge_35,
        }

        evaluator = evaluators.get(challenge_id)

        if not evaluator:
            return 0, False, f"❌ No evaluator for challenge {challenge_id}. Only Challenge 35 is available.", 0.0

        try:
            return evaluator(code)
        except Exception as e:
            return 0, False, f"❌ Critical evaluation error: {str(e)}", 0.0


# Helper function to capture stdout during execution
def capture_stdout(func, *args, **kwargs):
    """Captures stdout during function execution"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        result = func(*args, **kwargs)
        output = sys.stdout.getvalue()
        return result, output
    finally:
        sys.stdout = old_stdout
