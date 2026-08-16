import os

from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

alice_private_key = ec.generate_private_key(    #a
    ec.SECP256R1()
)

alice_public_key = alice_private_key.public_key()   #A=aG

bob_private_key = ec.generate_private_key(  #b
    ec.SECP256R1()
)
bob_public_key = bob_private_key.public_key() #B=bG

alice_shared_secret = alice_private_key.exchange(   #S(A) = aB = a(bG)
    ec.ECDH(),
    bob_public_key
)

bob_shared_secret = bob_private_key.exchange(   #S(B) = bA = b(aG)
    ec.ECDH(),
    alice_public_key
)
'''
print("Alice shared secret:", alice_shared_secret.hex())
print("Bob shared secret:", bob_shared_secret.hex())
print("Secrets match:", alice_shared_secret==bob_shared_secret)
'''

alice_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"quantum-threat-pqc-migration"
).derive(alice_shared_secret)

bob_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"quantum-threat-pqc-migration"
).derive(bob_shared_secret)

'''
print("Derived key:", alice_key.hex())
print("Keys match:", alice_key == bob_key)
'''

#Create AES Key
aes = AESGCM(alice_key)
nonce = os.urandom(12)

message = b"Post-quantum migration is important."

ciphertext = aes.encrypt(
    nonce,
    message,
    None
)

tampered_ciphertext = bytearray(ciphertext)
tampered_ciphertext[0] ^= 1

bob_aes = AESGCM(bob_key)

try:
    decrypted = bob_aes.decrypt(
        nonce,
        bytes(tampered_ciphertext),
        None
    )
    print("Tampered message decrypted:", decrypted)
except Exception:
    print("Tampering detected - authentication failed")

'''
print("Original message:", message)
print("Ciphertext:", ciphertext.hex())
print("Decrypted message:", decrypted)
print("Message recovered:", message == decrypted)
'''