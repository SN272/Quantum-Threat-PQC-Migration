from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

alice_private_key = ec.generate_private_key(
    ec.SECP256R1()
)

alice_private_key_bytes = alice_private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
print("Private key size:", len(alice_private_key_bytes),"bytes")

alice_public_key = alice_private_key.public_key()

alice_public_key_bytes = alice_public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
print("Public key size", len(alice_public_key_bytes),"bytes")

bob_private_key = ec.generate_private_key(
    ec.SECP256R1()
)

bob_public_key = bob_private_key.public_key()

alice_shared_secret = alice_private_key.exchange(
    ec.ECDH(),
    bob_public_key
)

bob_shared_secret = bob_private_key.exchange(
    ec.ECDH(),
    alice_public_key
)

print("Shared secrets match:", alice_shared_secret==bob_shared_secret)
print("Shared secrets size:", len(alice_shared_secret),"bytes")