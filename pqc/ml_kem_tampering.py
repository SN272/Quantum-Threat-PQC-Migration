from cryptography.hazmat.primitives.asymmetric import mlkem

private_key = mlkem.MLKEM768PrivateKey.generate()
public_key = private_key.public_key()

shared_Secret_alice, ciphertext = public_key.encapsulate()

print("Original ciphertext length:", len(ciphertext))

#Tamper with 1 byte
tampered_ciphertxt = bytearray(ciphertext)
tampered_ciphertxt[0] ^= 1
tampered_ciphertxt = bytes(tampered_ciphertxt)

print("Ciphertext modified")

try:
    shared_Secret_bob = private_key.decapsulate(
        tampered_ciphertxt
    )
    print("Shared secretsmatch:", shared_Secret_alice==shared_Secret_bob)
except ValueError:
    print("Tampering detected: decapsulation failed")