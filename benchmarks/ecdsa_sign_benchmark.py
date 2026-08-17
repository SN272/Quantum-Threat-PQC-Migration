import time
import statistics

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

ITERATIONS = 500

message = b"Quantum-safe migration starts with understanding classical cryptography."

private_key = ec.generate_private_key(
    ec.SECP256R1()
)

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()

    private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )

    end = time.perf_counter()

    measurements.append(end - start)

print("ECDSA P-256 Signing Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))