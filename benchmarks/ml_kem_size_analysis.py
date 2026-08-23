from cryptography.hazmat.primitives.asymmetric import mlkem

private_key = mlkem.MLKEM768PrivateKey.generate()
public_key = private_key.public_key()

shared_secret, ciphertext = public_key.encapsulate()

print("ML-KEM-768 Size Analysis")
print("Public key size:", len(public_key.public_bytes_raw()), "bytes")
print("Private key size:", len(private_key.private_bytes_raw()), "bytes")
print("Ciphertext size:", len(ciphertext), "bytes")
print("Shared secret size:", len(shared_secret), "bytes")