import sys
if sys.version_info < (3, 5):
    raise Exception('Run with python 3')

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import available_backends, execute
from qiskit.tools.visualization import plot_histogram, plot_state
from qiskit import IBMQ, Aer
import Qconfig
from qiskit.tools.visualization import circuit_drawer
from matplotlib import pyplot as plt
import numpy as np
from scipy import linalg as la


# oracle definition

# number of bits denoting the index of the index
index = '01101'

n = len(index)
if not n >= 2:
    raise ValueError
# Create a Quantum Register with 2 qubits.
# control quibits
q = QuantumRegister(n, 'q')
# ancillary qubits
anc = QuantumRegister(n - 1, 'anc')
# target qubits for oracle (for debuggin)
tar = QuantumRegister(1, 'tar')
# ancillary qubits for diffusion gate
d_anc = QuantumRegister(n-2, 'd_anc')
# target qubits for diffusion gate
tar_s = QuantumRegister(1, 'tar_s')
# Create a Classical Register for oracle measurements.
co = ClassicalRegister(1, 'co')
# registers for measurement of the qubits
c = ClassicalRegister(n, 'c')
# Create a Quantum Circuit
qc = QuantumCircuit(q, anc, tar, co, c, d_anc)

# set input for testing
for i in range(n):
    v = int(index[i])
    if v != 0:
        qc.x(q[i])


# apply hadamard gates
# for i in range(n):
#     qc.h(q[i])


#################################################
"""ORACLE IMPLEMENTATION
"""

# applying control-NOT gates
for i in range(n):
    v = int(index[i])
    print(v)
    if i == 0:
        v2 = int(index[i+1])
        if v2 == 0:
            qc.x(q[i + 1])
        if v == 0:
            qc.x(q[i])
            qc.ccx(q[i], q[i + 1], anc[i])
            qc.x(q[i])
        else:
            qc.ccx(q[i], q[i + 1], anc[i])
        if v2 == 0:
            qc.x(q[i + 1])
    elif i == 1:
        pass

    else:
        if v == 0:
            qc.x(q[i])
            qc.ccx(q[i], anc[i - 2], anc[i - 1])
            qc.x(q[i])
        else:
            qc.ccx(q[i], anc[i - 2], anc[i - 1])
qc.cx(anc[n - 2], tar[0])
qc.z(tar[0])
qc.measure(tar, co)

#################################################
"""GROVER-DIFFUSION GATE IMPLEMENTAION
"""

# apply hadamard gates
for i in range(n):
    qc.h(q[i])

# apply pauli-X gates
for i in range(n):
    qc.x(q[i])

# """Apply multi-qubit control-pauli-Z gate
# """
# for i in range(n - 1):
#     if i == 0:
#         qc.ccx(q[i], q[i + 1], anc[i])
#     elif i == 1:
#         pass
#     else:
#         qc.ccx(q[i], anc[i - 2], anc[i - 1])
# qc.cz(anc[-1], q[-1])


# apply pauli-X gates
for i in range(n):
    qc.x(q[i])

# apply hadamard gates
for i in range(n):
    qc.h(q[i])
#################################################

circuit_drawer(qc, filename='gidney.png')

# See a list of available local simulators
print("Local backends: ", Aer.available_backends())

# Compile and run the Quantum circuit on a simulator backend
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

# Show the results
print("simulation: ", result_sim)
print(result_sim.get_counts(qc))
