from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization

private_key = ec.generate_private_key(
    ec.SECP256R1()
)

public_key = private_key.public_key()

message = b"Quantum-safe migration starts with understanding classical cryptography."

public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("Public key size:", len(public_key_bytes), "bytes")

private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

print("Private key size:", len(private_key_bytes), "bytes")

signature = private_key.sign(
    message,
    ec.ECDSA(hashes.SHA256())
)

print("Signature size:", len(signature),"bytes")