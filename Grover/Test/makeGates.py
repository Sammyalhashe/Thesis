"""
This file contains the code that attempts to build the physically realiseable
gates from the matrices defined in the matrices.py file. (Also, more abstract
matrices like the MS gate and sqaure-root gates)
"""
###############################################################################

from qiskit.mapper import euler_angles_1q, two_qubit_kak
from numpy import array, dot
from sqrtGate import sqrtGate
from prettyPrintMatrix import matprint
from filterMat import filterNpdArray


###############################################################################
def createMapping(qc):
    return {
        'u3': {
            'gate': qc.u3,
            'args': 3,
            'ctl': 0,
            'argpos': [0, 1, 2]
        },
        'u2': {
            'gate': qc.u2,
            'args': 2,
            'ctl': 0,
            'argpos': [1, 2]
        },
        'u1': {
            'gate': qc.u1,
            'args': 1,
            'ctl': 0,
            'argpos': [2]
        },
        'id': {
            'gate': qc.iden,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        'x': {
            'gate': qc.x,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        'y': {
            'gate': qc.y,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        'z': {
            'gate': qc.z,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        'h': {
            'gate': qc.h,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        's': {
            'gate': qc.s,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        'st': {
            'gate': qc.sdg,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        't': {
            'gate': qc.t,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        'tt': {
            'gate': qc.tdg,
            'args': 0,
            'ctl': 0,
            'argpos': []
        },
        'rx': {
            'gate': qc.rx,
            'args': 1,
            'ctl': 0,
            'argpos': [0]
        },
        'ry': {
            'gate': qc.ry,
            'args': 1,
            'ctl': 0,
            'argpos': [0]
        },
        'rz': {
            'gate': qc.rz,
            'args': 1,
            'ctl': 0,
            'argpos': [1]
        },
        'cx': {
            'gate': qc.cx,
            'args': 0,
            'ctl': 1,
            'argpos': []
        },
        'cy': {
            'gate': qc.cy,
            'args': 0,
            'ctl': 1,
            'argpos': []
        },
        'cz': {
            'gate': qc.cz,
            'args': 0,
            'ctl': 1,
            'argpos': []
        },
        'ch': {
            'gate': qc.ch,
            'args': 0,
            'ctl': 1,
            'argpos': []
        },
        'crz': {
            'gate': qc.crz,
            'args': 1,
            'ctl': 1,
            'argpos': [2]
        },
        'cu1': {
            'gate': qc.cu1,
            'args': 1,
            'ctl': 1,
            'argpos': [2]
        },
        'cu3': {
            'gate': qc.cu3,
            'args': 3,
            'ctl': 1,
            'argpos': [0, 1, 2]
        },
        'swap': {
            'gate': qc.swap,
            'args': 0,
            'ctl': 1,
            'argpos': []
        },
        'ccx': {
            'gate': qc.ccx,
            'args': 0,
            'ctl': 2,
            'argpos': []
        },
        'cswap': {
            'gate': qc.cswap,
            'args': 0,
            'ctl': 2,
            'argpos': []
        }
    }


###############################################################################
def makeGatesFrom2DMatrix(qc, q, mat):
    """makeGatesFrom2DMatrix

    :param qc: QuantumCircuit to apply the gate to
    :param q: qubit to apply the gate to
    :param mat: unitary matrix (2D)
    """
    theta, phi, lmbda, s = euler_angles_1q(mat)
    qc.rz(phi, q)
    qc.ry(theta, q)
    qc.rz(lmbda, q)


# use the mapping above to make the gates from the instructions returned
# from two_qubit_kak()
def makeGatesFrom4DMatrix(qc, qubits, mat):
    """makeGatesFrom4DMatrix

    :param qc: QuantumCircuit to apply the gate to
    :param qubits: qubits this gate acts on (2 qubits in an array)
    :param mat: unitary matrix (4D)
    """
    q1 = qubits[0]
    q2 = qubits[1]
    mat = filterNpdArray(mat)
    print('mat: ')
    test = filterNpdArray(dot(mat, mat.conj().T))
    matprint(test)
    MS_gate = two_qubit_kak(mat)
    mp = createMapping(qc)
    n = len(MS_gate)
    for i in range(n):
        gate = MS_gate[i]['name']
        qubits_direction = MS_gate[i]['args']
        params = MS_gate[i]['params']

        # grabs the gate (function) from mapping
        qiskit_gate = mp[gate]['gate']
        num_args = mp[gate]['args']
        argpos = mp[gate]['argpos']
        # num_ctl = mp[gate]['ctl']

        paramsf = []
        # print(params)
        if num_args != 0:
            for index in argpos:
                print(index)
                paramsf.append(params[index])

        qubits_inorder = []
        print(gate)
        for j in range(len(qubits_direction)):
            if qubits_direction[j] == 1:
                qubits_inorder.append(q2)
            else:
                qubits_inorder.append(q1)
        # implements the gate
        qiskit_gate(*paramsf, *qubits_inorder)


###############################################################################
def makeControlGate(qc, qubits, mat2D):
    u00 = mat2D[0][0]
    u01 = mat2D[0][1]
    u10 = mat2D[1][0]
    u11 = mat2D[1][1]
    cgatemat = array([[1, 0, 0, 0], [0, u00, 0, u01], [0, 0, 1, 0],
                      [0, u10, 0, u11]])
    makeGatesFrom4DMatrix(qc, qubits, cgatemat)


###############################################################################
def nCGATE(qc, qubits, gate):
    """nCGATE

    :param qc: QuantumCircuit to apply this gate to
    :param qubits: qubits to act on. This must be a list, with the last
    element being the target qubit and all other elements being the cotrol
    qubits.
    """
    # print('matrix: ', gate)
    n = len(qubits)
    if n == 0:
        return
    if n == 1:
        makeGatesFrom2DMatrix(qc, qubits[0], gate)
        return
    if n == 2:
        makeControlGate(qc, qubits, gate)
        return
    sq, sqt = sqrtGate(gate)
    nCGATE(qc, qubits[:-1], gate)
    nCGATE(qc, qubits[-2:], sqt)
    nCGATE(qc, qubits[:-1], gate)
    nCGATE(qc, qubits[-2:], sq)
    nCGATE(qc, qubits[:-2] + qubits[-1], sq)


###############################################################################
