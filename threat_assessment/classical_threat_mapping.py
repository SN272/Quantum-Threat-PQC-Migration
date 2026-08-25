threats = {
    "RSA-2048": {
        "security_assumption": "Integer factorization",
        "quantum_algorithm": "Shor's Algorithm",
        "quantum_status": "Vulnerable",
        "migration_target": "ML-KEM-768 for key establishment/encryption; ML-DSA-65 for signatures"
    },
    "ECDSA-P256": {
        "security_assumption": "Elliptic Curve Discrete Logarithm Problem",
        "quantum_algorithm": "Shor's Algorithm",
        "quantum_status": "Vulnerable",
        "migration_target": "ML-DSA-65"
    },
    "ECDH-P256": {
        "security_assumption": "Elliptic Curve Discrete Logarithm Problem",
        "quantum_algorithm": "Shor's Algorithm",
        "quantum_status": "Vulnerable",
        "migration_target": "ML-KEM-768"
    },
    "AES-256": {
        "security_assumption": "Symmetric-key security",
        "quantum_algorithm": "Grover's Algorithm",
        "quantum_status": "Reduced security margin",
        "migration_target": "Retain with adequate key size"
    },
    "HKDF-SHA256": {
        "security_assumption": "HMAC/hash security",
        "quantum_algorithm": "No direct Shor attack",
        "quantum_status": "Not a public-key migration target",
        "migration_target": "Retain"
    }
}

for algo, info in threats.items():
    print("\n", algo)
    for key, value in info.items():
        print(f"{key}: {value}")