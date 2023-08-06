from quspin_qite.utils import * 
from quspin_qite.phys.physics_system import PhysicsSystem
import numpy as np  # generic math functions
from scipy import linalg as SciLA
from quspin.basis import spin_basis_1d  # Hilbert space spin basis
from quspin.operators import hamiltonian  # Hamiltonians and operators

class Ising(PhysicsSystem):
    """Ising model within some range.
    """
    
    def __init__(self, L, R, theta):
        """Initialize the Ising model within some range.
        
        Args:
            L (int): The number of spins.
            R (float): The range of interactions.
            theta (float): The angle for the coefficient parameters.
        """
        super().__init__()
        basis = spin_basis_1d(L=L)
        H = []
        for i in range(L):
            j = (i + 1) % L
            # -----
            active = [
                k for k in range(L) if dpbc(i, k, L) < R or dpbc(j, k, L) < R
            ]
            active = np.asarray(active)
            # -----
            static = [
                ["z", [[np.sin(theta) / 2.0, i]]],
                ["z", [[np.sin(theta) / 2.0, j]]],
                ["xx", [[np.cos(theta), i, j]]],
            ]
            ham = hamiltonian_s(static, [], dtype=np.complex128, basis=basis)
            H.append((active, ham))

        self._post_proc(H, L)
        