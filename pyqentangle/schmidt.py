from itertools import product

import numpy as np
from numpy.linalg import eig
from .bipartite_reddenmat_nocheck import bipartitepurestate_reduceddensitymatrix_nocheck
from .bipartite_denmat import bipartitepurestate_densitymatrix_cython


# total density matrix
def bipartitepurestate_densitymatrix(bipartitepurestate_tensor):
    """Calculate the whole density matrix of the bipartitite system

    Given a discrete normalized quantum system, given in terms of 2-D numpy array ``bipartitepurestate_tensor``,
    each element of ``bipartitepurestate_tensor[i, j]`` is the coefficient of the ket :math:`|ij\\rangle`,
    calculate the whole density matrix.

    :param bipartitepurestate_tensor: tensor describing the bi-partitite states, with each elements the coefficients for :math:`|ij\\rangle`
    :return: density matrix
    :type bipartitepurestate_tensor: numpy.ndarray
    :rtype: numpy.ndarray

    """
    return bipartitepurestate_densitymatrix_cython(bipartitepurestate_tensor)


def bipartitepurestate_reduceddensitymatrix(bipartitepurestate_tensor, kept):
    """Calculate the reduced density matrix for the specified subsystem

    Given a discrete normalized quantum system, given in terms of 2-D numpy array ``bipartitepurestate_tensor``,
    each element of ``bipartitepurestate_tensor[i, j]`` is the coefficient of the ket :math:`|ij\\rangle`,
    calculate the reduced density matrix of the specified subsystem.

    :param bipartitepurestate_tensor: tensor describing the bi-partitite states, with each elements the coefficients for :math:`|ij\\rangle`
    :param kept: subsystem, 0 indicating the first subsystem; 1 the second
    :return: reduced density matrix of the specified subsystem
    :type bipartitepurestate_tensor: numpy.ndarray
    :type kept: int
    :rtype: numpy.ndarray

    """
    if not (kept in [0, 1]):
        raise ValueError('kept can only be 0 or 1!')
    return bipartitepurestate_reduceddensitymatrix_nocheck(bipartitepurestate_tensor, kept)


# TODO: change here
def schmidt_decomposition(bipartitepurestate_tensor):
    """Calculate the Schmidt decomposition of the given discrete bipartite quantum system

    Given a discrete normalized quantum system, given in terms of 2-D numpy array ``bipartitepurestate_tensor``,
    each element of ``bipartitepurestate_tensor[i, j]`` is the coefficient of the ket :math:`|ij\\rangle`,
    calculate its Schmidt decomposition, returned as a list of tuples, where each tuple contains
    the Schmidt coefficient, the vector of eigenmode of first subsystem, and the vector of the eigenmode of
    second subsystem.

    :param bipartitepurestate_tensor: tensor describing the bi-partitite states, with each elements the coefficients for :math:`|ij\\rangle`
    :return: list of tuples containing the Schmidt coefficient, eigenmode for first subsystem, and eigenmode for second subsystem
    :type bipartitepurestate_tensor: numpy.ndarray
    :rtype: list

    """
    state_dims = bipartitepurestate_tensor.shape
    mindim = np.min(state_dims)

    rho1 = bipartitepurestate_reduceddensitymatrix(bipartitepurestate_tensor, 1)
    eigenvalues1, unitarymat1 = eig(rho1)
    coefmat0 = np.matmul(bipartitepurestate_tensor, unitarymat1)

    decomposition = [(float(np.real(eigenvalues1[k])),
                      coefmat0[:, k] / np.linalg.norm(coefmat0[:, k]),
                      unitarymat1[:, k])
                     for k in range(mindim)]
    decomposition = sorted(decomposition, key=lambda dec: dec[0], reverse=True)

    return decomposition
