import pyquil
from pyquil import get_qc

qc = get_qc('4q-qvm')
print(pyquil.__version__)
print(qc.compiler.get_version_info())
print(qc.qam.get_version_info())
