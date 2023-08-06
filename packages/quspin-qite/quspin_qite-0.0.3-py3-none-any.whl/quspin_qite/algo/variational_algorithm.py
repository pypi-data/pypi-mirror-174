import numpy as np


class VariationalAlgorithm:
    # like QAOA is one of the VQA / VQE
    def __init__(self, physics_system, q):
        """initialization of the variational algorithms     
        """
        self.physics_system = physics_system
        self.q = q
        
        self._extract_physics_system() # extract the variables from the physics system

    def _extract_physics_system(self):
        """Extract the variables from the physics system.
        """
        self.h_list = self.physics_system.H_list
        self.L = self.physics_system.L
        self.n_term = self.physics_system.n_term
        
        self.psi_initial = self.physics_system.psi_initial
        self.psi_target = self.physics_system.psi_target
        self.psi_target_conjugate_transpose = self.psi_target.conjugate().transpose()


    @property
    def param_shape(self):
        """Return the shape of the parameters.
        """
        return (self.q, self.n_term, 4 ** len(self.h_list[0]))


    def _initial_x0(self):
        """Generate the initial guess of the parameters.
        """
        x0 = np.random.randn(*self.param_shape)
        return x0

    @property
    def initial_guess(self):
        """Generate the initial guess for the sovler
        """
        return self._initial_x0()
    
    def expected_energy(self, params):
        """Compute the expected energy of the evolved state.
        """
        u = self.evolve(params)
        return self._compute_expected_energy(u)

    def get_reward(self, params, reward_type='fidelity'):
        """Compute the reward of the evolved state.
        """
        if reward_type == 'fidelity':
            return self.fidelity(params)
        elif reward_type == 'energy':
            return - self.expected_energy(params)
        else:
            raise NotImplementedError("The reward type is not supported.")

    def _compute_fidelity(self, u):
        """Compute the fidelity between the target state and the evolved state.
        """
        return np.absolute(np.matmul(self.psi_target_conjugate_transpose, u)) ** 2

    # TODO: add the noise reward (maybe to the noise module, which is supposed to add more method to the class)
    @property
    def name(self):
        return self._name
    