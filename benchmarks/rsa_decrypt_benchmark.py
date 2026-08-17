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

public_key = private_key.public_key()

message = b"Quantum-safe migration starts with understanding classical cryptography"

ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

measurements = []

for _ in range(ITERATIONS):
    start = time.perf_counter()

    private_key.decrypt(
        ciphertext,
        padding=padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    end = time.perf_counter()

    measurements.append(end - start)

print("RSA-", KEY_SIZE, "Decryption Benchmark")
print("Iterations:", ITERATIONS)
print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Minimum:", min(measurements))
print("Standard Deviation:", statistics.stdev(measurements))