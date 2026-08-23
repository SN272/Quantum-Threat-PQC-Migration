import time
import statistics

from cryptography.hazmat.primitives.asymmetric import mlkem

ITERATIONS = 500

private_key = mlkem.MLKEM768PrivateKey.generate()
public_key = private_key.public_key()

_, ciphertext = public_key.encapsulate()

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()
    shared_secret = private_key.decapsulate(ciphertext)
    end = time.perf_counter()

    measurements.append(end-start)

print("ML-KEM-768 Decapsulation Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))