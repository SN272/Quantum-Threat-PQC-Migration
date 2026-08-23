from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)

# Equal superposition
qc.h(0)
qc.h(1)

# Oracle for target |10>
qc.x(1)
qc.cz(0,1)
qc.x(1)

# Diffusion operator
qc.h(0)
qc.h(1)

qc.x(0)
qc.x(1)

qc.h(1)
qc.cx(0,1)
qc.h(1)

qc.x(0)
qc.x(1)

qc.h(0)
qc.h(1)

# Measure
qc.measure_all()

print(qc.draw())

# Simulate
simulator = AerSimulator()
result = simulator.run(
    qc,
    shots = 1000
).result()


counts = result.get_counts()
total_shots = sum(counts.values())


print("\nProbabilities:")
for state, count in counts.items():
    probability = count/total_shots
    print(f"{state}: {probability:.3f}")
