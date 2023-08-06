from quspin_qite.utils import * 
from quspin_qite.phys.physics_system import PhysicsSystem
import numpy as np  # generic math functions
from scipy import linalg as SciLA
from quspin.basis import spin_basis_1d  # Hilbert space spin basis
from quspin.operators import hamiltonian  # Hamiltonians and operators

class Maxcut(PhysicsSystem):
    """Maxcut model within some range.
    """
    
    def __init__(self, graph, R):
        """Initialize the Maxcut model within some range.
        
        Args:
            graph (list): The graph of the Maxcut model.
            R (float): The range of interactions.
        """
        super().__init__()
        VV, EE = graph
        L = len(VV)
        basis = spin_basis_1d(L=L)
        H = []
        for (i, j) in EE:
            # -----
            active = [
                k for k in range(L) if dgr(graph, i, k) < R or dgr(graph, j, k) < R
            ]
            active = np.asarray(active)
            # -----
            static = [["I", [[-0.5, i]]], ["zz", [[0.5, i, j]]]]
            ham = hamiltonian_s(static, [], dtype=np.complex128, basis=basis)
            H.append((active, ham))
            # -----

        self._post_proc(H, L)
