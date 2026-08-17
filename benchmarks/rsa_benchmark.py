import time
import statistics

from cryptography.hazmat.primitives.asymmetric import rsa

KEY_SIZE = 2048
ITERATIONS = 30

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()

    rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE
    )

    end = time.perf_counter()

    measurements.append(end - start)

print("Measurements: ", measurements)
print("Mean: ", statistics.mean(measurements))
print("Median: ", statistics.median(measurements))
print("Minimum", min(measurements))
print("Standard Deviation: ", statistics.stdev(measurements))
