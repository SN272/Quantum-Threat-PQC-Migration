import csv
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import ec

WARMUP = 100
ITERATIONS = 1500

OUTPUT = Path("data/raw/benchmark_results.csv")

def record_operation(writer, algorithm, parameter, operation, function):
    # Warm-up
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

def generate_ecdh_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_key.public_key()

alice_private = ec.generate_private_key(ec.SECP256R1())
alice_public = alice_private.public_key()

bob_private = ec.generate_private_key(ec.SECP256R1())
bob_public = bob_private.public_key()

def derive_shared_secret():
    return alice_private.exchange(
        ec.ECDH(),
        bob_public
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
        "ECDH",
        "P-256",
        "KeyGen",
        generate_ecdh_keypair
    )

    #Shared-secret derivation
    record_operation(
        writer,
        "ECDH",
        "P-256",
        "SharedSecret",
        derive_shared_secret
    )

print("ECDH-P256 final benchmark complete.")