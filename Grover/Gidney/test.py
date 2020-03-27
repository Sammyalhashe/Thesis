from qiskit.tools.visualization import plot_histogram  # plot_state,

# counts = {
# "0x3": 261,
# "0x2": 247,
# "0x1": 254,
# "0x0": 301,
# "0x7": 223,
# "0x6": 232,
# "0x5": 222,
# "0x4": 260
# }

counts = {"01": 2000, "00": 0, "10": 0, "11": 0}

plot_histogram(counts)
