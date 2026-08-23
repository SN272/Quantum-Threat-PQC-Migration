from cryptography.hazmat.primitives.asymmetric import mldsa
from cryptography.exceptions import InvalidSignature

private_key = mldsa.MLDSA65PrivateKey.generate()
public_key = private_key.public_key()

message = b"Post-quantum migration requires replacing quantum-vulnerable signatures."

signature = private_key.sign(message)

print("ML-DSA-65")
print("Signature generated")
print("Signature length:", len(signature))

try:
    public_key.verify(signature, message)
    print("Signature valid")
except InvalidSignature:
    print("Signature invalid")

tampered_message = b"Post-quantum migration requires replacing quantum-vulnerable encryption."

try:
    public_key.verify(signature, tampered_message)
    print("Tampered message accepted")

except InvalidSignature:
    print("Tampering detected - signature invalid")