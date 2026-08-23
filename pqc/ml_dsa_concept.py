operations = {
    "KeyGen": "Generate public key and private key",
    "Sign": "Use private key to generate a signature for a message",
    "Verify": "Use public key to verify the signature"
}

for operation, description in operations.items():
    print(f"{operation}: {description}")