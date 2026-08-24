from fractions import Fraction

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit_aer import AerSimulator

N = 15
A = 2

COUNTING_QUBITS = 4
WORK_QUBITS = 4

def multiplication_unitary(a,n):
    """Create the unitary U|x> = |a*x mod N> for x < N."""
    size = 2 ** n
    matrix = [[0j for _ in range(size)] for _ in range(size)]
    for x in range(size):
        if x<N:
            y = (a * x) % N
        else:
            y = x
        matrix[y][x] = 1.0
    return matrix

def build_shor_demo():
    counting = QuantumRegister(COUNTING_QUBITS, "count")
    work = QuantumRegister(WORK_QUBITS, "work")
    classical = ClassicalRegister(COUNTING_QUBITS, "meas")

    circuit = QuantumCircuit(counting, work, classical)

    #Prepare |x> in work register
    circuit.x(work[0])

    #Put counting registers in superposition
    for qubit in counting:
        circuit.h(qubit)

    #Controlled modular exponentiation
    base_unitary = UnitaryGate(
        multiplication_unitary(A, WORK_QUBITS),
        label="x2 mod 15"
    )

    for j in range(COUNTING_QUBITS):
        power = 2**j
        controlled_unitary = base_unitary.power(power).control()
        circuit.append(
            controlled_unitary,
            [counting[j]]+ list(work)
        )

    #Inverse QFT
    circuit.append(
        inverse_qft(COUNTING_QUBITS),
        counting
    )

    #Measure counting registers
    circuit.measure(counting, classical)

    return circuit

def inverse_qft(n):
    circuit = QuantumCircuit(n, name="QFT†")
    #Swap qubits
    for i in range(n//2):
        circuit.swap(i, n-i-1)

    #Inverse QFT
    for j in range(n):
        for m in range(j):
            circuit.cp(
                -3.141592653589793 / (2 ** (j - m)),
                m, j
            )
        circuit.h(j)
    return circuit.to_gate()

def estimate_order(counts):
    """Estimate the order r from the measured phase"""
    best_r = None
    for bitstring, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        value = int(bitstring, 2)
        if value==0:
            continue
        phase = Fraction(
            value,
            2** COUNTING_QUBITS
        )
        denominator = phase.limit_denominator(N)
        candidate_r = denominator.denominator
        if candidate_r >0 and candidate_r<N :
            if pow(A, candidate_r, N)==1:
                best_r = candidate_r
                break
    return best_r

def factor_from_order(r):
    if r is None or r % 2 != 0:
        return None

    x= pow(A, r//2, N)
    factor1 = __import__("math").gcd(x-1, N)
    factor2 = __import__("math").gcd(x+1, N)

    if factor1 in (1, N) or factor2 in (1,N):
        return None
    return factor1, factor2

#------------------------------DEMONSTRATION-----------------------------

circuit = build_shor_demo()
print("Shor's Algorithm - N=15 Demonstration")
print("Target number:", N)
print("Chosen base:", A)
print()
print("Quantum circuit:")
print(circuit.draw())

simulator = AerSimulator()

compiled = transpile(circuit, simulator)

result = simulator.run(
    compiled,
    shots=1024
).result()

counts = result.get_counts()

print()
print("Measurement results:")
print(counts)

r = estimate_order(counts)

print()
print("Estimated order r:", r)

factors = factor_from_order(r)

if factors:
    print("Factors found:", factors)
else:
    print("Factors were not recovered from this run.")