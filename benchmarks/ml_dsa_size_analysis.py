from cryptography.hazmat.primitives.asymmetric import mldsa

private_key= mldsa.MLDSA65PrivateKey.generate()
public_key = private_key.public_key()

message = b"Post-quantum migration requires replacing quantum-vulnerable signatures."

signature = private_key.sign(message)

print("ML-DSA-65 Size Analysis")
print(
    "Public key size:",
    len(public_key.public_bytes_raw()),
    "bytes"
)
print(
    "Private key size:",
    len(private_key.private_bytes_raw()),
    "bytes"
)
print(
    "Signature size:",
    len(signature),
    "bytes"
)