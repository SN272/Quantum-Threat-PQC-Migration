from cryptography.hazmat.primitives.asymmetric import mlkem
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Bob's keys
private_key = mlkem.MLKEM768PrivateKey.generate()
public_key = private_key.public_key()

# Alice use bob keys
shared_secret_alice, ciphertext = public_key.encapsulate()

# Bob decapsulates
shared_secret_bob = private_key.decapsulate(
    ciphertext
)

print(
    "Shared secrets match:",
    shared_secret_alice == shared_secret_bob
)

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"ML-KEM secure channel"
)

aes_key_alice = hkdf.derive(shared_secret_alice)

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"ML-KEM secure channel"
)

aes_key_bob = hkdf.derive(shared_secret_bob)

print(
    "AES keys match:",
    aes_key_alice == aes_key_bob
)


# ------------------Encryption-------------------------

message  = b"Confidential message protected using a PQC-established key."

nonce = os.urandom(12)

aesgcm = AESGCM(aes_key_alice)

ciphertext_data = aesgcm.encrypt(
    nonce,
    message,
    None
)

#---------------------Decryption--------------------------
decrpyted_message = aesgcm.decrypt(
    nonce,
    ciphertext_data,
    None
)

print("Decryption successful:", decrpyted_message==message)
