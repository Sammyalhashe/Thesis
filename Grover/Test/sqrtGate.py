"""
This file contains code to build continuously "square-rooted" gates.
For the moment, it merely does only matrix algebra, without yet being able to
construct explicit gates.

I try to implement what Craig Gidney output in his blog post to implement
n-bit control gates without using any ancilla. In that paper he details how
to construct square-root gates. My job is to then try to be able to then
construct physically realizeable quantum gates made using the gates already
available to me in qiskit.

I am also using the resource https://arxiv.org/pdf/quant-ph/9503016.pdf, which
details how to construct n-bit toffoli gates from elementary gates.
"""
###############################################################################

import numpy
from numpy import array, sqrt, dot
from scipy.linalg import eig
from prettyPrintMatrix import matprint
from filterMat import filterNpdArray

from qiskit.mapper import euler_angles_1q
# from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

###############################################################################
mapping = {'x': array([[0, 1], [1, 0]], dtype=complex)}

MS = array(
    [[1, 0, 0, 0 - 1j], [0, 1, 0 - 1j, 0], [0, 0 - 1j, 1, 0],
     [0 - 1j, 0, 0, 1]],
    dtype=complex)

###############################################################################


def Ry(theta):
    pass


###############################################################################
def innerProd(vec1, vec2):
    """Ry

    :param theta:
    """
    """innerProd

    :param vec1:
    :param vec2:
    """
    vec2 = vec2.conj()
    s = vec1.shape
    n = len(s)
    final_arr = []
    if n == 1:
        n1 = s[0]
        for i in range(n1):
            val = vec1[i]
            row = []
            for j in range(n1):
                row.append(val * vec2[j])
            final_arr.append(row)
        return array(final_arr)
    else:
        raise ValueError


###############################################################################
def sqrtGate(gate='x'):
    """sqrtGate

    :param gate:
    """
    if isinstance(gate, str):
        mat = mapping[gate]
        a = eig(mat)
    if isinstance(gate, numpy.ndarray):
        a = eig(gate)
    val1, val2 = a[0][0], a[0][1]
    vec1, vec2 = a[1][0], a[1][1]
    re1 = sqrt(val1) * innerProd(vec1, vec1)
    re2 = sqrt(val2) * innerProd(vec2, vec2)
    result = re1 + re2
    print(euler_angles_1q(result))
    return filterNpdArray(result), filterNpdArray(result.conj().T)


###############################################################################

if __name__ == '__main__':
    sx, _ = sqrtGate()
    print('sx: ')
    matprint(sx)

    ssx, ssxt = sqrtGate(gate=sx)
    print('ssx: ')
    matprint(ssx)

    sssx, _ = sqrtGate(gate=ssx)
    print('sssx: ')
    matprint(sssx)

    print('dot: ')
    matprint(filterNpdArray(dot(sx, sx.conj().T)))

    # sMS, _ = sqrtGate(MS)
    # print('sMS: ')
    # matprint(sMS)

    # ssMS, _ = sqrtGate(sMS)
    # print('ssMS: ')
    # matprint(ssMS)

    # sssMS, sssMSt = sqrtGate(ssMS)
    # print('sssMS: ')
    # matprint(sssMS)
    # matprint(dot(sssMS, sssMSt.conj().T))
