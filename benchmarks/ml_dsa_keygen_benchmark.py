import time
import statistics

from cryptography.hazmat.primitives.asymmetric import mldsa

ITERATIONS = 500

measurements =[]

for _ in range(ITERATIONS):
    start = time.perf_counter()
    private_key = mldsa.MLDSA65PrivateKey.generate()
    public_key = private_key.public_key()
    end = time.perf_counter()
    measurements.append(end-start)

print("ML-DSA-65 Key Generation Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))