import csv
import time 
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

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
    #Warm-up
    for _ in range(WARMUP):
        function()

    #Recorded measurements
    for iteration in range(1, ITERATIONS+1):
        start = time.perf_counter()
        function()
        end = time.perf_counter()

        writer.writerow([
            algorithm,
            parameter,
            "Classical",
            operation,
            iteration,
            end - start
        ])

def generate_ecdsa_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_key.public_key()

private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

message = b"Quantum-safe migration benchmark message."

signature = private_key.sign(
    message,
    ec.ECDSA(hashes.SHA256())
)

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

    #Key generation
    record_operation(
        writer,
        "ECDSA",
        "P-256",
        "KeyGen",
        generate_ecdsa_keypair
    )

    #Signing
    record_operation(
        writer,
        "ECDSA",
        "P-256",
        "Signing",
        lambda: private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
    )

    #Verification
    record_operation(
        writer,
        "ECDSA",
        "P-256",
        "Verification",
        lambda:public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256())
        )
    )

print("ECDSA-P256 final benchmark complete")