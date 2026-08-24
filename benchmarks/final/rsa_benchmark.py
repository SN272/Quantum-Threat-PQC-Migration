import csv
import time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa, padding
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
    # Warm-up
    for _ in range(WARMUP):
        function()

    # Recorded measurements
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

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key.public_key()

# Prepare RSA keys

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

message = b"Quantum-safe migration benchmark message."

signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

encrypted_message = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
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

    record_operation(
        writer,
        "RSA",
        "2048",
        "KeyGen",
        generate_rsa_keypair
    )
    
    record_operation(
        writer,
        "RSA",
        "2048",
        "Verification",
        lambda: public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    )

    record_operation(
        writer,
        "RSA",
        "2048",
        "Encryption",
        lambda: public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    )

    record_operation(
        writer,
        "RSA",
        "2048",
        "Decryption",
        lambda: private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    )

    record_operation(
        writer,
        "RSA",
        "2048",
        "Signing",
        lambda: private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    )

print("RSA-2048 final benchmark complete.")