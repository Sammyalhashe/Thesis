"""
This code contains all the main gates in matrix form (not quantum gate objects)
"""
###############################################################################
from numpy import array, cos, sin, exp, pi


###############################################################################
def U(theta, phi, lmbda):
    return array([[cos(theta / 2), -exp(lmbda * 1j) * sin(theta / 2)], [
        exp(phi * 1j) * sin(theta / 2),
        exp((lmbda + phi) * 1j) * cos(theta / 2)
    ]])


###############################################################################


def u3(theta, phi, lmbda):
    return U(theta, phi, lmbda)


def u2(phi, lmbda):
    return u3(pi / 2, phi, lmbda)


def u1(lmbda):
    return u3(0, 0, lmbda)


###############################################################################

Identity = u3(0, 0, 0)

###############################################################################

X = u3(pi, 0, pi)

Y = u3(pi, pi / 2, pi / 2)

Z = u1(-pi)
###############################################################################

H = u2(0, pi)

S = u1(pi / 2)

S_t = u1(-pi / 2)

T = u1(pi / 4)

T_t = u1(-pi / 4)

###############################################################################


def Rx(theta):
    return u3(theta, -pi / 2, pi / 2)


def Ry(theta):
    return u3(theta, 0, 0)


def Rz(phi):
    return u1(phi)


###############################################################################


def build_control_gate(gate):
    u00 = gate[0][0]
    u01 = gate[0][1]
    u10 = gate[1][0]
    u11 = gate[1][1]

    return array([[1, 0, 0, 0], [0, u00, 0, u01], [0, 0, 1, 0],
                  [0, u10, 0, u11]])


###############################################################################
# not sure what to do with this yet. I'm trying to think of a way the
# instructions given by the 'two_qubit_kak()' function to a physical gate.
mapping = {}
###############################################################################
if __name__ == '__main__':
    print(build_control_gate(X))
