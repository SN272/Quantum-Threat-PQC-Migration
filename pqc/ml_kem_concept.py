operations = {
    "KeyGen": "Generate public key and private key",
    "Encaps": "Use public key to generate ciphertext and shared secret",
    "Decaps": "Use private key and ciphertext to recover shared secret"
}

for operation, description in operations.items():
    print(f"{operation}: {description}")