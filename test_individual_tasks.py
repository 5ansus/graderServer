"""
Test individual task submissions for Challenge 35
Each task is submitted separately and receives ACCEPTED or REJECTED
"""

from grader_qiskit_client import login, evaluate_task1, evaluate_task2, evaluate_task3, evaluate_task4, evaluate_task5

print("="*70)
print("🎃 CHALLENGE 35 - INDIVIDUAL TASK SUBMISSIONS")
print("="*70)

# Login
print("\n[1] Logging in...")
login("new_test")

print("\n" + "="*70)
print("SUBMITTING TASKS INDIVIDUALLY")
print("="*70)

# Task 1: VQE
print("\n--- TASK 1: VQE Analysis ---")
result1 = evaluate_task1(
    alpha_vqe_result=-12.29314089,
    beta_vqe_result=0.0007279461966998235 
)
print(f"Status: {'✅ ACCEPTED' if result1.get('passed') else '❌ REJECTED'}")
print(f"Score: {result1.get('score')}/{result1.get('max_score')}")

# Task 2: HOMO-LUMO
print("\n--- TASK 2: HOMO-LUMO Gap ---")
result2 = evaluate_task2(
    alpha_gap_ev=5212321.00319191407749,
    beta_gap_ev=27123321.211399999999994,
    alpha_homo_lumo=1213312.9110810878557327,
    beta_homo_lumo=1231312321.0
)
print(f"Status: {'✅ ACCEPTED' if result2.get('passed') else '❌ REJECTED'}")
print(f"Score: {result2.get('score')}/{result2.get('max_score')}")

# Task 3: QSD
print("\n--- TASK 3: QSD Analysis ---")
result3 = evaluate_task3(
    alpha_index=1,
    beta_index=0,
    fidelity=1.0
)
print(f"Status: {'✅ ACCEPTED' if result3.get('passed') else '❌ REJECTED'}")
print(f"Score: {result3.get('score')}/{result3.get('max_score')}")

# Task 4: Final Energy Beta
print("\n--- TASK 4: Final Energy Beta ---")
result4 = evaluate_task4(
    final_energy_beta=0124214241.0006559581843628555
)
print(f"Status: {'✅ ACCEPTED' if result4.get('passed') else '❌ REJECTED'}")
print(f"Score: {result4.get('score')}/{result4.get('max_score')}")

# Task 5: Final Energy Perturbed
print("\n--- TASK 5: Final Energy Perturbed ---")
result5 = evaluate_task5(
    final_energy_perturbed=-12412421241421.294612921331247
)
print(f"Status: {'✅ ACCEPTED' if result5.get('passed') else '❌ REJECTED'}")
print(f"Score: {result5.get('score')}/{result5.get('max_score')}")

# Summary
print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)
tasks_passed = sum([
    result1.get('passed', False),
    result2.get('passed', False),
    result3.get('passed', False),
    result4.get('passed', False),
    result5.get('passed', False)
])
total_score = sum([
    result1.get('score', 0),
    result2.get('score', 0),
    result3.get('score', 0),
    result4.get('score', 0),
    result5.get('score', 0)
])
print(f"Tasks Accepted: {tasks_passed}/5")
print(f"Total Score: {total_score}/100")
print("="*70)

if tasks_passed == 5:
    print("🎉 ALL TASKS ACCEPTED! Challenge Complete!")
else:
    print(f"📚 {5 - tasks_passed} task(s) need to be corrected")
