from cryptography.hazmat.primitives.asymmetric import mlkem

private_key = mlkem.MLKEM768PrivateKey.generate()

public_key = private_key.public_key()

shared_secret_alice, ciphertext = public_key.encapsulate()

shared_secret_bob = private_key.decapsulate(
    ciphertext
)

print("ML-KEM-768")
print("Ciphertext generated")
print("Shared secrets match:", shared_secret_alice == shared_secret_bob)

print("Public key size:", len(public_key.public_bytes_raw()), "bytes")
print("Private key size:", len(private_key.private_bytes_raw()), "bytes")
print("Ciphertext size:", len(ciphertext), "bytes")
print("Shared secret size:", len(shared_secret_alice), "bytes")