import csv
from pathlib import Path

from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import (
    rsa,
    ec,
    mlkem,
    mldsa
)

OUTPUT = Path("data/sizes/cryptographic_sizes.csv")

def add_row(writer, algorithm, parameter, object_type, size, serialization_type):
    writer.writerow([
        algorithm,
        parameter,
        object_type,
        size,
        serialization_type
    ])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", newline="")as file:
    writer = csv.writer(file)
    writer.writerow([
        "algorithm",
        "parameter",
        "object_type",
        "size_bytes",
        "serialization"
    ])

    #-------------------------RSA 2048------------------------------------------------

    rsa_private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    rsa_public = rsa_private.public_key()

    rsa_public_bytes = rsa_public.public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    rsa_private_bytes = rsa_private.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    add_row(
        writer,
        "RSA",
        "2048",
        "PublicKey",
        len(rsa_public_bytes),
        "DER-SPKI"
    )

    add_row(
        writer,
        "RSA",
        "2048",
        "PrivateKey",
        len(rsa_private_bytes),
        "DER-PKCS8"
    )

    #--------------------------------ECDSA P256-------------------------------------

    ecdsa_private = ec.generate_private_key(
        ec.SECP256R1()
    )
    ecdsa_public = ecdsa_private.public_key()

    ecdsa_public_bytes = ecdsa_public.public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    ecdsa_private_bytes = ecdsa_private.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    message = b"Quantum-safe migration benchmark message."

    ecdsa_signature = ecdsa_private.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    add_row(
        writer,
        "ECDSA",
        "P-256",
        "PublicKey",
        len(ecdsa_public_bytes),
        "DER-SPKI"
    )

    add_row(
        writer,
        "ECDSA",
        "P-256",
        "PrivateKey",
        len(ecdsa_private_bytes),
        "DER-PKCS8"
    )

    add_row(
        writer,
        "ECDSA",
        "P-256",
        "Signature",
        len(ecdsa_signature),
        "DER-ECDSA"
    )

    #---------------------ECDH P256----------------------------------------------

    ecdh_private = ec.generate_private_key(ec.SECP256R1())
    ecdh_public = ecdh_private.public_key()

    ecdh_public_bytes = ecdh_public.public_bytes(
        serialization.Encoding.DER,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    ecdh_private_bytes = ecdh_private.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    shared_secret = ecdh_private.exchange(
        ec.ECDH(),
        ecdh_public
    )

    add_row(
        writer,
        "ECDH",
        "P-256",
        "PublicKey",
        len(ecdh_public_bytes),
        "DER-SPKI"
    )

    add_row(
        writer,
        "ECDH",
        "P-256",
        "PrivateKey",
        len(ecdh_private_bytes),
        "DER-PKCS8"
    )

    add_row(
        writer,
        "ECDH",
        "P-256",
        "SharedSecret",
        len(shared_secret),
        "Raw"
    )

    #---------------------ML-KEM-768----------------------------------------------
    kem_private = mlkem.MLKEM768PrivateKey.generate()
    kem_public = kem_private.public_key()

    kem_private_bytes = kem_private.private_bytes_raw()
    kem_public_bytes = kem_public.public_bytes_raw()

    shared_secret, ciphertext = kem_public.encapsulate()

    add_row(
        writer,
        "ML-KEM",
        "768",
        "PublicKey",
        len(kem_public_bytes),
        "StandardizedRaw"
    )

    add_row(
        writer,
        "ML-KEM",
        "768",
        "PrivateKey",
        len(kem_private_bytes),
        "StandardizedRaw"
    )

    add_row(
        writer,
        "ML-KEM",
        "768",
        "Ciphertext",
        len(ciphertext),
        "Raw"
    )

    add_row(
        writer,
        "ML-KEM",
        "768",
        "SharedSecret",
        len(shared_secret),
        "Raw"
    )

    #----------------------------ML-DSA-65----------------------------------------

    dsa_private = mldsa.MLDSA65PrivateKey.generate()
    dsa_public = dsa_private.public_key()

    dsa_private_bytes = dsa_private.private_bytes_raw()
    dsa_public_bytes = dsa_public.public_bytes_raw()

    dsa_signature = dsa_private.sign(message)

    add_row(
        writer,
        "ML-DSA",
        "65",
        "PublicKey",
        len(dsa_public_bytes),
        "StandardizedRaw"
    )

    add_row(
        writer,
        "ML-DSA",
        "65",
        "PrivateKey",
        len(dsa_private_bytes),
        "StandardizedRaw"
    )

    add_row(
        writer,
        "ML-DSA",
        "65",
        "Signature",
        len(dsa_signature),
        "StandardizedRaw"
    )

#----------------------------------------------------------------------------------

print("Cryptographic size analysis completed.")