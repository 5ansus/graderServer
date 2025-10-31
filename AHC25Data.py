# AHC25Data.py
# MadQFF'25: Halloween Carol 2025 - Official Molecular Data & aux methods
# Challenge made by Enrique Anguiano-Vara
# ================================================
# DO NOT CHANGE THIS FILE

import numpy as np
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_algorithms.eigensolvers import NumPyEigensolver
import matplotlib.pyplot as plt


######################### HAMILTONIANS ####################################

def get_alpha_hamiltonian():
    pauli_strings_A = [
        'IIII',
        'IIIZ', 'IIZI', 'IZII', 'ZIII',
        'IIZZ', 'IZZI', 'ZZII', 'IZIZ', 'ZIZI', 'ZZZI', 'ZZZZ',
        'IXXI', 'IYYI', 'XXII', 'YYII', 'XXXX', 'YYYY',
        'IXIY', 'IYIX', 'XYXY', 'YXYX',
        'XZXZ', 'YZYZ', 'XZYZ', 'YXZX',
        'IXZI', 'IYZI', 'IZXI', 'IZYI',
        'XZYI', 'YZXI', 'XYZI', 'YXZI',
        'IZZZ', 'ZIZZ', 'ZZIZ', 'ZZZI',
        'XIXI', 'YIYI', 'ZIXI', 'ZIYI',
        'XIYZ', 'YIXZ', 'ZXIY', 'ZYIX',
        'XXYY', 'YYXX', 'XZZY', 'YZXZ'
    ]

    coefficients_A = [
        -2.1847, 1.2451, -0.8923, 0.7134, -0.6245,
        -1.8934, 1.4567, -1.2789, -1.5432, -1.3456, 0.9876, 0.2157,
        0.8234, 0.7345, 0.4567, 0.3789, 0.1892, 0.0945,
        0.6547, 0.5438, -0.7629, 0.8341,
        0.9712, -0.8563, 0.4729, -0.3641,
        0.7281, 0.6392, -0.5483, 0.4574,
        0.3865, -0.2956, 0.8147, -0.7258,
        0.6419, -0.5370, 0.4281, 0.3192,
        0.9583, -0.8674, 0.7765, -0.6856,
        0.5947, 0.4038, -0.3129, 0.2210,
        0.8492, -0.7583, 0.6674, -0.5765
    ]
    
    return SparsePauliOp(pauli_strings_A, coefficients_A)


def get_beta_hamiltonian():
    return SparsePauliOp([
        'IIII',
        'IIIX', 'IIIY', 'IIIZ', 'IIXI', 'IIXX', 'IIXY', 'IIXZ',
        'IIYI', 'IIYX', 'IIYY', 'IIYZ', 'IIZI', 'IIZX', 'IIZY', 'IIZZ', 
        'IXII', 'IXIX', 'IXIY', 'IXIZ', 'IXXI', 'IXXX', 'IXXY', 'IXXZ', 
        'IXYI', 'IXYX', 'IXYY', 'IXYZ', 'IXZI', 'IXZX', 'IXZY', 'IXZZ', 
        'IYII', 'IYIX', 'IYIY', 'IYIZ', 'IYXI', 'IYXX', 'IYXY', 'IYXZ', 
        'IYYI', 'IYYX', 'IYYY', 'IYYZ', 'IYZI', 'IYZX', 'IYZY', 'IYZZ', 
        'IZII', 'IZIX', 'IZIY', 'IZIZ', 'IZXI', 'IZXX', 'IZXY', 'IZXZ', 
        'IZYI', 'IZYX', 'IZYY', 'IZYZ', 'IZZI', 'IZZX', 'IZZY', 'IZZZ', 
        'XIII', 'XIIX', 'XIIY', 'XIIZ', 'XIXI', 'XIXX', 'XIXY', 'XIXZ', 
        'XIYI', 'XIYX', 'XIYY', 'XIYZ', 'XIZI', 'XIZX', 'XIZY', 'XIZZ', 
        'XXII', 'XXIX', 'XXIY', 'XXIZ', 'XXXI', 'XXXX', 'XXXY', 'XXXZ', 
        'XXYI', 'XXYX', 'XXYY', 'XXYZ', 'XXZI', 'XXZX', 'XXZY', 'XXZZ', 
        'XYII', 'XYIX', 'XYIY', 'XYIZ', 'XYXI', 'XYXX', 'XYXY', 'XYXZ', 
        'XYYI', 'XYYX', 'XYYY', 'XYYZ', 'XYZI', 'XYZX', 'XYZY', 'XYZZ', 
        'XZII', 'XZIX', 'XZIY', 'XZIZ', 'XZXI', 'XZXX', 'XZXY', 'XZXZ', 
        'XZYI', 'XZYX', 'XZYY', 'XZYZ', 'XZZI', 'XZZX', 'XZZY', 'XZZZ', 
        'YIII', 'YIIX', 'YIIY', 'YIIZ', 'YIXI', 'YIXX', 'YIXY', 'YIXZ', 
        'YIYI', 'YIYX', 'YIYY', 'YIYZ', 'YIZI', 'YIZX', 'YIZY', 'YIZZ', 
        'YXII', 'YXIX', 'YXIY', 'YXIZ', 'YXXI', 'YXXX', 'YXXY', 'YXXZ', 
        'YXYI', 'YXYX', 'YXYY', 'YXYZ', 'YXZI', 'YXZX', 'YXZY', 'YXZZ', 
        'YYII', 'YYIX', 'YYIY', 'YYIZ', 'YYXI', 'YYXX', 'YYXY', 'YYXZ', 
        'YYYI', 'YYYX', 'YYYY', 'YYYZ', 'YYZI', 'YYZX', 'YYZY', 'YYZZ', 
        'YZII', 'YZIX', 'YZIY', 'YZIZ', 'YZXI', 'YZXX', 'YZXY', 'YZXZ', 
        'YZYI', 'YZYX', 'YZYY', 'YZYZ', 'YZZI', 'YZZX', 'YZZY', 'YZZZ', 
        'ZIII', 'ZIIX', 'ZIIY', 'ZIIZ', 'ZIXI', 'ZIXX', 'ZIXY', 'ZIXZ', 
        'ZIYI', 'ZIYX', 'ZIYY', 'ZIYZ', 'ZIZI', 'ZIZX', 'ZIZY', 'ZIZZ', 
        'ZXII', 'ZXIX', 'ZXIY', 'ZXIZ', 'ZXXI', 'ZXXX', 'ZXXY', 'ZXXZ', 
        'ZXYI', 'ZXYX', 'ZXYY', 'ZXYZ', 'ZXZI', 'ZXZX', 'ZXZY', 'ZXZZ', 
        'ZYII', 'ZYIX', 'ZYIY', 'ZYIZ', 'ZYXI', 'ZYXX', 'ZYXY', 'ZYXZ', 
        'ZYYI', 'ZYYX', 'ZYYY', 'ZYYZ', 'ZYZI', 'ZYZX', 'ZYZY', 'ZYZZ', 
        'ZZII', 'ZZIX', 'ZZIY', 'ZZIZ', 'ZZXI', 'ZZXX', 'ZZXY', 'ZZXZ', 
        'ZZYI', 'ZZYX', 'ZZYY', 'ZZYZ', 'ZZZI', 'ZZZX', 'ZZZY', 'ZZZZ'], 
        [0.9375, -0.010720630186836649, -0.007688489947996393, -0.04579959825524122,
        0.005708536268553768, 0.009456185177851854, -0.003481059377495254,
        0.005395864172393348, -0.006752500902160423, -0.004152649388396435,
        -0.008360685888339225, -0.010605645228152988, -0.043528597945463404, 
        0.00022732306959296223, -0.008988865722571952, -0.05193706612483937, 
        0.014480825360255727, -0.003706664276011422, 0.003185395342731028, 
        0.020813751102231753, 0.01518609364836118, 0.0022043831381906008, 
        0.00029280104040912573, 0.01661003410492523, 0.012910768745394222, 
        0.0011022330156942165, 4.214555708008773e-05, 0.0022075556848692893, 
        0.020350681583949978, -0.0002898179057482242, 0.001817999672575286, 
        0.018301375823535648, 0.01850359599256015, 0.011171641437209714, 
        0.0029589976018439823, 0.012941626337723776, -0.012479119501619737, 
        0.0004504775309635435, 0.0019217650572198697, -0.003177690625024711, 
        0.01743281603530763, 0.0033943776839820724, -0.0009851518619498892, 
        0.0195769385196232, 0.008039057472016104, 0.0007991394570125137, 
        0.002155079150697221, 0.013462785833797031, 0.03875573165622567, 
        0.0013053552028407843, 0.011156941957570153, 0.043652299885582044, 
        -0.009884151847835058, -0.004908549372058623, 0.010930348093257847, 
        -0.007639788619828511, 0.00543450660422448, 0.012456196316318115, 
        0.0031292325571785737, 0.0024658394520949323, 0.05066584622350721, 
        0.005695267004848275, 0.009384496880501756, 0.03886017172249298, 
        -0.0025310440672254783, 0.0018770854327623161, -0.017252157374242627, 
        -0.0026781700893154592, 0.0009798364631826732, 0.002287589408042427, 
        0.013095299449204723, 0.001334045613338187, 0.004447869596771954, 
        0.00964158996144411, -0.0008751529816651326, 0.004888883717380736, 
        -0.011105128355296175, -0.012634892668167308, -0.011018389599202915, 
        -0.003876646353327834, 0.009784711650545409, -0.0006362675849084813, 
        -0.000922045129941487, 0.006263803842372222, -0.011571928380537028, 
        -0.029035111362207308, 0.004206570778574621, -0.009374037516623943, 
        0.00019149413306222157, 0.00017507941682775208, 0.03209715818582216, 
        -0.004361780577598175, 0.003895860469968858, -0.007703575169026626, 
        0.0006903550351354408, 0.01074137051504298, 0.009550679819985943, 
        0.005213166438257704, 0.0019129333390875737, 0.014366916936558956, 
        -0.004519656276208423, -0.003792831188030263, -0.033114774689453785, 
        0.0018882326062155397, -0.010358946082357687, -0.02973402366714928, 
        0.005691903717304268, -0.008663796940337419, 0.018689291775474594, 
        0.014933506617082865, -0.0015416044321410192, 0.013178054268545208, 
        0.0012294811875130885, 0.008435450104129511, 0.013528679623252087, 
        -0.0015285914571935106, 0.002863949338869438, 0.012025447051376013, 
        -0.0053828970799310715, 0.0016567026257795132, -0.006871132568356792, 
        -0.00429401084054413, -0.010193872918794832, -0.008914093765561841, 
        -0.0012414457034053417, 2.078965330664772e-05, 0.020137589391888155, 
        -0.004906884475025247, -0.00025678370109682427, -0.017831428571917496, 
        -0.0009212235992612436, 0.0005045266342249169, 0.014185883631433718, 
        0.01518153977356888, -0.0013042966727380523, 0.008242229714571385, 
        -0.0031220104305239695, -0.0023609478291974195, -0.009579153388266749, 
        0.00022864606107414888, 0.00253546102766326, -0.010163675645222484, 
        0.010174679307185564, 0.0025192986543773957, -0.011568516740012953, 
        -0.002030961598768427, 9.20722236192285e-05, -0.016117080996356593, 
        0.0029488316643219593, 0.006807144635160973, 0.025003844478867252, 
        -0.005304961285630945, 0.00887371016806853, 0.029646515170072257, 
        0.0010773221062876865, 0.007465485551739347, -0.014915484707342734, 
        -0.0033783652891559396, 0.0043249399083109775, -0.010770226217622518, 
        0.010231315300564394, 0.0012493901491552803, -0.0046368943222457595, 
        0.006261308586499958, -0.014803338277260953, -0.037783570851223594, 
        0.0011949306044783691, -0.011587142039029838, 0.003066194071768875, 
        0.007036445764526384, 0.03189701646584385, -0.0028828898944728374, 
        0.0032997124460873955, -0.004803240258382419, -0.010080351060711548, 
        0.008563957826642458, 0.0020980889356884713, 0.013909539859300123, 
        -0.009394456581501922, 0.001242063955090991, -0.0035503605746020793, 
        -0.005380815427469224, -0.013763301210794384, -0.00028594252193529237, 
        -0.0015675476959194584, -0.009691011303209927, 0.0036151854851845734, 
        -0.004398080416039472, 0.0024559322123541417, 0.018827677342181978, 
        0.00030733631986854925, 0.002141727217171124, -0.043896286043319334, 
        -0.0012827080925667607, -0.00905993149841521, -0.05604329311295356, 
        0.0029234773811759496, 0.0021420569719508347, -0.010339219751946509, 
        0.005158579378981624, -0.01597781104335055, -0.014916818154945829, 
        -0.0041330550729886005, -0.008014492739762204, -0.050832902136312065, 
        -0.006335175949431225, -0.009311144711502828, -0.042610613180825305, 
        0.020064539935483492, 0.0020200746604051357, 0.0019104295380023035, 
        0.015045017680109608, 0.014878607390883192, 0.0006689337536037276, 
        0.003510522219594931, 0.013739355270361596, 0.002312635830673755, 
        -0.0030275929872108226, 0.0026185210351688764, 0.014330571071746467, 
        0.018124217420781175, 0.0016375690372463498, -0.004114287368053997, 
        0.02001553467175457, 0.01156719334380249, 0.0011581783952790622, 
        -0.0007264295353577298, 0.015934043279529034, -0.0019944401537961686, 
        0.0036708179370864053, 0.004350589494224769, -0.011915259216183896, 
        0.022438526785290597, 0.009523104841019784, 0.001766949234819556, 
        0.0192755449657082, 0.014162249702548473, 0.00292015411226541, 
        -0.0013798688368423409, 0.00907920610251678, 0.04896889424041321, 
        0.007784609239320036, 0.007632924565749148, 0.03989254256037074, 
        -0.008195258728270573, -0.008397963503111781, 0.003030046490805822, 
        -0.01226733051811199, 0.001514688883912653, 0.004081175289293036, 
        0.01166018099912895, 0.0007102359902153375, 0.04066631496130923, 
        0.0009739249537302065, 0.00910207762535543, 0.05252775449262141])


######################## AUX METHODS ###############################

# For reference
def get_alpha_exact_hamiltonian(): 
    return __exact_diagonalization(get_alpha_hamiltonian(), "ALPHA", 10)

def get_beta_exact_hamiltonian(): 
    return __exact_diagonalization(get_beta_hamiltonian(), "BETA", 10)

def __exact_diagonalization(hamiltonian, name, num_eigenvalues=5):
    solver = NumPyEigensolver(k=num_eigenvalues)
    result = solver.compute_eigenvalues(hamiltonian)
    
    eigenvalues = np.real(result.eigenvalues)
      
    return eigenvalues, result.eigenstates

alpha_exact_evals, alpha_exact_states = get_alpha_exact_hamiltonian()
beta_exact_evals, beta_exact_states = get_beta_exact_hamiltonian() 

#################################### PLOTS ##################################

def vqe_plot(alpha_vqe_tracker, beta_vqe_tracker): 
    # Visualize VQE convergence
    _, axes = plt.subplots(1, 2, figsize=(16, 5))

    # Alpha convergence
    axes[0].plot(alpha_vqe_tracker.energies, 'b-', linewidth=2, label='VQE Energy')
    axes[0].axhline(y=alpha_exact_evals[0], color='r', linestyle='--', linewidth=2, label='Exact Ground')
    axes[0].set_xlabel('Iteration', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Energy (Hartree)', fontsize=12, fontweight='bold')
    axes[0].set_title('Alpha VQE Convergence', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Beta convergence
    axes[1].plot(beta_vqe_tracker.energies, 'r-', linewidth=2, label='VQE Energy')
    axes[1].axhline(y=beta_exact_evals[0], color='b', linestyle='--', linewidth=2, label='Exact Ground')
    axes[1].set_xlabel('Iteration', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Energy (Hartree)', fontsize=12, fontweight='bold')
    axes[1].set_title('Beta VQE Convergence', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('vqe_convergence.png', dpi=300, bbox_inches='tight')
    plt.show()


def homolumo_plot(alpha_gap_ev, beta_gap_ev, alpha_homo_lumo, beta_homo_lumo): 
    print(f"\n📊 HOMO-LUMO Comparison:")
    print(f"   Alpha gap: {alpha_gap_ev:.4f} eV")
    print(f"   Beta gap:  {beta_gap_ev:.4f} eV")
    print(f"   Ratio (α/β): {alpha_homo_lumo/beta_homo_lumo:.4f}")

    if alpha_homo_lumo > beta_homo_lumo:
        print(f"\n   ✅ Beta is MORE REACTIVE than Alpha (smaller gap)")
        print(f"   → Beta has greater tendency to form chemical bonds")
    elif alpha_homo_lumo < beta_homo_lumo:
        print(f"\n   ✅ Alpha is MORE REACTIVE than Beta (smaller gap)")
        print(f"   → Alpha has greater tendency to form chemical bonds")
    else:
        print(f"\n   ⚖️ Both have similar reactivity")

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Alpha levels
    ax.hlines(alpha_exact_evals[0], 0.8, 1.2, colors='blue', linewidth=10, label='Alpha HOMO')
    ax.hlines(alpha_exact_evals[1], 0.8, 1.2, colors='lightblue', linewidth=10, 
            linestyle='--', label='Alpha LUMO')
    ax.annotate('', xy=(1.0, alpha_exact_evals[1]), xytext=(1.0, alpha_exact_evals[0]),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=3))
    ax.text(1.3, (alpha_exact_evals[0] + alpha_exact_evals[1])/2, 
            f'Δ={alpha_gap_ev:.2f} eV', fontsize=12, fontweight='bold')

    # Beta levels
    ax.hlines(beta_exact_evals[0], 1.8, 2.2, colors='red', linewidth=10, label='Beta HOMO')
    ax.hlines(beta_exact_evals[1], 1.8, 2.2, colors='lightcoral', linewidth=10, 
            linestyle='--', label='Beta LUMO')
    ax.annotate('', xy=(2.0, beta_exact_evals[1]), xytext=(2.0, beta_exact_evals[0]),
                arrowprops=dict(arrowstyle='<->', color='red', lw=3))
    ax.text(2.3, (beta_exact_evals[0] + beta_exact_evals[1])/2, 
            f'Δ={beta_gap_ev:.2f} eV', fontsize=12, fontweight='bold')

    ax.set_xlim(0.5, 2.5)
    ax.set_xticks([1.0, 2.0])
    ax.set_xticklabels(['Alpha', 'Beta'], fontsize=14, fontweight='bold')
    ax.set_ylabel('Energy (Hartree)', fontsize=12, fontweight='bold')
    ax.set_title('HOMO-LUMO Energy Diagram', fontsize=16, fontweight='bold')
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('homo_lumo_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()


def qsd_plot(n_states_to_compare, alpha_qsd_states, beta_qsd_states): 
    if n_states_to_compare < 2:
        print(f"\n   ⚠️ WARNING: Very small subspace ({n_states_to_compare} states)")
        print(f"   Not enough states for complete fidelity analysis")
        print(f"   This suggests Alpha has very collapsed structure")
        print(f"   Trying alternative method...")
        
        # Alternative: use full exact states
        print("\n   📐 Using direct analysis of full states (no projection):")
        
        fidelity_matrix = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                if isinstance(alpha_exact_states[i], Statevector):
                    psi_alpha = alpha_exact_states[i].data
                else:
                    psi_alpha = alpha_exact_states[i]
                
                if isinstance(beta_exact_states[j], Statevector):
                    psi_beta = beta_exact_states[j].data
                else:
                    psi_beta = beta_exact_states[j]
                
                fidelity = np.abs(np.vdot(psi_alpha, psi_beta))**2
                fidelity_matrix[i, j] = fidelity
        
        print(f"   ✅ Using full states in original Hilbert space")
        
    else:
        # Normal analysis with projected states
        print(f"\n   Comparing {n_states_to_compare} states in the subspace...")
        
        fidelity_matrix = np.zeros((n_states_to_compare, n_states_to_compare))
        for i in range(n_states_to_compare):
            for j in range(n_states_to_compare):
                psi_alpha = alpha_qsd_states[:, i]
                psi_beta = beta_qsd_states[:, j]
                fidelity = np.abs(np.vdot(psi_alpha, psi_beta))**2
                fidelity_matrix[i, j] = fidelity

    print(f"\n   Fidelity matrix (Alpha rows × Beta cols):")
    print("   " + "  ".join([f"β{j}" for j in range(fidelity_matrix.shape[1])]))
    for i in range(fidelity_matrix.shape[0]):
        row_str = f"α{i} " + "  ".join([f"{fidelity_matrix[i,j]:.3f}" for j in range(fidelity_matrix.shape[1])])
        print(f"   {row_str}")

    # Find best matches
    print(f"\n   🎯 Best matches (Fidelity > 0.5):")
    strong_matches = []
    for i in range(fidelity_matrix.shape[0]):
        for j in range(fidelity_matrix.shape[1]):
            F = fidelity_matrix[i, j]
            if F > 0.5:
                strong_matches.append((i, j, F))
                print(f"      α_{i} ↔ β_{j}: F = {F:.4f}")

    if len(strong_matches) == 0:
        print(f"      No strong matches found (all F < 0.5)")
        print(f"      This suggests Alpha and Beta have VERY different quantum structures")

    # Visualize fidelity matrix (adjusted to actual size)
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    im = ax.imshow(fidelity_matrix, cmap='hot', interpolation='nearest', vmin=0, vmax=1)
    ax.set_xlabel('Beta State Index', fontsize=12, fontweight='bold')
    ax.set_ylabel('Alpha State Index', fontsize=12, fontweight='bold')

    # Title adjusted based on method used
    if n_states_to_compare < 2:
        title_text = 'Fidelity Matrix: Alpha vs Beta States\n(Direct comparison - Full Hilbert space)'
    else:
        title_text = 'QSD Fidelity Matrix: Alpha vs Beta States\n(in Krylov subspace generated from Alpha)'

    ax.set_title(title_text, fontsize=14, fontweight='bold')
    ax.set_xticks(range(fidelity_matrix.shape[1]))
    ax.set_yticks(range(fidelity_matrix.shape[0]))
    ax.set_xticklabels([f'β{i}' for i in range(fidelity_matrix.shape[1])])
    ax.set_yticklabels([f'α{i}' for i in range(fidelity_matrix.shape[0])])

    # Annotate values
    for i in range(fidelity_matrix.shape[0]):
        for j in range(fidelity_matrix.shape[1]):
            text = ax.text(j, i, f'{fidelity_matrix[i, j]:.2f}',
                        ha="center", va="center", 
                        color="white" if fidelity_matrix[i, j] < 0.5 else "black",
                        fontsize=11, fontweight='bold')

    plt.colorbar(im, ax=ax, label='Fidelity')
    plt.tight_layout()
    plt.savefig('qsd_fidelity_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()


def varqite_plot(alpha_exact_evals, alpha_gs_vec, beta_exact_evals, beta_evolution_energies, beta_evolution_states):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Plot 1: Energy evolution
    axes[0, 0].plot(beta_evolution_energies, 'b-', linewidth=2, label='Beta Energy Evolution')
    axes[0, 0].axhline(y=beta_exact_evals[0], color='r', linestyle='--', linewidth=2, label='Beta Ground State')
    axes[0, 0].axhline(y=alpha_exact_evals[0], color='g', linestyle=':', linewidth=2, label='Alpha Ground State')
    axes[0, 0].set_xlabel('Time Step', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Energy (Hartree)', fontsize=12, fontweight='bold')
    axes[0, 0].set_title('VarQITE: Beta Energy Relaxation', fontsize=14, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Convergence (log scale)
    energy_diffs = np.abs(np.array(beta_evolution_energies) - beta_exact_evals[0])
    axes[0, 1].semilogy(energy_diffs, 'r-', linewidth=2)
    axes[0, 1].set_xlabel('Time Step', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('|E - E_ground| (log scale)', fontsize=12, fontweight='bold')
    axes[0, 1].set_title('Convergence to Ground State (log)', fontsize=14, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, which='both')

    # Plot 3: Temporal fidelity with Alpha
    fidelities_to_alpha = []
    for state in beta_evolution_states:
        state_sv = Statevector(state)
        fid = np.abs(state_sv.inner(alpha_gs_vec))**2
        fidelities_to_alpha.append(fid)

    axes[1, 0].plot(fidelities_to_alpha, 'purple', linewidth=2)
    axes[1, 0].set_xlabel('Time Step', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Fidelity with Alpha Ground State', fontsize=12, fontweight='bold')
    axes[1, 0].set_title('Beta → Alpha Convergence', fontsize=14, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_ylim([0, 1])

    # Plot 4: Final state comparison
    steps_to_show = [0, len(beta_evolution_states)//3, 2*len(beta_evolution_states)//3, -1]
    colors = ['red', 'orange', 'yellow', 'green']
    labels = ['Initial', 'Early', 'Mid', 'Final']

    for idx, (step, color, label) in enumerate(zip(steps_to_show, colors, labels)):
        state = beta_evolution_states[step]
        probs = np.abs(state)**2
        # Show first 16 elements for clarity
        axes[1, 1].bar(np.arange(min(16, len(probs))) + idx*0.2, probs[:16], 
                    width=0.2, alpha=0.7, color=color, label=label)

    axes[1, 1].set_xlabel('Basis State Index', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Probability', fontsize=12, fontweight='bold')
    axes[1, 1].set_title('State Vector Evolution (first 16 basis states)', fontsize=14, fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('varqite_evolution.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("\n" + "="*80)


def entanglement_entropy_plot(alpha_entropies, beta_entropies): 

    # Visualize
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    x = np.arange(len(alpha_entropies))
    ax.plot(x, alpha_entropies, 'bo-', linewidth=2, markersize=10, label='Alpha')
    ax.plot(x, beta_entropies, 'ro-', linewidth=2, markersize=10, label='Beta')
    ax.set_xlabel('State Index', fontsize=12, fontweight='bold')
    ax.set_ylabel('Entanglement Entropy (bits)', fontsize=12, fontweight='bold')
    ax.set_title('Entanglement Structure Comparison', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('entanglement_entropy.png', dpi=300, bbox_inches='tight')
    plt.show()


def final_plot(energies_perturbed, alpha_exact_evals): 

    # Visualize evolution
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Energy vs time
    axes[0].plot(energies_perturbed, 'b-', linewidth=2, label='Perturbed State')
    axes[0].axhline(y=alpha_exact_evals[0], color='r', linestyle='--', linewidth=2, label='α₀ (target)')
    axes[0].axhline(y=alpha_exact_evals[1], color='g', linestyle=':', linewidth=2, label='α₁ (initial)')
    axes[0].set_xlabel('Time Step', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Energy (Hartree)', fontsize=12, fontweight='bold')
    axes[0].set_title('VarQITE: Perturbed State Relaxation', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Convergence log
    energy_diffs_pert = np.abs(np.array(energies_perturbed) - alpha_exact_evals[0])
    axes[1].semilogy(energy_diffs_pert, 'r-', linewidth=2)
    axes[1].set_xlabel('Time Step', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('|E - E_ground| (log scale)', fontsize=12, fontweight='bold')
    axes[1].set_title('Convergence Rate', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('varqite_perturbed_test.png', dpi=300, bbox_inches='tight')
    plt.show()


def test_fidelity(fidelity_beta_to_alpha): 
    print(f"\n🎯 CONVERGENCE")
    print(f"   Fidelity Beta(final) → Alpha(ground): F = {fidelity_beta_to_alpha:.6f}")

    if fidelity_beta_to_alpha > 0.6:
        print(f"   ✅ Beta CONVERGES towards Alpha!")
    elif fidelity_beta_to_alpha > 0.5:
        print(f"   🔶 Partial convergence (moderate similarity)")
    elif fidelity_beta_to_alpha > 0.3:
        print(f"   ⚠️  Weak convergence")
    else:
        print(f"   ❌ Beta maintains different structure")