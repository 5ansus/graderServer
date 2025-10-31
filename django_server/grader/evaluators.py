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
        Updated with new reference values for 3 separate tasks.

        Args:
            results: Dictionary with required variables

        Returns:
            tuple: (score, passed, feedback, execution_time)
        """
        start_time = time.time()

        try:
            # Check that required variables exist for all tasks
            required_items = {
                'task1': ['alpha_vqe_result', 'beta_vqe_result'],
                'task2': ['alpha_gap_ev', 'beta_gap_ev', 'alpha_homo_lumo', 'beta_homo_lumo'],
                'task3': ['alpha_index', 'beta_index', 'fidelity']
            }

            # Flatten all required items
            all_required = []
            for task_items in required_items.values():
                all_required.extend(task_items)

            missing = [item for item in all_required if item not in results]

            if missing:
                feedback = f"❌ Missing results: {', '.join(missing)}\n"
                feedback += "You must send all required variables for all 3 tasks."
                return 0, False, feedback, time.time() - start_time

            # Extract results
            alpha_vqe = results.get('alpha_vqe_result')
            beta_vqe = results.get('beta_vqe_result')
            alpha_gap = results.get('alpha_gap_ev')
            beta_gap = results.get('beta_gap_ev')
            alpha_homo_lumo = results.get('alpha_homo_lumo')
            beta_homo_lumo = results.get('beta_homo_lumo')
            alpha_index = results.get('alpha_index')
            beta_index = results.get('beta_index')
            fidelity = results.get('fidelity')

            # Scoring system
            score = 0
            feedback_parts = []

            # NEW REFERENCE VALUES
            ALPHA_VQE_REF = -12.29314089
            BETA_VQE_REF = 0.00015438
            ALPHA_GAP_EV_REF = 52.00319191407749
            BETA_GAP_EV_REF = 27.211399999999994
            ALPHA_HOMO_LUMO_REF = 1.9110810878557327
            BETA_HOMO_LUMO_REF = 1.0  # Can be 0.9999999999999998 or 1
            ALPHA_INDEX_REF = 1
            BETA_INDEX_REF = 0
            FIDELITY_REF = 1.0

            # TASK 1: VQE Analysis (30 points)
            task1_score = 0
            try:
                alpha_energy = float(alpha_vqe)
                beta_energy = float(beta_vqe)

                # Check proximity to reference values
                alpha_error = abs(alpha_energy - ALPHA_VQE_REF)
                beta_error = abs(beta_energy - BETA_VQE_REF)

                # Relative error for better scoring
                alpha_rel_error = alpha_error / abs(ALPHA_VQE_REF) if ALPHA_VQE_REF != 0 else alpha_error
                beta_rel_error = beta_error / abs(BETA_VQE_REF) if BETA_VQE_REF != 0 else beta_error

                if alpha_rel_error < 0.01 and beta_rel_error < 0.1:
                    task1_score = 30
                    feedback_parts.append(f"✅ Task 1 (VQE): Perfect! α={alpha_energy:.8f}, β={beta_energy:.8f}")
                elif alpha_rel_error < 0.05 and beta_rel_error < 0.5:
                    task1_score = 20
                    feedback_parts.append(f"⚠️ Task 1 (VQE): Good, but can improve precision. α={alpha_energy:.8f}, β={beta_energy:.8f}")
                else:
                    task1_score = 10
                    feedback_parts.append(f"⚠️ Task 1 (VQE): Calculated but far from reference. α={alpha_energy:.8f}, β={beta_energy:.8f}")

                score += task1_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 1 (VQE): Error processing - {str(e)}")

            # TASK 2: HOMO-LUMO Gap (30 points)
            task2_score = 0
            try:
                alpha_gap_val = float(alpha_gap)
                beta_gap_val = float(beta_gap)
                alpha_hl = float(alpha_homo_lumo)
                beta_hl = float(beta_homo_lumo)

                # Check gaps
                gap_error_alpha = abs(alpha_gap_val - ALPHA_GAP_EV_REF)
                gap_error_beta = abs(beta_gap_val - BETA_GAP_EV_REF)

                # Check HOMO-LUMO values
                hl_error_alpha = abs(alpha_hl - ALPHA_HOMO_LUMO_REF)
                hl_error_beta = abs(beta_hl - BETA_HOMO_LUMO_REF)

                # Relative errors
                gap_rel_alpha = gap_error_alpha / ALPHA_GAP_EV_REF
                gap_rel_beta = gap_error_beta / BETA_GAP_EV_REF
                hl_rel_alpha = hl_error_alpha / ALPHA_HOMO_LUMO_REF
                hl_rel_beta = hl_error_beta / BETA_HOMO_LUMO_REF

                if (gap_rel_alpha < 0.01 and gap_rel_beta < 0.01 and
                    hl_rel_alpha < 0.01 and hl_rel_beta < 0.01):
                    task2_score = 30
                    feedback_parts.append(f"✅ Task 2 (HOMO-LUMO): Perfect! All values accurate.")
                elif (gap_rel_alpha < 0.05 and gap_rel_beta < 0.05 and
                      hl_rel_alpha < 0.05 and hl_rel_beta < 0.05):
                    task2_score = 20
                    feedback_parts.append(f"⚠️ Task 2 (HOMO-LUMO): Good, small deviations present.")
                else:
                    task2_score = 10
                    feedback_parts.append(f"⚠️ Task 2 (HOMO-LUMO): Calculated but significant deviations.")

                score += task2_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 2 (HOMO-LUMO): Error processing - {str(e)}")

            # TASK 3: QSD - Quantum State Divergence (40 points)
            task3_score = 0
            try:
                alpha_idx = int(alpha_index)
                beta_idx = int(beta_index)
                fid = float(fidelity)

                # Check indices
                indices_correct = (alpha_idx == ALPHA_INDEX_REF and beta_idx == BETA_INDEX_REF)

                # Check fidelity (allow small numerical errors)
                fidelity_error = abs(fid - FIDELITY_REF)
                fidelity_correct = fidelity_error < 0.01

                if indices_correct and fidelity_correct:
                    task3_score = 40
                    feedback_parts.append(f"✅ Task 3 (QSD): Perfect! Correct state matching α[{alpha_idx}]↔β[{beta_idx}], F={fid:.6f}")
                elif indices_correct or fidelity_correct:
                    task3_score = 25
                    feedback_parts.append(f"⚠️ Task 3 (QSD): Partial credit - indices or fidelity correct.")
                else:
                    task3_score = 10
                    feedback_parts.append(f"⚠️ Task 3 (QSD): Incorrect matching. Got α[{alpha_idx}]↔β[{beta_idx}], F={fid:.6f}")

                score += task3_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 3 (QSD): Error processing - {str(e)}")

            # Final feedback
            feedback = "\n".join(feedback_parts)
            passed = score >= 70

            feedback += f"\n\n📊 Total Score: {score}/100 (Task1: {task1_score}/30, Task2: {task2_score}/30, Task3: {task3_score}/40)"

            if passed:
                feedback += f"\n🎉 CONGRATULATIONS! You passed the challenge!"
            else:
                feedback += f"\n📚 You need ≥70 points to pass. Keep trying!"

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
