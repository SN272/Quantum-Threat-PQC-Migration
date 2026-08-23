import time
import statistics

from cryptography.hazmat.primitives.asymmetric import mldsa

ITERATIONS = 500

private_key = mldsa.MLDSA65PrivateKey.generate()

message = b"Post-quantum migration benchmark message"

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()
    signature = private_key.sign(message)
    end = time.perf_counter()

    measurements.append(end-start)

print("ML-DSA-65 Signing Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))