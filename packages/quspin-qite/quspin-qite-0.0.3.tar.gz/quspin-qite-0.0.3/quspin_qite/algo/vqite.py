from quspin_qite.algo.variational_algorithm import VariationalAlgorithm
import numpy as np
import wandb

from quspin_qite.utils import pauli_action
import numpy as np
from scipy import linalg as SciLA



class vQITE(VariationalAlgorithm):
    """Variational QITE ansatz
    
    Use the QITE ansatz to solve the optimization problem. Here, the ansatz is the complete;
    As opposed to the compact ansatz, which is a low rank approximation the complete ansatz.
    
    Note that there is no low rank approximation here!
    """

    def __init__(self, physics_system, q):
        """Initialize the Variational-QITE ansatz.
        Args:
            physics_system (PhysicsSystem): the physics system.
            q (int): the number of qubits.
            ham_pool_length (int): the length of the hamiltonian pool.
            pauli_site (int): the numbers of the sites the pauli operator acts on.
        """
        super().__init__(physics_system, q)
        self._name = 'v-QITE'

    
    def _evolve_one_step(self, psi, h_list, a_list):
        """Evolve the system with the given parameters.
        Args:
            params (np.ndarray): the parameters of the variational ansatz.
            h_list (list): the list of the hamiltonians.
            a_list (list): the list of the coefficients.
        """
        active_array, h_glob = h_list
        pauli_list = pauli_action(active_=active_array, nbit_=self.L)

        Hamiltonian_A = 0
        for _ in range(len(a_list)):
            Hamiltonian_A = Hamiltonian_A + a_list[_] * pauli_list[_]
        
        psi_out = SciLA.expm(-1j * Hamiltonian_A).dot(psi)

        return psi_out

    def evolve(self, params):
        """Evolve the system with the given parameters.
        Args:
            variational_ansatz (tuple): the ordering of the hamiltonians
            params (np.ndarray): the parameters of the variational ansatz.
        """
        u = np.copy(self.psi_initial)

        # reshape the params to the correct shape
        a_vec = np.reshape(params, self.param_shape)
        for i in range(self.q):
            for h_index in range(self.n_term): 
                a_list = a_vec[i, h_index]  
                u = self._evolve_one_step(u, self.h_list[h_index], a_list)
        return u

    def fidelity(self, params):
        """Compute the fidelity between the target state and the evolved state.
        """
        u = self.evolve(params)
        wandb.log({'fidelity': self._compute_fidelity(u)})
        return self._compute_fidelity(u)

