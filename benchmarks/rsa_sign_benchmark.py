import time
import statistics

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

KEY_SIZE = 2048
ITERATIONS = 500

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=KEY_SIZE
)

message = b"Quantum-safe migration starts with understanding classical cryptography"

measurements =[]

for _ in range(ITERATIONS):
    start = time.perf_counter()

    private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    end = time.perf_counter()

    measurements.append(end-start)

print("RSA: ", KEY_SIZE, "Signing benchmark")
print("Iterations:", ITERATIONS)
print("Mean: ", statistics.mean(measurements))
print("Median: ", statistics.median(measurements))
print("Minimum: ", min(measurements))
print("Standard deviations: ", statistics.stdev(measurements))