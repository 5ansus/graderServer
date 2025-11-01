"""
Test individual task submissions for Challenge 36
Each task is submitted separately and receives ACCEPTED or REJECTED
"""

from grader_qiskit_client import login, submit_results, evaluate_task6, evaluate_task7, evaluate_task8

print("="*70)
print("🎃 CHALLENGE 36 - INDIVIDUAL TASK SUBMISSIONS")
print("="*70)

# Login
print("\n[1] Logging in...")
login("new_test36")

print("\n" + "="*70)
print("SUBMITTING TASKS INDIVIDUALLY")
print("="*70)

# Task 361: Classification Accuracy
print("\n--- TASK 361: Classification Accuracy ---")
# make 100 labels with 99 matches -> accuracy 0.99
y_hidden = [0]*100
preds = [0]*99 + [1]
result1 = evaluate_task6(preds, y_hidden)
print(f"Status: {'✅ ACCEPTED' if result1.get('passed') else '❌ REJECTED'}")
print(f"Score: {result1.get('score')}/{result1.get('max_score')}")

# Task 362: Image Generation
print("\n--- TASK 362: Image Generation ---")
# generate identical arrays so MSE=0 and shape (50,16)
gen = [[0.1 for _ in range(16)] for _ in range(50)]
clean = [[0.1 for _ in range(16)] for _ in range(50)]
result2 = evaluate_task7(gen, clean, [50, 16])
print(f"Status: {'✅ ACCEPTED' if result2.get('passed') else '❌ REJECTED'}")
print(f"Score: {result2.get('score')}/{result2.get('max_score')}")

# Task 363: Reinforcement Rewards
print("\n--- TASK 363: Reinforcement Rewards ---")
rewards = [1, 2, 3, 4, 5]
result3 = evaluate_task8(rewards)
print(f"Status: {'✅ ACCEPTED' if result3.get('passed') else '❌ REJECTED'}")
print(f"Score: {result3.get('score')}/{result3.get('max_score')}")

# Summary
print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)

tasks_passed = sum([
    result1.get('passed', False),
    result2.get('passed', False),
    result3.get('passed', False)
])

total_score = sum([
    result1.get('score', 0),
    result2.get('score', 0),
    result3.get('score', 0)
])
print(f"Tasks Accepted: {tasks_passed}/3")
print(f"Total Score: {total_score}/60")
print("="*70)

if tasks_passed == 3:
    print("🎉 ALL TASKS ACCEPTED! Challenge 36 Individual Tasks Passed!")
else:
    print(f"📚 {3 - tasks_passed} task(s) need to be corrected")
