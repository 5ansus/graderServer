"""
Example usage of the new lightweight system:
Users run code locally and only send the final results.
"""

from grader_qiskit_client import login, submit_results

# 1. Login
login('AliceQuantum', 'mypassword123')

# 2. User executes their code locally in the Halloween35.ipynb notebook
# and obtains the results

# 3. Send ONLY the results (no heavy code)
submit_results(
    35,
    alpha_vqe_result=-2.1847,
    beta_vqe_result=0.9375,
    alpha_gap_ev=33.57,
    beta_gap_ev=27.21,
    alpha_homo_lumo=1.234,
    beta_homo_lumo=1.0
)

