import time
import statistics

from cryptography.hazmat.primitives.asymmetric import ec

ITERATIONS = 500

alice_private_key = ec.generate_private_key(
    ec.SECP256R1()
)

alice_public_key = alice_private_key.public_key()

bob_private_key = ec.generate_private_key(
    ec.SECP256R1()
)

bob_public_key = bob_private_key.public_key()

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()

    alice_private_key.exchange(
        ec.ECDH(),
        bob_public_key
    )

    end = time.perf_counter()

    measurements.append(end-start)

print("ECDH P-256 Shared Secret Derivation Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))