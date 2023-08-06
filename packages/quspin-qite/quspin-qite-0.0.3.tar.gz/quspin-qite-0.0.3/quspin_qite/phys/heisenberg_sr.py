from quspin_qite.utils import * 
from quspin_qite.phys.physics_system import PhysicsSystem
import numpy as np  # generic math functions
from scipy import linalg as SciLA
from quspin.basis import spin_basis_1d  # Hilbert space spin basis
from quspin.operators import hamiltonian  # Hamiltonians and operators

class Heisenberg_SR(PhysicsSystem):
    """Heisenberg model with short range interactions.
    """
    
    def __init__(self, L, R):
        """Initialize the Heisenberg model with short range interactions.
        
        Args:
            L (int): The number of spins.
            R (float): The range of interactions.
        """
        super().__init__()
        basis = spin_basis_1d(L=L)
        H = []
        imax = L
        if L == 2:
            imax = L - 1
        for i in range(imax):
            j = (i + 1) % L
            active = [
                k for k in range(L) if dpbc(i, k, L) < R or dpbc(j, k, L) < R
            ]
            active = np.asarray(active)
            # -----
            static = [["xx", [[1, i, j]]], ["yy", [[1, i, j]]], ["zz", [[1, i, j]]]]
            ham = hamiltonian_s(static, [], dtype=np.complex128, basis=basis)
            H.append((active, ham))

        self._post_proc(H, L)
        