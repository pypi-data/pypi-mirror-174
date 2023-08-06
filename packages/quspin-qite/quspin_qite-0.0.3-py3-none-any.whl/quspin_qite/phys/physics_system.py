import numpy as np
from scipy import linalg as SciLA
from quspin_qite.utils import overlap

class PhysicsSystem:
    def __init__(self):
        """intialization"""
        pass

    def _post_proc(self, H, L):
        """Post-processing of the wavefunction.
        """
        self.H_target = sum([h[1] for h in H]).toarray()
        self.E_GS, self.psi_target = SciLA.eigh(self.H_target)[0][0], SciLA.eigh(self.H_target)[1][:, 0]
        
        # AFM initial state
        self.psi_initial = np.zeros(2 ** L, dtype=complex)
        xvec = [0, 1] * (L // 2)
        xind = int("".join([str(x) for x in xvec]), 2)
        self.psi_initial[xind] = 1.0
        
        self._H_list = H
        self._L = L # number of spins

    

    @property
    def H_list(self):
        """Get the Hamiltonian list."""
        return self._H_list

    @property
    def hamiltonian(self):
        """Get the target Hamiltonian."""
        return self.H_target
    
    @property
    def ground_state_energy(self):
        """Get the ground state energy."""
        return self.E_GS
    
    @property
    def initial_state(self):
        """Get the initial state."""
        return self.psi_initial
    
    @property
    def target_state(self):
        """Get the target state."""
        return self.psi_target
    
    @property
    def init_tar_overlap(self):
        """Get the overlap between the initial and target states."""
        return overlap(self.psi_intial, self.psi_target)
    
    @property
    def L(self):
        """Get the number of spins."""
        return self._L
    
    @property
    def n_term(self):
        """Get the number of terms in the Hamiltonian."""
        return len(self.H_list)
    