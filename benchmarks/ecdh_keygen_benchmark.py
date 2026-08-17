import time
import statistics

from cryptography.hazmat.primitives.asymmetric import ec

ITERATIONS = 500

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()

    private_key = ec.generate_private_key(
        ec.SECP256R1()
    )

    end = time.perf_counter()

    measurements.append(end - start)

print("ECDH P-256 Key Generation Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))