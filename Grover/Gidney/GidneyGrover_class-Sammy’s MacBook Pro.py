from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, compile  # available_backends
from qiskit.tools.visualization import plot_histogram  # plot_state,
from qiskit import Aer, IBMQ
from qiskit.backends.jobstatus import JOB_FINAL_STATES
# import Qconfig
from qiskit.tools.visualization import circuit_drawer  # plot_state_qsphere
# from matplotlib import pyplot as plt
# import numpy as np
# from scipy import linalg as la
from math import sqrt
import time

import sys
if sys.version_info < (3, 5):
    raise Exception('Run with python >3.5')

# oracle definition

# number of bits denoting the index of the index
index = '101'

# load acccount
IBMQ.load_accounts()
print(IBMQ.backends())


class Grover(object):
    def __init__(self, index):
        self.index = index
        self.n = len(self.index)
        if not self.n >= 2:
            raise ValueError
        # Create a Quantum Register with 2 qubits.
        # control quibits
        self.q = QuantumRegister(self.n, 'q')
        # ancillary qubits
        self.anc = QuantumRegister(self.n - 1, 'anc')
        # control for control z-gate in oracle
        # target qubits for oracle (for debugging)
        self.tar = QuantumRegister(1, 'tar')
        # ancillary qubits for diffusion gate
        self.ancD = QuantumRegister(1, 'ancD') if self.n <= 2 else \
            QuantumRegister(self.n - 2, 'ancD')
        # target qubits for diffusion gate
        self.tarD = QuantumRegister(1, 'tarD')
        # Create a Classical Register for oracle measurements.
        # cOracle = ClassicalRegister(1, 'cOracle')
        # registers for measurement of the qubits
        self.c = ClassicalRegister(self.n, 'c')
        # Create a Quantum Circuit
        self.qc = QuantumCircuit(self.q, self.anc, self.tar, self.ancD,
                                 self.tarD, self.c)

        # # set input for testing
        # for i in range(n):
        #     v = int(index[i])
        #     if v != 0:
        #         qc.x(q[i])

        # apply hadamard gates
        for i in range(self.n):
            self.qc.h(self.q[i])

        self.qc.x(self.tar[0])

    #################################################
    """ORACLE IMPLEMENTATION
    """

    def oracle1(self):
        """oracle1"""
        # applying control-NOT gates forward
        for i in range(self.n):
            v = int(self.index[i])
            if i == 0:
                v2 = int(self.index[i + 1])
                if v2 == 0:
                    self.qc.x(self.q[i + 1])
                if v == 0:
                    self.qc.x(self.q[i])
                    self.qc.ccx(self.q[i], self.q[i + 1], self.anc[i])
                    # qc.x(q[i])
                else:
                    self.qc.ccx(self.q[i], self.q[i + 1], self.anc[i])
            elif i == 1:
                pass

            else:
                if v == 0:
                    self.qc.x(self.q[i])
                    self.qc.ccx(self.q[i], self.anc[i - 2], self.anc[i - 1])
                    # qc.x(q[i])
                else:
                    self.qc.ccx(self.q[i], self.anc[i - 2], self.anc[i - 1])
        self.qc.cx(self.anc[self.n - 2], self.tar[0])
        self.qc.z(self.tar[0])

        self.qc.cx(self.anc[self.n - 2], self.tar[0])
        # applying control-NOT gates backwards -> reset
        for i in range(self.n - 1, -1, -1):
            v = int(self.index[i])
            if i == 0:
                v2 = int(self.index[i + 1])
                # if v2 == 0:
                #     qc.x(q[i + 1])
                if v == 0:
                    # qc.x(q[i])
                    self.qc.ccx(self.q[i], self.q[i + 1], self.anc[i])
                    self.qc.x(self.q[i])
                else:
                    self.qc.ccx(self.q[i], self.q[i + 1], self.anc[i])
                if v2 == 0:
                    self.qc.x(self.q[i + 1])
            elif i == 1:
                pass

            else:
                if v == 0:
                    # qc.x(q[i])
                    self.qc.ccx(self.q[i], self.anc[i - 2], self.anc[i - 1])
                    self.qc.x(self.q[i])
                else:
                    self.qc.ccx(self.q[i], self.anc[i - 2], self.anc[i - 1])

    def toffoli_n_unborrowed(self, qubits, borrowed, target):
        """toffoli_n

        :param qubits: list of indexes for global qubits
        There are n-qubits and n-2 borrowed bits
        :param borrowed: list of indexes for the borrowed bits
        :param target: index of the target qubit
        """
        if isinstance(target, int):
            target_bit = self.q[target]
        else:
            target_bit = target

        if len(qubits) <= 2:
            self.qc.ccx(
                self.q[qubits[0]]
                if isinstance(qubits[0], int) else qubits[0], self.q[qubits[1]]
                if isinstance(qubits[1], int) else qubits[1], target_bit)
        else:
            m = len(qubits) - 2 - 1
            self.qc.ccx(
                self.q[qubits[m + 2]] if isinstance(qubits[m + 2], int) else
                qubits[m + 2], self.q[borrowed[m]]
                if isinstance(borrowed[m], int) else borrowed[m], target_bit)
            # first forward pass
            for i in range(m - 1, -1, -1):
                if i == 0:
                    print(qubits[i])
                    self.qc.ccx(
                        self.q[qubits[i]] if isinstance(qubits[i], int) else
                        qubits[i], self.q[qubits[i + 1]] if isinstance(
                            qubits[i + 1],
                            int) else qubits[i + 1], self.q[borrowed[i]])
                else:
                    self.qc.ccx(
                        self.q[qubits[i + 2]] if isinstance(
                            qubits[i + 2],
                            int) else qubits[i + 2], self.q[borrowed[i]]
                        if isinstance(borrowed[i], int) else borrowed[i],
                        self.q[borrowed[i + 1]] if isinstance(
                            borrowed[i + 1], int) else borrowed[i + 1])
            # first backwards pass
            for i in range(1, m - 1):
                self.qc.ccx(
                    self.q[borrowed[i]]
                    if isinstance(borrowed[i],
                                  int) else borrowed[i], self.q[qubits[i + 2]]
                    if isinstance(qubits[i + 2], int) else qubits[i + 2],
                    self.q[borrowed[i + 1]]
                    if isinstance(borrowed[i + 1], int) else borrowed[i + 1])

            # second forward pass
            self.qc.ccx(
                self.q[qubits[m + 2]] if isinstance(qubits[m + 2], int) else
                qubits[m + 2], self.q[borrowed[m]]
                if isinstance(borrowed[m], int) else borrowed[m], target_bit)
            for i in range(m - 1, -1, -1):
                if i == 0:
                    self.qc.ccx(
                        self.q[qubits[i]] if isinstance(qubits[i], int) else
                        qubits[i], self.q[qubits[i + 1]] if isinstance(
                            qubits[i + 1],
                            int) else qubits[i + 1], self.q[borrowed[i]]
                        if isinstance(borrowed[i], int) else borrowed[i])
                else:
                    self.qc.ccx(
                        self.q[qubits[i + 2]] if isinstance(
                            qubits[i + 2],
                            int) else qubits[i + 2], self.q[borrowed[i]]
                        if isinstance(borrowed[i], int) else borrowed[i],
                        self.q[borrowed[i + 1]] if isinstance(
                            borrowed[i + 1], int) else borrowed[i + 1])

            # second backwards pass
            for i in range(1, m - 1):
                self.qc.ccx(
                    self.q[borrowed[i]]
                    if isinstance(borrowed[i],
                                  int) else borrowed[i], self.q[qubits[i + 2]]
                    if isinstance(qubits[i + 2], int) else qubits[i + 2],
                    self.q[borrowed[i + 1]]
                    if isinstance(borrowed[i + 1], int) else borrowed[i + 1])

    def oracle2(self):
        """
        Recursive Definition:
        - Using Borrowed bits to first break down into sequnetial controls
        that use every other bit
        - break them down until they reach 4-controls
        - break the 4-control toffolis into double bit toffolis
        """
        n = self.n
        first = []
        second = []
        counter = 0
        # for the indices that are zero, make sure to first NOT them
        # need to undo this not later
        # prepare the array of indices that hold the two divisions of indices
        for i in range(n):
            if counter % 2 == 0:
                first.append(i)
            else:
                second.append(i)
            v = int(self.index[i])
            if v == 0:
                self.qc.x(self.q[i])
            counter += 1

        second.append(self.anc[0])

        print(first)
        print(second)

        for i in range(2):  # necessary for uncomputation
            self.toffoli_n_unborrowed(first, second[:-1], self.anc[0])
            self.toffoli_n_unborrowed(second, first, self.tar[0])
        self.qc.z(self.tar[0])
        for i in range(2):  # necessary for uncomputation
            self.toffoli_n_unborrowed(first, second[:-1], self.anc[0])
            self.toffoli_n_unborrowed(second, first, self.tar[0])
        for i in range(n):
            v = int(self.index[i])
            if v == 0:
                self.qc.x(self.q[i])

    #################################################
    """GROVER-DIFFUSION GATE IMPLEMENTAION
    """

    def diffusion_gate(self):
        """diffusion_gate"""
        # apply hadamard gates
        for i in range(self.n):
            self.qc.h(self.q[i])

        # apply pauli-X gates
        for i in range(self.n):
            self.qc.x(self.q[i])

        self.qc.barrier()
        """Apply multi-qubit control-pauli-Z gate
        """
        if self.n > 2:
            for i in range(self.n - 1):
                if i == 0:
                    self.qc.ccx(self.q[i], self.q[i + 1], self.ancD[i])
                elif i == 1:
                    pass
                else:
                    self.qc.ccx(self.q[i], self.ancD[i - 2], self.ancD[i - 1])
            self.qc.cz(self.ancD[self.n - 3], self.q[self.n - 1])

            for i in range(self.n - 2, -1, -1):
                if i == 0:
                    self.qc.ccx(self.q[i], self.q[i + 1], self.ancD[i])
                elif i == 1:
                    pass
                else:
                    # print('i: ', i)
                    # print('q: ', len(self.q))
                    # print('ancD: ', len(self.ancD))
                    self.qc.ccx(self.q[i], self.ancD[i - 2], self.ancD[i - 1])
        else:
            # if n == 2, only need to control-z the first with the second
            self.qc.cx(self.q[0], self.ancD[0])
            self.qc.cz(self.ancD[0], self.q[1])
            self.qc.cx(self.q[0], self.ancD[0])

        self.qc.barrier()

        # apply pauli-X gates
        for i in range(self.n):
            self.qc.x(self.q[i])

        # apply hadamard gates
        for i in range(self.n):
            self.qc.h(self.q[i])

    def construct(self):
        """construct"""
        #################################################
        """Grover implementation repeating oracle + diffusion
        """
        N = int(sqrt(self.n))

        for i in range(N):
            self.oracle1()
            self.qc.barrier()
            self.diffusion_gate()
            self.qc.barrier()
        #################################################
        """Measurement of quibits
        """

        for i in range(self.n):
            self.qc.measure(self.q[i], self.c[i])

        #################################################
        circuit_drawer(self.qc, filename='./Pictures/gidney3_class.png')

    def construct_N(self, N):
        """construct_N"""
        #################################################
        """Grover implementation repeating oracle + diffusion for N iterations
        """
        for i in range(N):
            self.oracle1()
            self.diffusion_gate()
        #################################################
        """Measurement of quibits
        """

        for i in range(self.n):
            self.qc.measure(self.q[i], self.c[i])

        #################################################
        # circuit_drawer(self.qc, filename='./Pictures/gidney3_class.png')

    def run_sim(self):
        """run_sim"""
        # See a list of available local simulators
        # print("Local backends: ", Aer.available_backends())

        # compile and run the Quantum circuit on a simulator backend
        backend_sim = Aer.get_backend('qasm_simulator')
        job_sim = execute(self.qc, backend_sim)
        result_sim = job_sim.result()
        # Show the results
        print("simulation: ", result_sim)
        counts = result_sim.get_counts(self.qc)
        # state = result_sim.get_statevector(self.qc)
        # plot_state_qsphere(state).savefig('bloch.png')
        return counts
        # The commented below doesn't seem to work
        # state = result_sim.get_statevector(self.qc)
        # plot_state(state)
        # plot_histogram(counts)

    def run(self, be):
        """run

        :param be: Quantum Processor Chosen to use available
        """
        backend = IBMQ.get_backend(name=be)
        qobj = compile(self.qc, backend, shots=2000)
        job = backend.run(qobj)
        start_time = time.time()
        job_status = job.status()
        while job_status not in JOB_FINAL_STATES:
            print(
                f'Status @ {time.time()-start_time:0.0f} s: {job_status.name},'
                f' est. queue position: {job.queue_position()}')
            time.sleep(10)
            job_status = job.status()

        result = job.result()
        counts = result.get_counts()
        # get_data() contains time to run the application
        print(result.get_data())
        print(counts)
        return counts


if __name__ == '__main__':
    # start = time.time()
    grover = Grover(index)
    grover.construct()
    # counts = grover.run_sim()
    # counts = grover.run('ibmqx4')
    counts = grover.run('ibmq_16_melbourne')
    counts_l = [(i, counts[i]) for i in counts.keys()]
    print('Sim: ', sorted(counts_l, key=lambda x: x[1], reverse=True)[:5])
    # counts_l = [(i, counts[i]) for i in counts.keys()]
    # print('Proc: ', sorted(counts_l, key=lambda x: x[1], reverse=True)[:5])
    # end = time.time()
    # print('Time to construct and simulate: ', end - start)
    plot_histogram(counts)
