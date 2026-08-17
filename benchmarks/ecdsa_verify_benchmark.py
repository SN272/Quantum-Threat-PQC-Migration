import time
import  statistics

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

ITERATIONS = 500

private_key = ec.generate_private_key(
    ec.SECP256R1()
)

public_key = private_key.public_key()

messsage = b"Quantum-safe migration starts with understanding classical cryptography."

signature = private_key.sign(
    messsage,
    ec.ECDSA(hashes.SHA256())
)

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()

    public_key.verify(
        signature,
        messsage,
        ec.ECDSA(hashes.SHA256())
    )

    end = time.perf_counter()

    measurements.append(end-start)

print("ECDSA P-256 Verification Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))