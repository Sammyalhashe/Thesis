"""
This file contains code to filter out noisy values in numpy arrays
"""

from numpy import absolute, zeros


###############################################################################
def filterNpdArray(mat):
    x, y = mat.shape
    threshold = 1e-12
    newmat = zeros((x, y), dtype=complex)
    for i in range(x):
        for j in range(y):
            if absolute(mat[i, j]) <= threshold:
                newmat[i, j] = 0
            else:
                newmat[i, j] = mat[i, j]
    return newmat


###############################################################################
