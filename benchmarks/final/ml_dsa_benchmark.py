import csv
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import mldsa


WARMUP = 100
ITERATIONS = 1500

OUTPUT = Path("data/raw/benchmark_results.csv")


def record_operation(
        writer,
        algorithm,
        parameter,
        operation,
        function
):
    # Warm-up
    for _ in range(WARMUP):
        function()

    # Recorded measurements
    for iteration in range(1, ITERATIONS + 1):

        start = time.perf_counter()

        function()

        end = time.perf_counter()

        writer.writerow([
            algorithm,
            parameter,
            "PQC",
            operation,
            iteration,
            end - start
        ])


def generate_mldsa_keypair():
    private_key = mldsa.MLDSA65PrivateKey.generate()
    private_key.public_key()

private_key = mldsa.MLDSA65PrivateKey.generate()
public_key = private_key.public_key()

message = b"Quantum-safe migration benchmark message."

signature = private_key.sign(message)


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

file_exists = OUTPUT.exists()

with open(OUTPUT, "a", newline="") as file:

    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "algorithm",
            "parameter",
            "category",
            "operation",
            "iteration",
            "time_seconds"
        ])

    # Key Generation
    record_operation(
        writer,
        "ML-DSA",
        "65",
        "KeyGen",
        generate_mldsa_keypair
    )

    # Signing
    record_operation(
        writer,
        "ML-DSA",
        "65",
        "Signing",
        lambda: private_key.sign(message)
    )

    # Verification
    record_operation(
        writer,
        "ML-DSA",
        "65",
        "Verification",
        lambda: public_key.verify(
            signature,
            message
        )
    )


print("ML-DSA-65 final benchmark complete.")