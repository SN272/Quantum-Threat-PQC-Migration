from cryptography.hazmat.primitives.asymmetric import mlkem

private_key = mlkem.MLKEM768PrivateKey.generate()
public_key = private_key.public_key()

shared_secret, ciphertext = public_key.encapsulate()

print("Ciphertext length:", len(ciphertext))
print("Shared secret length:", len(shared_secret))

for i in range(5):
    recovered = private_key.decapsulate(ciphertext)
    print(i + 1, "success:", recovered == shared_secret)