###############################################################################
from numpy import array, exp, sin, cos, pi, log


def e2(phi):
    return exp(1j * phi / 2)


def rotationGate(T, P):
    A = array([[
        e2(-P) * (cos(T / 2)**2 - 1j * sin(T / 2)**2),
        -e2(P) * (1 + 1j) * (sin(T / 2) * cos(T / 2))
    ], [
        e2(-P) * sin(T / 2) * cos(T / 2) * (1 - 1j),
        e2(P) * (cos(T / 2)**2 + 1j * sin(T / 2)**2)
    ]])

    return A


###############################################################################
if __name__ == '__main__':
    zero = array([1, 0])
    n = 3
    m = 1
    # T = 2*pi*n + ((pi / 2) + log(1 + sqrt(2))*1j)
    P = 2 * (2 * pi * m - 1j * log((1 + 1j) / 2))
    T = -pi / 2
    asdf = rotationGate(T, P).dot(zero)
    print(asdf)
    print(((1 - 1j) / 2) * e2(-P))
###############################################################################
