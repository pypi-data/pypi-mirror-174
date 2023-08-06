import numpy as np
from sysflow.parallel.parallel import parallelize
from itertools import product
from functools import partial


from quspin.basis import spin_basis_1d
from quspin.operators import hamiltonian
import contextlib
import numpy as np
import os
import warnings
import wandb # noqa: E402

os.environ[
    "KMP_DUPLICATE_LIB_OK"
] = "True"  # uncomment this line if omp error occurs on OSX for python 3
os.environ["MKL_NUM_THREADS"] = "1"  # set number of MKL threads to run in parallel
os.environ["OMP_NUM_THREADS"] = "4"

warnings.filterwarnings("ignore")


import numpy as np
import contextlib
from quspin.operators import hamiltonian


def pass_print(str_s):
    print("\033[1;32m{}\033[0m".format(str_s))


def dobc(a, b, n):
    return np.abs(a - b)


def dpbc(a, b, n):
    return np.min([(a - b) % n, (b - a) % n])


def dgr(graph, i, j):
    VV, EE = graph
    nbit = len(VV)
    paths = []
    if i == j:
        return 0

    for (a, b) in EE:
        if i == a and j == b or i == b and j == a:
            return 1

    for (a, b) in EE:
        if i == a:
            paths.append([a, b])
        if i == b:
            paths.append([b, a])

    while True:
        new_paths = []
        for p in paths:
            end = p[len(p) - 1]
            for (a, b) in EE:
                if end == a:
                    if b == j:
                        return len(p)
                    else:
                        new_paths.append(p + [b])
                if end == b:
                    if a == j:
                        return len(p)
                    else:
                        new_paths.append(p + [a])
        paths = [x for x in new_paths]


def Bas2Int(x, b):
    nbit = len(x)
    z = [b ** (nbit - 1 - i) for i in range(nbit)]
    return np.dot(z, x)


def hamiltonian_s(*args, **kwargs):
    # silence the checking (otherwise the output is too verbose)
    with contextlib.redirect_stdout(None):
        return hamiltonian(*args, **kwargs)


import numpy as np
import time


def Int2Bas(n, b, nbit):
    if n == 0:
        return [0] * nbit
    x = []
    while n:
        x.append(int(n % b))
        n //= b
    return [0] * (nbit - len(x)) + x[::-1]


def Bas2Int(x, b):
    nbit = len(x)
    z = [b ** (nbit - 1 - i) for i in range(nbit)]
    return np.dot(z, x)


def Psi2Str(x):
    s = "|"
    for i in x:
        s += str(i)
    return s + ">"


def str_op(i):
    if i == 0:
        return "I"
    if i == 1:
        return "X"
    if i == 2:
        return "Y"
    if i == 3:
        return "Z"


def Opp2Str(x):
    s = ""
    for i in x:
        s += str_op(i)
    return s


def Lst2Str(x):
    s = ""
    for i in x:
        s += str(i)
    return s


def d12(t):
    return 1 if t % 3 > 0 else 0


d12f = np.vectorize(d12)


def d2(t):
    return 1 if t == 2 else 0


d2f = np.vectorize(d2)


def d23(t):
    return 1 if t > 1 else 0


d23f = np.vectorize(d23)


def computational_basis(nbit_):
    N = 2 ** nbit_
    for i in range(N):
        print(i, Psi2Str(Int2Bas(i, 2, nbit_)))


def pauli_basis(nbit_):
    M = 4 ** nbit_
    for i in range(M):
        print(i, Opp2Str(Int2Bas(i, 4, nbit_)))


# ---------------------------------------------------------- #


def pauli_action(active_, nbit_, verbose=False):
    nact = len(active_)
    N = 2 ** nbit_
    M = 4 ** nact

    dot = [2 ** (nbit_ - 1 - i) for i in range(nbit_)]
    ind_sx = np.zeros((M, N), dtype=int)
    gmm_sx = np.zeros((M, N), dtype=complex) + 1

    svec = np.zeros((M, nbit_), dtype=int)
    for mu in range(M):
        svec[mu, active_] = Int2Bas(mu, 4, nact)
    sxyvec = d12f(svec)
    nyvec = d2f(svec)
    syzvec = d23f(svec)
    nyvec = np.einsum("ab->a", nyvec)

    xvec = np.zeros((N, nbit_), dtype=int)
    for xi in range(N):
        xvec[xi, :] = np.asarray(Int2Bas(xi, 2, nbit_))

    gmm_sx = np.einsum("am,bm->ba", xvec, syzvec) + 0j
    gmm_sx[:, :] = (-1) ** gmm_sx[:, :]
    for mu in range(M):
        gmm_sx[mu, :] *= 1j ** nyvec[mu]
        yvec = (xvec[:, :] + sxyvec[mu, :]) % 2
        ind_sx[mu, :] = np.einsum("a,ba->b", dot, yvec)

    return ind_sx, gmm_sx


def print_state(psi_, nbit, outf):
    for i in range(psi_.shape[0]):
        if np.abs(psi_[i]) > 1e-4:
            for x in Int2Bas(i, 2, nbit):
                outf.write(str(x))
            outf.write(" %.12f %.12f I \n" % (np.real(psi_[i]), np.imag(psi_[i])))


def fidelity(psi_, phi_):
    return np.abs(np.vdot(psi_, phi_))


sigma_matrices = np.zeros((2, 2, 4), dtype=complex)
for i in range(2):
    j = (i + 1) % 2
    sigma_matrices[i, i, 0] = 1.0
    sigma_matrices[i, j, 1] = 1.0
    sigma_matrices[i, j, 2] = 1.0j * (-1.0) ** (i + 1.0)
    sigma_matrices[i, i, 3] = (-1.0) ** i


def matprint(mat, fmt="g"):
    # adapted from: https://gist.github.com/lbn/836313e283f5d47d2e4e
    col_maxes = [max([len(("{:" + fmt + "}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("\t{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
        print("")


def pass_print(str_s):
    print("\033[1;32m{}\033[0m".format(str_s))


def hamiltonian_s(*args, **kwargs):
    # silence the checking (otherwise the output is too verbose)
    with contextlib.redirect_stdout(None):
        return hamiltonian(*args, **kwargs)


# utils (which is not used)
def pauli2ind(pauli_str):
    for pauli, index in {"I": "0", "x": "1", "y": "2", "z": "3"}.items():
        pauli_str = pauli_str.replace(pauli, index)
    pauli_str = "".join(pauli_str)
    return int(pauli_str, len(pauli_list))


def dpbc(a, b, n):
    return np.min([(a - b) % n, (b - a) % n])


pauli_list = ["I", "x", "y", "z"]


def pauli_mat(pauli_str, active, N, basis=None, coo=False, transpose=False):
    """convert Pauli string to matrix

    Args:
        pauli_str (str): the pauli string description
        active (list[int]): active location
        N (int): number of qubit
        basis (quspin.basis, optional): quspin spin basis. Defaults to None.
        coo (bool, optional): if True, return COO matrix. Defaults to False.
        transpose (bool, optional): if True, return transpose of COO matrix. Defaults to False.
    """
    if basis is None:
        basis = spin_basis_1d(L=N)

    static = [[pauli_str, [[1, *active]]]]
    pauli_mat = hamiltonian_s(static, [], dtype=np.complex128, basis=basis)
    if coo:
        if transpose:
            ham_coo = pauli_mat.T.tocsr().tocoo()
        else:
            ham_coo = pauli_mat.tocsr().tocoo()
        return ham_coo.col, ham_coo.data
    else:
        # return pauli_mat.tocsc()
        return pauli_mat.toarray()


def pauli_action(active_, nbit_):
    """get all the active action in a matrix

    Args:
        active_ (list): the spin location of active qubit
        nbit_ (int): the total number of quspin spin

    Returns:
        ind_sx: the index of the non-zero element in the operator, shape (2**len(active), 2**nbit_)
            Note: ind_sx is transpose in order to match the matrix vector multiplication
        gmm_sx: the value of the non-zero element in the operator, shape (2**len(active), 2**nbit_)
    """
    nact = len(active_)
    opstr_list = list(product(pauli_list, repeat=nact))
    opstr_list = ["".join(opstr) for opstr in opstr_list]
    # from icecream import ic
    # ic([opstr_list[i] for i in [6, 9]])
    ret = parallelize(
        partial(
            pauli_mat, active=active_, N=nbit_, basis=None, coo=False, transpose=True
        ),
        opstr_list,
        backend="joblib",
    )
    return ret


# utils for the quantum state 
def overlap(psi1, psi2): 
    """compute the overlap between two quantum states

    TODO (jim): should we omit "**2" in the output? 

    Args:
        psi1 (np.ndarray): the first quantum state
        psi2 (np.ndarray): the second quantum state

    Returns:
        float: the overlap between two quantum states
    """
    return np.abs(np.vdot(psi1, psi2)) ** 2

# wandb utils 
def wandb_init(project): 
    """initialize wandb

    Args:
        project (str): the project name
    """
    wandb.init(project=project, settings=wandb.Settings(
                start_method="thread",
                _disable_stats=True,
                ),)

if __name__ == "__main__":
    ret = pauli_action(active_=[0, 2], nbit_=3)
