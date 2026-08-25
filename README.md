# Quantum Threat Assessment & Post-Quantum Migration

A practical assessment of the impact of quantum computing on classical public-key cryptography and the engineering considerations involved in migrating to post-quantum cryptography (PQC).

## Overview

This project evaluates the quantum vulnerability of RSA-2048, ECDSA-P256, and ECDH-P256, and studies migration to ML-DSA-65 and ML-KEM-768.

The project combines:

- Quantum-threat demonstrations using Shor's and Grover's algorithms
- Classical and post-quantum cryptographic implementations
- Controlled performance benchmarking
- Cryptographic object-size analysis
- Statistical comparison of classical and PQC mechanisms
- Practical PQC migration assessment

## Algorithms

| Mechanism | Function | Quantum status | PQC direction |
|---|---|---|---|
| RSA-2048 | Encryption / signatures | Vulnerable to Shor's Algorithm | ML-KEM-768 / ML-DSA-65 |
| ECDH-P256 | Key establishment | Vulnerable to Shor's Algorithm | ML-KEM-768 |
| ECDSA-P256 | Digital signatures | Vulnerable to Shor's Algorithm | ML-DSA-65 |
| AES-256 | Symmetric encryption | Reduced security margin under Grover's Algorithm | Retain |
| HKDF-SHA256 | Key derivation | No direct Shor attack | Retain |

## Benchmarking

The final benchmark dataset contains **24,000 observations**, with **1,500 iterations per algorithm-operation pair**.

The study measures:

- Key generation
- Encryption / decryption
- Signing / verification
- Key establishment
- Encapsulation / decapsulation
- Cryptographic object sizes

### Key Results

| Migration | Main measured impact |
|---|---:|
| ECDH -> ML-KEM | 5.48x modeled mean workflow time |
| ECDSA -> ML-DSA | 12.95x modeled mean workflow time |
| ECDH public key -> ML-KEM public key | 13.01x public-key size |
| ECDSA signature -> ML-DSA signature | 45.96x size |

These measurements represent implementation-level engineering trade-offs and do not change the underlying quantum vulnerability of the classical mechanisms.

## Project Structure

```text
analysis/
    Statistical and size analysis
    Comparison datasets
    Findings
    Final figures

benchmarks/
    baseline/       Initial benchmark implementations
    final/          Final benchmark implementations

data/
    raw/            Raw benchmark results
    sizes/          Cryptographic object-size measurements

methodology/
    Experimental methodology

pqc/
    ML-KEM and ML-DSA implementations and demonstrations

quantum_threat/
    Shor's and Grover's demonstrations

threat_assessment/
    Classical quantum-threat mapping
    PQC migration assessment
```

## Installation

Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Reproduction

Run the benchmark scripts from `benchmarks/final/` to generate benchmark data.

Statistical analysis:

```powershell
python analysis\statistical_analysis.py
```

Size analysis:

```powershell
python analysis\size_analysis.py
```

Generate figures:

```powershell
python analysis\generate_figures.py
```

Threat mapping:

```powershell
python threat_assessment\classical_threat_mapping.py
```

The resulting datasets and figures are stored under `data/` and `analysis/`.

## Migration Assessment

The project uses a function-based migration approach:

- ECDH -> ML-KEM for key establishment
- ECDSA -> ML-DSA for digital signatures
- RSA migration depends on the cryptographic function being performed

The detailed migration assessment, measured overheads, decision matrix, and recommendations are available in:

`threat_assessment/pqc_migration_assessment.md`

Detailed experimental findings are available in:

`analysis/findings.md`

## Limitations

The measurements represent the specific implementations, software environment, and hardware used for this project. They should therefore be interpreted as experimental engineering measurements rather than universal performance benchmarks.

The project focuses on RSA-2048, ECDH-P256, ECDSA-P256, ML-KEM-768, and ML-DSA-65 rather than providing an exhaustive evaluation of all classical and post-quantum algorithms.

## Conclusion

The results demonstrate that post-quantum migration introduces measurable computational and communication overhead, particularly for digital signatures and public-key/ciphertext sizes.

The project therefore evaluates PQC migration as an engineering trade-off involving **quantum risk, cryptographic function, performance, and communication/storage constraints** rather than as a simple algorithm-for-algorithm replacement.
