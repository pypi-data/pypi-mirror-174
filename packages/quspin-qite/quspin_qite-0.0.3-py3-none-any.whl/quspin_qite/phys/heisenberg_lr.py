from quspin_qite.utils import * 
from quspin_qite.phys.physics_system import PhysicsSystem
import numpy as np  # generic math functions
from scipy import linalg as SciLA
from quspin.basis import spin_basis_1d  # Hilbert space spin basis
from quspin.operators import hamiltonian  # Hamiltonians and operators

class Heisenberg_LR(PhysicsSystem):
    """Heisenberg model with long range interactions.
    """
    
    def __init__(self, L, R):
        """Initialize the Heisenberg model with long range interactions.
        
        Args:
            L (int): The number of spins.
            R (float): The range of interactions.
        """
        super().__init__()
        basis = spin_basis_1d(L=L)
        H = []
        for i in range(L):
            for j in range(i + 1, L):
                # -----
                active = [
                    k
                    for k in range(L)
                    if dobc(i, k, L) < R or dobc(j, k, L) < R
                ]
                active = np.asarray(active)
                # # -----
                h_alpha = 1.0 / (dobc(i, j, L) + 1.0)
                static = [
                    ["xx", [[h_alpha, i, j]]],
                    ["yy", [[h_alpha, i, j]]],
                    ["zz", [[h_alpha, i, j]]],
                ]
                ham = hamiltonian_s(static, [], dtype=np.complex128, basis=basis)
                H.append((active, ham))
        
                self._post_proc(H, L)