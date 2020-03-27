###############################################################################
from numpy import array, sqrt
from pyquil import get_qc
from pyquil import Program
from pyquil.gates import H, X  # MEASURE  # Z
from gates import sqrtGate, makeControlGate, makeCCGate
from qiskit.tools.visualization import plot_histogram  # plot_state,
# from pyquil.latex.latex_generation import to_latex
###############################################################################
mapping = {
    'x': array([[0, 1], [1, 0]], dtype=complex),
    'z': array([[1, 0], [0, -1]], dtype=complex)
}


###############################################################################
class Grover_noAncilla(object):
    def __init__(self, target, trials):

        self.index = target
        self.n = len(self.index)
        self.trials = trials
        self.p = Program()

        # self.ro = self.p.declare('ro', 'BIT', self.n)

        for i in range(self.n):
            self.p += H(i)

        self.p += X(self.n)

    def nToffoli(self, controls, target, gate, gate_index, inverse=False):
        nctl = len(controls)

        if nctl == 0:
            self.p += gate(target)
            return
        if nctl == 1:
            name = "c_sqrt_{0}_{1}_end".format(inverse, gate_index)
            defin, constr = makeControlGate(gate, name)
            if name not in [gate.name for gate in self.p.defined_gates]:
                self.p += defin
            self.p += constr(controls[0], target)
            return
        if nctl == 2:
            name = "cc_sqrt_{0}_{1}_end".format(inverse, gate_index)
            defin, constr = makeCCGate(gate, name)
            if name not in [gate.name for gate in self.p.defined_gates]:
                self.p += defin
            self.p += constr(controls[0], controls[1], target)
            return

        # create the sqrt gate numpy arrays
        sqrt, sqrtT = sqrtGate(gate)

        # use the numpy arrays to create the custom pyquil gates
        # for those numpy matrices
        """These are the control gates"""
        sqrt_name = "c_sqrt_{0}_{1}".format('normal', gate_index)
        sqrtT_name = "c_sqrt_{0}_{1}".format('inverse', gate_index)
        sqrgate_def, sqtgate_constr = makeControlGate(sqrt, sqrt_name)
        sqrgateT_def, sqtgateT_constr = makeControlGate(sqrtT, sqrtT_name)

        # add the created gate definitions to the quantum program
        if sqrt_name not in [gate.name for gate in self.p.defined_gates]:
            self.p += sqrgate_def
        if sqrtT_name not in [gate.name for gate in self.p.defined_gates]:
            self.p += sqrgateT_def

        # Break the gate down
        self.nToffoli(controls[:-1], controls[-1], gate, gate_index + 1)
        self.p += sqtgateT_constr(controls[-1], target)
        self.nToffoli(controls[:-1], controls[-1], gate, gate_index + 1)
        self.p += sqtgate_constr(controls[-1], target)
        self.nToffoli(controls[:-1], target, sqrt, gate_index + 1)

    def oracle(self):
        for i in range(self.n):
            if int(self.index[i]) == 0:
                self.p += X(i)
        # n-bit Toffoli gate with target bit being an extra target bit
        self.nToffoli(
            controls=[i for i in range(self.n - 1)],
            target=self.n - 1,
            gate=mapping['z'],
            gate_index=0)

        # hit the target bit with a Z gate to complete the phase kickback
        # self.p += Z(self.n)

        # "un-compute" the nToffoli

        # self.nToffoli(
        # controls=[i for i in range(self.n)],
        # target=self.n,
        # gate=mapping['x'],
        #     gate_index=0)

        for i in range(self.n):
            if int(self.index[i]) == 0:
                self.p += X(i)

    def diffusion(self):
        for i in range(self.n):
            self.p += H(i)
            self.p += X(i)

        self.nToffoli(
            controls=[i for i in range(self.n - 1)],
            target=self.n - 1,
            gate=mapping['z'],
            gate_index=0)

        for i in range(self.n):
            self.p += X(i)
            self.p += H(i)

    def run(self):
        """How many times to run an iteration"""
        m = int(sqrt(self.n))

        for _ in range(m):
            self.oracle()
            self.diffusion()

        qc = get_qc('{}q-qvm'.format(str(self.n + 1)))
        # qc = get_qc('9q-generic-qvm')
        result = qc.run_and_measure(self.p, trials=self.trials)
        m = len(result[0])
        for bit in result:
            print(result[bit])
        counts = {}
        for i in range(m):
            index_str = "{0}{1}{2}".format(result[0][i], result[1][i],
                                           result[2][i])
            if index_str not in counts:
                counts[index_str] = 1
            else:
                counts[index_str] += 1
        print(counts)
        plot_histogram(counts)
        # latex_string = to_latex(self.p)
        # with open('circuit.tex', 'w') as f:
        #     print(latex_string, file=f)
        # for i in range(self.n):
        # self.p += MEASURE(i, self.ro[i])
        # exe = qc.compile(self.p)
        # result = qc.run(exe)
        # print(result)


###############################################################################
if __name__ == '__main__':
    grover = Grover_noAncilla('111', trials=20)
    grover.run()
###############################################################################
