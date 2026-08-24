from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

private_key = ec.generate_private_key(
    ec.SECP256R1()
)

public_key = private_key.public_key()
print("ECDSA key pair generated")

message = b"Quantum-safe migration starts with understanding ecc"

signature = private_key.sign(
    message,
    ec.ECDSA(hashes.SHA256())
)

print("Signature generated")
print("Signature length: ", len(signature))

message = b"Quantum-safe migration starts with understanding ECC"
try:
    public_key.verify(
        signature,
        message,
        ec.ECDSA(hashes.SHA256())
    )
    print("Signature valid")
except Exception:
    print("Signature invalid")