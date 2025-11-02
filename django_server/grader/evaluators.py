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
    def evaluate_challenge_35_task1(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 1: VQE Analysis - Binary accept/reject"""
        start_time = time.time()
        try:
            ALPHA_VQE_REF = -12.29314089
            BETA_VQE_REF = 0.00015438
            EPSILON = 0.01        # tolerancia relativa (1%)
            ABS_TOL = 0.001       # tolerancia absoluta fija

            def check_value_in_range(value, reference, epsilon, abs_tol=ABS_TOL):
                # --- Rango relativo ---
                if reference < 0:
                    lower_rel = reference * (1 + epsilon)
                    upper_rel = reference * (1 - epsilon)
                else:
                    lower_rel = reference * (1 - epsilon)
                    upper_rel = reference * (1 + epsilon)

                # --- Rango absoluto ---
                lower_abs = reference - abs_tol
                upper_abs = reference + abs_tol

                # --- Combinar chequeos ---
                in_relative_range = lower_rel <= value <= upper_rel
                in_absolute_range = lower_abs <= value <= upper_abs

                return in_relative_range or in_absolute_range

            alpha_energy = float(results.get('alpha_vqe_result'))
            beta_energy = float(results.get('beta_vqe_result'))

            alpha_ok = check_value_in_range(alpha_energy, ALPHA_VQE_REF, EPSILON)
            beta_ok = check_value_in_range(beta_energy, BETA_VQE_REF, EPSILON)

            if alpha_ok and beta_ok:
                return max_score, True, "✅ Task 1 ACCEPTED", time.time() - start_time
            else:
                return 0, False, "❌ Task 1 REJECTED", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 1 ERROR: {str(e)}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_35_task2(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 2: HOMO-LUMO Gap - Binary accept/reject"""
        start_time = time.time()
        try:
            ALPHA_GAP_EV_REF = 52.00319191407749
            BETA_GAP_EV_REF = 27.211399999999994
            ALPHA_HOMO_LUMO_REF = 1.9110810878557327
            BETA_HOMO_LUMO_REF = 1.0
            EPSILON = 0.01

            def check_value_in_range(value, reference, epsilon):
                if reference < 0:
                    lower = reference * (1 + epsilon)
                    upper = reference * (1 - epsilon)
                else:
                    lower = reference * (1 - epsilon)
                    upper = reference * (1 + epsilon)
                return lower <= value <= upper

            alpha_gap = float(results.get('alpha_gap_ev'))
            beta_gap = float(results.get('beta_gap_ev'))
            alpha_hl = float(results.get('alpha_homo_lumo'))
            beta_hl = float(results.get('beta_homo_lumo'))

            all_ok = (
                check_value_in_range(alpha_gap, ALPHA_GAP_EV_REF, EPSILON) and
                check_value_in_range(beta_gap, BETA_GAP_EV_REF, EPSILON) and
                check_value_in_range(alpha_hl, ALPHA_HOMO_LUMO_REF, EPSILON) and
                check_value_in_range(beta_hl, BETA_HOMO_LUMO_REF, EPSILON)
            )

            if all_ok:
                return max_score, True, "✅ Task 2 ACCEPTED", time.time() - start_time
            else:
                return 0, False, "❌ Task 2 REJECTED", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 2 ERROR: {str(e)}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_35_task3(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 3: QSD - Binary accept/reject"""
        start_time = time.time()
        try:
            ALPHA_INDEX_REF = 1
            BETA_INDEX_REF = 0
            FIDELITY_REF = 1.0
            EPSILON = 0.01

            def check_value_in_range(value, reference, epsilon):
                if reference < 0:
                    lower = reference * (1 + epsilon)
                    upper = reference * (1 - epsilon)
                else:
                    lower = reference * (1 - epsilon)
                    upper = reference * (1 + epsilon)
                return lower <= value <= upper

            alpha_idx = int(results.get('alpha_index'))
            beta_idx = int(results.get('beta_index'))
            fidelity = float(results.get('fidelity'))

            indices_ok = (alpha_idx == ALPHA_INDEX_REF and beta_idx == BETA_INDEX_REF)
            fidelity_ok = check_value_in_range(fidelity, FIDELITY_REF, EPSILON)

            if indices_ok and fidelity_ok:
                return max_score, True, "✅ Task 3 ACCEPTED", time.time() - start_time
            else:
                return 0, False, "❌ Task 3 REJECTED", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 3 ERROR: {str(e)}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_35_task4(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 4: Final Energy Beta - Binary accept/reject"""
        start_time = time.time()
        try:
            FINAL_ENERGY_BETA_REF = 0.0006559581843628555
            EPSILON = 0.01

            energy_beta = float(results.get('final_energy_beta'))
            lower = FINAL_ENERGY_BETA_REF * (1 - EPSILON)
            upper = FINAL_ENERGY_BETA_REF * (1 + EPSILON)

            if lower <= energy_beta <= upper:
                return max_score, True, "✅ Task 4 ACCEPTED", time.time() - start_time
            else:
                return 0, False, "❌ Task 4 REJECTED", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 4 ERROR: {str(e)}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_35_task5(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 5: Final Energy Perturbed - Binary accept/reject"""
        start_time = time.time()
        try:
            FINAL_ENERGY_PERTURBED_REF = -12.294612921331247
            EPSILON = 0.01

            energy_perturbed = float(results.get('final_energy_perturbed'))
            # Handle negative reference
            lower = FINAL_ENERGY_PERTURBED_REF * (1 + EPSILON)
            upper = FINAL_ENERGY_PERTURBED_REF * (1 - EPSILON)

            if lower <= energy_perturbed <= upper:
                return max_score, True, "✅ Task 5 ACCEPTED", time.time() - start_time
            else:
                return 0, False, "❌ Task 5 REJECTED", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 5 ERROR: {str(e)}", time.time() - start_time

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
                'task3': ['alpha_index', 'beta_index', 'fidelity'],
                'task4': ['final_energy_beta'],
                'task5': ['final_energy_perturbed']
            }

            # Flatten all required items
            all_required = []
            for task_items in required_items.values():
                all_required.extend(task_items)

            missing = [item for item in all_required if item not in results]

            if missing:
                feedback = f"❌ Missing results: {', '.join(missing)}\n"
                feedback += "You must send all required variables for all 5 tasks."
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
            final_energy_beta = results.get('final_energy_beta')
            final_energy_perturbed = results.get('final_energy_perturbed')

            # Scoring system
            score = 0
            feedback_parts = []

            # NEW REFERENCE VALUES
            ALPHA_VQE_REF = -12.29314089
            BETA_VQE_REF = 0.00015438
            ALPHA_GAP_EV_REF = 52.00319191407749
            BETA_GAP_EV_REF = 27.211399999999994
            ALPHA_HOMO_LUMO_REF = 1.9110810878557327
            BETA_HOMO_LUMO_REF = 1.0
            ALPHA_INDEX_REF = 1
            BETA_INDEX_REF = 0
            FIDELITY_REF = 1.0
            FINAL_ENERGY_BETA_REF = 0.0006559581843628555
            FINAL_ENERGY_PERTURBED_REF = -12.294612921331247

            # Error margin (epsilon) - 1% for all tasks
            EPSILON = 0.01

            def check_value_in_range(value, reference, epsilon):
                """Check if value is within epsilon% of reference (handles negative values)"""
                if reference < 0:
                    lower = reference * (1 + epsilon)
                    upper = reference * (1 - epsilon)
                else:
                    lower = reference * (1 - epsilon)
                    upper = reference * (1 + epsilon)
                return lower <= value <= upper

            # TASK 1: VQE Analysis (20 points) - BINARY: Accept or Reject
            task1_score = 0
            try:
                alpha_energy = float(alpha_vqe)
                beta_energy = float(beta_vqe)

                # Check if values are within epsilon range
                alpha_in_range = check_value_in_range(alpha_energy, ALPHA_VQE_REF, EPSILON)
                beta_in_range = check_value_in_range(beta_energy, BETA_VQE_REF, EPSILON)

                if alpha_in_range and beta_in_range:
                    task1_score = 20
                    feedback_parts.append(f"✅ Task 1 ACCEPTED (20 pts)")
                else:
                    task1_score = 0
                    feedback_parts.append(f"❌ Task 1 REJECTED (0 pts)")

                score += task1_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 1 ERROR (0 pts): {str(e)}")

            # TASK 2: HOMO-LUMO Gap (20 points)
            task2_score = 0
            try:
                alpha_gap_val = float(alpha_gap)
                beta_gap_val = float(beta_gap)
                alpha_hl = float(alpha_homo_lumo)
                beta_hl = float(beta_homo_lumo)

                # Check if all values are within epsilon range
                alpha_gap_ok = check_value_in_range(alpha_gap_val, ALPHA_GAP_EV_REF, EPSILON)
                beta_gap_ok = check_value_in_range(beta_gap_val, BETA_GAP_EV_REF, EPSILON)
                alpha_hl_ok = check_value_in_range(alpha_hl, ALPHA_HOMO_LUMO_REF, EPSILON)
                beta_hl_ok = check_value_in_range(beta_hl, BETA_HOMO_LUMO_REF, EPSILON)

                if alpha_gap_ok and beta_gap_ok and alpha_hl_ok and beta_hl_ok:
                    task2_score = 20
                    feedback_parts.append(f"✅ Task 2 (HOMO-LUMO): Perfect! All values accurate.")
                else:
                    errors = []
                    if not alpha_gap_ok:
                        err = abs((alpha_gap_val - ALPHA_GAP_EV_REF) / ALPHA_GAP_EV_REF) * 100
                        errors.append(f"α_gap: {err:.2f}%")
                    if not beta_gap_ok:
                        err = abs((beta_gap_val - BETA_GAP_EV_REF) / BETA_GAP_EV_REF) * 100
                        errors.append(f"β_gap: {err:.2f}%")
                    if not alpha_hl_ok:
                        err = abs((alpha_hl - ALPHA_HOMO_LUMO_REF) / ALPHA_HOMO_LUMO_REF) * 100
                        errors.append(f"α_hl: {err:.2f}%")
                    if not beta_hl_ok:
                        err = abs((beta_hl - BETA_HOMO_LUMO_REF) / BETA_HOMO_LUMO_REF) * 100
                        errors.append(f"β_hl: {err:.2f}%")
                    feedback_parts.append(f"❌ Task 2 (HOMO-LUMO): Outside acceptable range. Errors: {', '.join(errors)}")

                score += task2_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 2 (HOMO-LUMO): Error processing - {str(e)}")

            # TASK 3: QSD - Quantum State Divergence (30 points)
            task3_score = 0
            try:
                alpha_idx = int(alpha_index)
                beta_idx = int(beta_index)
                fid = float(fidelity)

                # Check indices (exact match required)
                indices_correct = (alpha_idx == ALPHA_INDEX_REF and beta_idx == BETA_INDEX_REF)

                # Check fidelity with epsilon range
                fidelity_correct = check_value_in_range(fid, FIDELITY_REF, EPSILON)

                if indices_correct and fidelity_correct:
                    task3_score = 30
                    feedback_parts.append(f"✅ Task 3 (QSD): Perfect! Correct state matching α[{alpha_idx}]↔β[{beta_idx}], F={fid:.6f}")
                elif indices_correct:
                    fid_error = abs((fid - FIDELITY_REF) / FIDELITY_REF) * 100
                    feedback_parts.append(f"⚠️ Task 3 (QSD): Indices correct but fidelity outside range (error: {fid_error:.2f}%)")
                elif fidelity_correct:
                    feedback_parts.append(f"⚠️ Task 3 (QSD): Fidelity correct but wrong indices. Expected α[{ALPHA_INDEX_REF}]↔β[{BETA_INDEX_REF}], got α[{alpha_idx}]↔β[{beta_idx}]")
                else:
                    feedback_parts.append(f"❌ Task 3 (QSD): Incorrect. Got α[{alpha_idx}]↔β[{beta_idx}], F={fid:.6f}")

                score += task3_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 3 (QSD): Error processing - {str(e)}")

            # TASK 4: Final Energy Beta (15 points)
            task4_score = 0
            try:
                energy_beta = float(final_energy_beta)

                # Calculate bounds with epsilon margin
                lower_bound = FINAL_ENERGY_BETA_REF * (1 - EPSILON)
                upper_bound = FINAL_ENERGY_BETA_REF * (1 + EPSILON)

                if lower_bound <= energy_beta <= upper_bound:
                    task4_score = 15
                    feedback_parts.append(f"✅ Task 4 (Final Energy Beta): Perfect! Value={energy_beta:.10f}")
                else:
                    error_percent = abs((energy_beta - FINAL_ENERGY_BETA_REF) / FINAL_ENERGY_BETA_REF) * 100
                    feedback_parts.append(f"❌ Task 4 (Final Energy Beta): Outside acceptable range. Value={energy_beta:.10f} (error: {error_percent:.2f}%)")

                score += task4_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 4 (Final Energy Beta): Error processing - {str(e)}")

            # TASK 5: Final Energy Perturbed (15 points)
            task5_score = 0
            try:
                energy_perturbed = float(final_energy_perturbed)

                # Calculate bounds with epsilon margin (handle negative values correctly)
                if FINAL_ENERGY_PERTURBED_REF < 0:
                    lower_bound = FINAL_ENERGY_PERTURBED_REF * (1 + EPSILON)
                    upper_bound = FINAL_ENERGY_PERTURBED_REF * (1 - EPSILON)
                else:
                    lower_bound = FINAL_ENERGY_PERTURBED_REF * (1 - EPSILON)
                    upper_bound = FINAL_ENERGY_PERTURBED_REF * (1 + EPSILON)

                if lower_bound <= energy_perturbed <= upper_bound:
                    task5_score = 15
                    feedback_parts.append(f"✅ Task 5 (Final Energy Perturbed): Perfect! Value={energy_perturbed:.10f}")
                else:
                    error_percent = abs((energy_perturbed - FINAL_ENERGY_PERTURBED_REF) / FINAL_ENERGY_PERTURBED_REF) * 100
                    feedback_parts.append(f"❌ Task 5 (Final Energy Perturbed): Outside acceptable range. Value={energy_perturbed:.10f} (error: {error_percent:.2f}%)")

                score += task5_score
            except Exception as e:
                feedback_parts.append(f"❌ Task 5 (Final Energy Perturbed): Error processing - {str(e)}")

            # Final feedback
            feedback = "\n".join(feedback_parts)
            passed = score >= 70

            feedback += f"\n\n📊 Total Score: {score}/100 (Task1: {task1_score}/20, Task2: {task2_score}/20, Task3: {task3_score}/30, Task4: {task4_score}/15, Task5: {task5_score}/15)"

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
    def evaluate_challenge_36_results(results: dict) -> tuple[int, bool, str, float]:
        """
        Evaluates Challenge 36 using provided results (no code execution).

        Expected keys in results dict:
          - 'task361_predictions' (iterable)
          - 'task361_y_test_hidden' (iterable)
          - 'task362_generated_images' (np.ndarray-like)
          - 'task362_test_clean' (np.ndarray-like)
          - 'task362_generated_shapes' (tuple)
          - 'task363_total_rewards' (iterable of numbers)

        Returns: (score, passed, feedback, execution_time)
        """
        start_time = time.time()
        try:
            import numpy as np

            # Required keys
            required = [
                'task361_predictions', 'task361_y_test_hidden',
                'task362_generated_images', 'task362_test_clean', 'task362_generated_shapes',
                'task363_total_rewards'
            ]

            missing = [k for k in required if k not in results]
            if missing:
                feedback = f"❌ Missing results: {', '.join(missing)}"
                return 0, False, feedback, time.time() - start_time

            score = 0
            feedback_parts = []

            # TASK 361: classification accuracy >= 0.98 (20 pts)
            try:
                preds = np.asarray(results.get('task361_predictions'))
                y_hidden = np.asarray(results.get('task361_y_test_hidden'))
                acc = np.mean(preds == y_hidden)
                if acc >= 0.98:
                    score += 20
                    feedback_parts.append(f"✅ Task 361: Accuracy {acc:.4f} — ACCEPTED (20 pts)")
                else:
                    feedback_parts.append(f"❌ Task 361: Accuracy {acc:.4f} — REJECTED (0 pts)")
            except Exception as e:
                feedback_parts.append(f"❌ Task 361 ERROR: {str(e)}")

            # TASK 362: image generation MSE <= 0.05 and shapes == (50,16) (20 pts)
            try:
                gen = np.asarray(results.get('task362_generated_images'))
                clean = np.asarray(results.get('task362_test_clean'))
                shapes = tuple(results.get('task362_generated_shapes'))

                mse = float(np.mean((gen - clean) ** 2))
                shape_ok = shapes == (50, 16)

                if mse <= 0.05 and shape_ok:
                    score += 20
                    feedback_parts.append(f"✅ Task 362: MSE={mse:.6f}, shape={shapes} — ACCEPTED (20 pts)")
                else:
                    reasons = []
                    if mse > 0.05:
                        reasons.append(f"MSE={mse:.6f} (too high)")
                    if not shape_ok:
                        reasons.append(f"shape={shapes} (incorrect)")
                    feedback_parts.append(f"❌ Task 362: REJECTED ({'; '.join(reasons)})")
            except Exception as e:
                feedback_parts.append(f"❌ Task 362 ERROR: {str(e)}")

            # TASK 363: mean(total_rewards) > 0 (20 pts)
            try:
                rewards = np.asarray(results.get('task363_total_rewards'))
                mean_reward = float(np.mean(rewards))
                if mean_reward > 0:
                    score += 20
                    feedback_parts.append(f"✅ Task 363: Mean reward {mean_reward:.6f} — ACCEPTED (20 pts)")
                else:
                    feedback_parts.append(f"❌ Task 363: Mean reward {mean_reward:.6f} — REJECTED (0 pts)")
            except Exception as e:
                feedback_parts.append(f"❌ Task 363 ERROR: {str(e)}")
            # For Challenge 36 total max = 60 (3 tasks * 20). Keep same 70% pass threshold => 42
            passed = score >= 42
            feedback = "\n".join(feedback_parts)
            feedback += f"\n\n📊 Total Score: {score}/60"
            if passed:
                feedback += "\n🎉 CONGRATULATIONS! You passed Challenge 36."
            else:
                feedback += "\n📚 You need ≥70% to pass (>=42/60)."

            return score, passed, feedback, time.time() - start_time

        except Exception as e:
            return 0, False, f"❌ Evaluation error: {str(e)}\n{traceback.format_exc()}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_36_task1(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 361: classification accuracy >= 0.98 (binary accept/reject)"""
        start_time = time.time()
        try:
            import numpy as np
            preds = np.asarray(results.get('task361_predictions'))
            y_hidden = np.asarray(results.get('task361_y_test_hidden'))
            acc = float(np.mean(preds == y_hidden))
            if acc >= 0.98:
                return max_score, True, "✅ Task 361 ACCEPTED", time.time() - start_time
            else:
                return 0, False, f"❌ Task 361 REJECTED (accuracy={acc:.4f})", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 361 ERROR: {str(e)}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_36_task2(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 362: image generation MSE and shape check (binary accept/reject)"""
        start_time = time.time()
        try:
            import numpy as np
            gen = np.asarray(results.get('task362_generated_images'))
            clean = np.asarray(results.get('task362_test_clean'))
            shapes = tuple(results.get('task362_generated_shapes'))

            mse = float(np.mean((gen - clean) ** 2))
            shape_ok = shapes == (50, 16)

            if mse <= 0.05 and shape_ok:
                return max_score, True, "✅ Task 362 ACCEPTED", time.time() - start_time
            else:
                reasons = []
                if mse > 0.05:
                    reasons.append(f"MSE={mse:.6f} (too high)")
                if not shape_ok:
                    reasons.append(f"shape={shapes} (incorrect)")
                return 0, False, f"❌ Task 362 REJECTED ({'; '.join(reasons)})", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 362 ERROR: {str(e)}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_36_task3(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 363: mean(total_rewards) > 0 (binary accept/reject)"""
        start_time = time.time()
        try:
            import numpy as np
            rewards = np.asarray(results.get('task363_total_rewards'))
            mean_reward = float(np.mean(rewards))
            if mean_reward > 0:
                return max_score, True, "✅ Task 363 ACCEPTED", time.time() - start_time
            else:
                return 0, False, f"❌ Task 363 REJECTED (mean_reward={mean_reward:.6f})", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Task 363 ERROR: {str(e)}", time.time() - start_time

    @staticmethod
    def evaluate_challenge_36(code: str) -> tuple[int, bool, str, float]:
        """
        Executes code for Challenge 36 and checks for required variables.

        Expected variables created by executed code:
          - 'task361_predictions', 'task361_y_test_hidden',
          - 'task362_generated_images', 'task362_test_clean', 'task362_generated_shapes',
          - 'task363_total_rewards'

        This mirrors `evaluate_challenge_36_results` but extracts values from executed namespace.
        """
        start_time = time.time()
        try:
            local_scope = {}
            exec(code, {}, local_scope)

            required = [
                'task361_predictions', 'task361_y_test_hidden',
                'task362_generated_images', 'task362_test_clean', 'task362_generated_shapes',
                'task363_total_rewards'
            ]

            missing = [k for k in required if k not in local_scope]
            if missing:
                feedback = f"❌ Missing variables: {', '.join(missing)}\nMake sure your notebook/code sets the required variables."
                return 0, False, feedback, time.time() - start_time

            # Build results dict and delegate to results-based evaluator
            results = {k: local_scope.get(k) for k in required}
            return CodeEvaluator.evaluate_challenge_36_results(results)

        except SyntaxError as e:
            return 0, False, f"❌ Syntax error: {str(e)}", time.time() - start_time
        except Exception as e:
            return 0, False, f"❌ Evaluation error: {str(e)}\n{traceback.format_exc()}", time.time() - start_time

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
            36: CodeEvaluator.evaluate_challenge_36,
        }

        evaluator = evaluators.get(challenge_id)

        if not evaluator:
            return 0, False, f"❌ No evaluator for challenge {challenge_id}. Only Challenge 35 is available.", 0.0

        try:
            return evaluator(code)
        except Exception as e:
            return 0, False, f"❌ Critical evaluation error: {str(e)}", 0.0

    # -------------------- Challenge 37: server-side individual task evaluators --------------------
    @staticmethod
    def evaluate_challenge_37_task371(results: dict, max_score: int = 10) -> tuple[int, bool, str, float]:
        """Task 1.1 for Challenge 37 (serialized client payload)

        Mirrors server_grade_task_1_1 from the challenge reference.
        """
        import time
        start = time.time()
        try:
            # Expecting keys: num_qubits, num_clbits, ops, counts
            score = int(results.get('score', 0)) if 'score' in results else 0
            # If results contain the detailed dict produced by client_task_1_1, compute same scoring
            num_qubits = results.get('num_qubits')
            if num_qubits != 2:
                return 0, False, "❌ Circuit should have exactly 2 qubits", time.time() - start

            feedback_lines = []
            ops = results.get('ops', [])

            score = 0
            if 'h' in ops:
                score += 3
                feedback_lines.append("✓ Hadamard gate found")
            else:
                feedback_lines.append("❌ Missing Hadamard gate")

            if 'cx' in ops:
                score += 3
                feedback_lines.append("✓ CNOT gate found")
            else:
                feedback_lines.append("❌ Missing CNOT gate")

            if 'measure' in ops:
                score += 2
                feedback_lines.append("✓ Measurement operations found")
            else:
                feedback_lines.append("❌ Missing measurement operations")

            counts = results.get('counts', {}) or {}
            total_shots = sum(counts.values()) if counts else 0
            bell_states = counts.get('00', 0) + counts.get('11', 0)
            bell_ratio = (bell_states / total_shots) if total_shots > 0 else 0.0

            if bell_ratio >= 0.95:
                score += 2
                feedback_lines.append(f"✓ Excellent Bell state: {bell_ratio:.2%} correct outcomes")
            elif bell_ratio >= 0.85:
                score += 1
                feedback_lines.append(f"⚠️ Good Bell state: {bell_ratio:.2%} correct outcomes")
            else:
                feedback_lines.append(f"❌ Poor Bell state: {bell_ratio:.2%} correct outcomes")

            passed = score >= max_score * 0.7
            return score, passed, "\n".join(feedback_lines), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start

    @staticmethod
    def evaluate_challenge_37_task372(results: dict, max_score: int = 10) -> tuple[int, bool, str, float]:
        """Task 1.2 for Challenge 37 (noise model)"""
        import time
        start = time.time()
        try:
            score = 0
            feedback = []
            if results is None:
                return 0, False, "❌ Noise model not created", time.time() - start

            if results.get('has_structure'):
                score += 5
                feedback.append("✓ Noise model structure is correct")
            else:
                feedback.append("❌ Invalid noise model structure")

            counts_noisy = results.get('counts_noisy', {}) or {}
            wrong_states = counts_noisy.get('01', 0) + counts_noisy.get('10', 0)
            total = sum(counts_noisy.values()) if counts_noisy else 0
            error_rate = (wrong_states / total) if total > 0 else 0.0

            if 0.05 <= error_rate <= 0.30:
                score += 5
                feedback.append(f"✓ Realistic noise level detected: {error_rate:.2%} errors")
            elif error_rate > 0:
                score += 3
                feedback.append(f"⚠️ Noise detected but unusual level: {error_rate:.2%}")
            else:
                feedback.append("❌ No noise effect detected")

            passed = score >= max_score * 0.7
            return score, passed, "\n".join(feedback), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start

    @staticmethod
    def evaluate_challenge_37_task373(results: dict, max_score: int = 15) -> tuple[int, bool, str, float]:
        """Task 1.3 for Challenge 37 (fidelity vs noise)"""
        import time
        start = time.time()
        try:
            score = 0
            feedback = []
            test_noise_levels = results.get('noise_levels', [])
            fidelities = results.get('fidelities', [])

            if len(fidelities) != len(test_noise_levels):
                return 0, False, "❌ Function should return same number of fidelities as noise levels", time.time() - start

            if fidelities and fidelities[0] >= 0.98:
                score += 3
                feedback.append(f"✓ Perfect fidelity at 0% noise: {fidelities[0]:.4f}")
            else:
                feedback.append(f"⚠️ Low fidelity at 0% noise: {fidelities[0] if fidelities else 'N/A'}")

            is_decreasing = all(fidelities[i] >= fidelities[i+1] for i in range(len(fidelities)-1)) if fidelities else False
            if is_decreasing:
                score += 5
                feedback.append("✓ Fidelity correctly decreases with noise")
            else:
                feedback.append("❌ Fidelity should decrease monotonically with noise")

            if fidelities and 0.85 <= fidelities[2] <= 0.95:
                score += 4
                feedback.append(f"✓ Realistic fidelity at 10% noise: {fidelities[2]:.4f}")
            else:
                score += 2
                feedback.append(f"⚠️ Unusual fidelity at 10% noise: {fidelities[2] if len(fidelities) > 2 else 'N/A'}")

            if fidelities and fidelities[-1] >= 0.5:
                score += 3
                feedback.append(f"✓ Reasonable fidelity at 20% noise: {fidelities[-1]:.4f}")
            else:
                feedback.append(f"⚠️ Very low fidelity at 20% noise: {fidelities[-1] if fidelities else 'N/A'}")

            passed = score >= max_score * 0.7
            return score, passed, "\n".join(feedback), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start

    @staticmethod
    def evaluate_challenge_37_task374(results: dict, max_score: int = 15) -> tuple[int, bool, str, float]:
        """Task 2.1: three-qubit encoding"""
        import time
        start = time.time()
        try:
            score = 0
            feedback = []
            cx_count = results.get('cx_count', 0)
            if cx_count == 2:
                score += 5
                feedback.append("✓ Correct number of CNOT gates (2)")
            else:
                feedback.append(f"❌ Expected 2 CNOT gates, found {cx_count}")

            overlap = float(results.get('overlap', 0.0))
            if overlap >= 0.99:
                score += 10
                feedback.append(f"✓ Perfect encoding: |1⟩ → |111⟩ (fidelity: {overlap:.4f})")
            elif overlap >= 0.90:
                score += 7
                feedback.append(f"⚠️ Good encoding but not perfect (fidelity: {overlap:.4f})")
            else:
                feedback.append(f"❌ Incorrect encoding (fidelity: {overlap:.4f})")

            passed = score >= max_score * 0.7
            return score, passed, "\n".join(feedback), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start

    @staticmethod
    def evaluate_challenge_37_task375(results: dict, max_score: int = 15) -> tuple[int, bool, str, float]:
        """Task 2.2: syndrome measurement"""
        import time
        start = time.time()
        try:
            score = 0
            feedback = []
            counts_map = results.get('counts_by_error', {}) or {}
            expected_syndromes = {0: '10', 1: '11', 2: '01'}
            for error_qubit in [0, 1, 2]:
                counts = counts_map.get(str(error_qubit), {})
                if counts:
                    most_common = max(counts, key=counts.get)
                else:
                    most_common = ''
                if most_common == expected_syndromes[error_qubit]:
                    score += 5
                    feedback.append(f"✓ Correct syndrome for error on qubit {error_qubit}: {most_common}")
                else:
                    feedback.append(f"❌ Wrong syndrome for error on qubit {error_qubit}: got {most_common}, expected {expected_syndromes[error_qubit]}")

            passed = score >= max_score * 0.7
            return score, passed, "\n".join(feedback), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start

    @staticmethod
    def evaluate_challenge_37_task376(results: dict, max_score: int = 20) -> tuple[int, bool, str, float]:
        """Task 3.2: error correction effectiveness"""
        import time
        import numpy as _np
        start = time.time()
        try:
            unprotected_list = results.get('unprotected', [])
            protected_list = results.get('protected', [])
            all_improvements = []
            for up, pr in zip(unprotected_list, protected_list):
                if pr > up:
                    improvement = (pr - up) / (up + 1e-6) * 100
                    all_improvements.append(improvement)

            if len(all_improvements) == 5:
                score = 5
                feedback = ["✓ Both functions work with hidden test cases"]
            else:
                return 0, False, "❌ Functions failed on some hidden test cases", time.time() - start

            avg_improvement = float(_np.mean(all_improvements))
            if avg_improvement >= 50:
                score += 15
                feedback.append(f"✓ Excellent error correction: {avg_improvement:.1f}% average improvement")
            elif avg_improvement >= 30:
                score += 12
                feedback.append(f"✓ Good error correction: {avg_improvement:.1f}% average improvement")
            elif avg_improvement >= 10:
                score += 10
                feedback.append(f"✓ Modest error correction: {avg_improvement:.1f}% average improvement")
            else:
                feedback.append(f"❌ Insufficient error correction: {avg_improvement:.1f}% average improvement")

            passed = score >= max_score * 0.7
            return score, passed, "\n".join(feedback), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start

    @staticmethod
    def evaluate_challenge_37_task377(results: dict, max_score: int = 10) -> tuple[int, bool, str, float]:
        """Task 4.1: Shor code encoding"""
        import time
        start = time.time()
        try:
            h_count = results.get('h_count', 0)
            cx_count = results.get('cx_count', 0)
            score = 0
            feedback = []
            if h_count == 3:
                score += 3
                feedback.append("✓ Correct number of Hadamard gates (3)")
            else:
                feedback.append(f"⚠️ Expected 3 Hadamard gates, found {h_count}")

            if cx_count == 8:
                score += 4
                feedback.append("✓ Correct number of CNOT gates (8)")
            elif 6 <= cx_count <= 10:
                score += 2
                feedback.append(f"⚠️ Close number of CNOT gates: {cx_count}")
            else:
                feedback.append(f"❌ Expected 8 CNOT gates, found {cx_count}")

            if results.get('num_qubits', 0) >= 9:
                score += 3
                feedback.append("✓ Circuit uses at least 9 qubits")
            else:
                feedback.append("❌ Shor code requires 9 qubits")

            passed = score >= max_score * 0.6
            return score, passed, "\n".join(feedback), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start

    @staticmethod
    def evaluate_challenge_37_task378(results: dict, max_score: int = 5) -> tuple[int, bool, str, float]:
        """Task 4.2: Shor syndrome measurement"""
        import time
        start = time.time()
        try:
            cx_count = results.get('cx_count', 0)
            measure_count = results.get('measure_count', 0)
            score = 0
            feedback = []
            if cx_count == 12:
                score += 3
                feedback.append("✓ Correct number of CNOT gates for syndrome (12)")
            elif 10 <= cx_count <= 14:
                score += 2
                feedback.append(f"⚠️ Close to correct CNOT count: {cx_count}")
            else:
                feedback.append(f"❌ Expected ~12 CNOT gates, found {cx_count}")

            if measure_count == 6:
                score += 2
                feedback.append("✓ Correct number of measurements (6)")
            else:
                feedback.append(f"⚠️ Expected 6 measurements, found {measure_count}")

            passed = score >= max_score * 0.6
            return score, passed, "\n".join(feedback), time.time() - start
        except Exception as e:
            return 0, False, f"❌ Error during evaluation: {str(e)}", time.time() - start


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

