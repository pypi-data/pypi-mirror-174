from quspin_qite.algo.variational_algorithm import VariationalAlgorithm
from numpy import linalg as LA
import numpy as np
import wandb

from quspin_qite.utils import pauli_action
import numpy as np
from scipy import linalg as SciLA



class QITE(VariationalAlgorithm):
    """Variational QITE ansatz
    
    Use the QITE ansatz to solve the optimization problem. Here, the ansatz is the complete;
    As opposed to the compact ansatz, which is a low rank approximation the complete ansatz.
    
    Note that there is no low rank approximation here!
    """

    def __init__(self, physics_system, q, delta_t):
        """Initialize the Variational-QITE ansatz.
        Args:
            physics_system (PhysicsSystem): the physics system.
            q (int): the number of qubits.
            ham_pool_length (int): the length of the hamiltonian pool.
            delta_t (float): the time step.
        """
        super().__init__(physics_system, q)
        self._name = 'QITE'
        self.delta_t = delta_t # the time step

    
    def _evolve_one_step(self, psi, h_list):
        """Evolve the system with the given parameters.
        Args:
            params (np.ndarray): the parameters of the variational ansatz.
            psi (np.ndarray): the quantum state.
            h_list (list): the list of the hamiltonians.
        """
        delta_t = self.delta_t
        active_array, h_glob = h_list
        h_glob = h_glob.toarray()

        c = 1 - 2 * delta_t * np.conj(psi).dot(h_glob).dot(psi)

        pauli_list = pauli_action(active_=active_array, nbit_=self.L)

        S = np.array(
            [
                [np.conj(psi).dot(p1).dot(p0).dot(psi) for p0 in pauli_list]
                for p1 in pauli_list
            ]
        ).real
        b_p = np.array(
            [
                1 / delta_t * (1 / np.sqrt(c) - 1) * np.conj(psi).dot(p1).dot(psi)
                - 1 / np.sqrt(c) * np.conj(psi).dot(p1).dot(h_glob).dot(psi)
                for p1 in pauli_list
            ]
        )
        b = (1j * np.conj(b_p) - 1j * b_p).real

        a_list = LA.lstsq(S + np.transpose(S), -b, rcond=-1)[0]
        a_list = delta_t * a_list 
        
        Hamiltonian_A = 0
        for _ in range(len(a_list)):
            Hamiltonian_A = Hamiltonian_A + a_list[_] * pauli_list[_]
        
        psi_out = SciLA.expm(-1j * Hamiltonian_A).dot(psi)

        return psi_out, a_list

    def evolve(self):
        """Evolve the system with the given parameters.
        Args:
            variational_ansatz (tuple): the ordering of the hamiltonians
            params (np.ndarray): the parameters of the variational ansatz.
        """
        u = np.copy(self.psi_initial)

        a_vec_list = []
        for i in range(self.q):
            a_vec = []
            for h_index in range(self.n_term):   
                u, a_list = self._evolve_one_step(u, self.h_list[h_index])
                a_vec.append(a_list)
            a_vec_list.append(np.array(a_vec)) # (n_term, 4**L)
        a_vec = np.array(a_vec_list) # (q, n_term, 4**L)
        
        self.a_vec = a_vec 
        return u

    def fidelity(self):
        """Compute the fidelity between the target state and the evolved state.
        """
        u = self.evolve()
        wandb.log({'fidelity': self._compute_fidelity(u)})
        return self._compute_fidelity(u)


    
    @property
    def params(self): 
        # retrive the params from solving the qite
        return self.a_vec