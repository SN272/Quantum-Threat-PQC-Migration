import time
import statistics

from cryptography.hazmat.primitives.asymmetric import mlkem

ITERATIONS = 500

private_key = mlkem.MLKEM768PrivateKey.generate()
public_key = private_key.public_key()

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()
    shared_secret, ciphertext = public_key.encapsulate()
    end = time.perf_counter()

    measurements.append(end-start)

print("ML-KEM-768 Encapsulation Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))