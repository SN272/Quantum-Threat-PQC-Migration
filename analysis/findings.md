# PQC Migration Benchmark Findings

## 1. Dataset and Experimental Scope

The benchmark dataset contains 24,000 timing observations across five cryptographic algorithms:

- RSA-2048
- ECDSA P-256
- ECDH P-256
- ML-KEM-768
- ML-DSA-65

Each algorithm-operation combination was measured over 1,500 iterations. The dataset validation completed successfully before statistical analysis.

The size analysis contains 15 cryptographic object measurements covering public keys, private keys, signatures, ciphertexts, and shared secrets.

## 2. Timing Findings

### 2.1 Classical cryptography

Measured mean execution times:

| Algorithm | Operation | Mean |
|---|---|---:|
| ECDH | KeyGen | 0.027 ms |
| ECDH | SharedSecret | 0.075 ms |
| ECDSA | KeyGen | 0.026 ms |
| ECDSA | Signing | 0.038 ms |
| ECDSA | Verification | 0.098 ms |
| RSA-2048 | KeyGen | 72.395 ms |
| RSA-2048 | Encryption | 0.040 ms |
| RSA-2048 | Decryption | 0.420 ms |
| RSA-2048 | Signing | 0.440 ms |
| RSA-2048 | Verification | 0.045 ms |

RSA-2048 key generation is substantially more expensive than the other measured classical operations and dominates the overall classical timing scale.

### 2.2 Post-quantum cryptography

Measured mean execution times:

| Algorithm | Operation | Mean |
|---|---|---:|
| ML-KEM-768 | KeyGen | 0.294 ms |
| ML-KEM-768 | Encapsulation | 0.072 ms |
| ML-KEM-768 | Decapsulation | 0.194 ms |
| ML-DSA-65 | KeyGen | 0.314 ms |
| ML-DSA-65 | Signing | 1.517 ms |
| ML-DSA-65 | Verification | 0.273 ms |

ML-KEM encapsulation is close to ECDH shared-secret generation in the measured environment, while ML-KEM decapsulation is slower. ML-DSA signing shows the largest timing increase relative to its classical counterpart.

## 3. Classical-to-PQC Operation Comparisons

### ECDH → ML-KEM

| Operation mapping | Mean ratio (PQC / Classical) | Median ratio |
|---|---:|---:|
| KeyGen → KeyGen | 10.85× | 10.73× |
| SharedSecret → Encapsulation | 0.96× | 0.92× |
| SharedSecret → Decapsulation | 2.58× | 2.33× |

The measurements show that ML-KEM key generation is substantially slower than ECDH key generation. However, encapsulation is approximately comparable to ECDH shared-secret computation, while decapsulation introduces a larger computational cost.

### ECDSA → ML-DSA

| Operation mapping | Mean ratio (PQC / Classical) | Median ratio |
|---|---:|---:|
| KeyGen → KeyGen | 12.02× | 11.01× |
| Signing → Signing | 39.99× | 33.06× |
| Verification → Verification | 2.77× | 2.78× |

The largest measured performance impact occurs during digital signature generation. ML-DSA signing is approximately 40 times slower than ECDSA signing in this benchmark environment.

## 4. End-to-End Modeled Migration Workflow

The modeled workflow comparisons combine the relevant operations for each migration:

| Migration | Classical mean | PQC mean | Mean overhead |
|---|---:|---:|---:|
| ECDH → ML-KEM | 0.102 ms | 0.560 ms | 5.48× |
| ECDSA → ML-DSA | 0.162 ms | 2.103 ms | 12.95× |

The modeled ECDH-to-ML-KEM workflow therefore requires approximately 5.48 times the measured execution time of the corresponding ECDH workflow.

The modeled ECDSA-to-ML-DSA workflow has a larger relative overhead of approximately 12.95 times. The difference is primarily influenced by the substantially higher ML-DSA signing cost.

These workflow ratios describe the specific operations included in this project's modeled migration workflow; they should not be interpreted as universal application-level performance factors.

## 5. Cryptographic Object Size Findings

### Key establishment

| Object | Size |
|---|---:|
| ECDH P-256 Public Key | 91 B |
| ML-KEM-768 Public Key | 1,184 B |
| ML-KEM-768 Ciphertext | 1,088 B |
| ECDH P-256 Shared Secret | 32 B |
| ML-KEM-768 Shared Secret | 32 B |

The ML-KEM public key is approximately 13.01 times the measured ECDH public-key size. The ML-KEM ciphertext is approximately 11.96 times the ECDH public-key size.

An important positive observation is that both ECDH and ML-KEM produce a 32-byte shared secret in the measured implementation.

### Digital signatures

| Object | Size |
|---|---:|
| ECDSA P-256 Signature | 72 B |
| ML-DSA-65 Signature | 3,309 B |

The ML-DSA signature is approximately 45.96 times the measured ECDSA signature size, adding 3,237 bytes per signature.

### Other measured sizes

- RSA-2048 public key: 294 B
- ML-KEM-768 public key: 1,184 B
- ML-DSA-65 public key: 1,952 B
- ECDH P-256 private key: 138 B
- ML-KEM-768 private key: 64 B in the measured standardized-raw representation

The size values above describe the representations used by this project's benchmark and should therefore be interpreted as measured object sizes rather than universal serialized sizes for every cryptographic library or protocol format.

## 6. Main Migration Implications

### 6.1 Performance

PQC migration introduces measurable computational overhead in the tested environment. The impact is not uniform across operations:

- ML-KEM encapsulation is close to ECDH shared-secret computation.
- ML-KEM decapsulation is moderately more expensive.
- ML-KEM key generation is substantially slower than ECDH key generation.
- ML-DSA verification has a moderate increase over ECDSA verification.
- ML-DSA signing is the dominant signature-operation overhead.

### 6.2 Communication and storage

PQC introduces a much larger communication footprint for several cryptographic objects:

- ML-KEM public keys and ciphertexts are roughly an order of magnitude larger than the measured ECDH public key.
- ML-DSA signatures are roughly 46 times larger than ECDSA signatures.
- Shared-secret size remains 32 bytes in the measured ECDH/ML-KEM comparison.

Therefore, PQC migration affects not only CPU cost but also bandwidth, packet sizes, certificate or key storage, and protocol message design.

### 6.3 Security-migration trade-off

The benchmark demonstrates a practical engineering trade-off: replacing quantum-vulnerable classical public-key mechanisms with post-quantum mechanisms can increase computational and communication overhead, even though the migration is motivated by the need for quantum-resistant security.

The results support evaluating PQC migration at the system and protocol level rather than comparing algorithms only by cryptographic security properties.

## 7. Important Limitations

1. The measurements represent this project's execution environment and implementation choices.
2. Timing results are benchmark measurements, not theoretical complexity estimates.
3. The modeled workflow ratios cover only the operations defined in the project and do not represent complete application-level latency.
4. Size comparisons depend on the representation/serialization format measured by the project.
5. The benchmark does not claim that every implementation of the same algorithm will produce identical timings or object sizes.
6. The analysis focuses on ML-KEM-768 and ML-DSA-65 and therefore does not generalize directly to all PQC parameter sets.

## 8. Overall Finding

The benchmark provides quantitative evidence that PQC migration changes both computational and data-size characteristics.

For this implementation and measurement environment, the modeled ECDH → ML-KEM workflow incurs approximately **5.48×** mean timing overhead, while the modeled ECDSA → ML-DSA workflow incurs approximately **12.95×** mean timing overhead. Communication and signature objects can increase substantially, with the measured ML-KEM public key being **13.01×** the ECDH public-key size and the ML-DSA signature being **45.96×** the ECDSA signature size.

At the same time, the measured ML-KEM shared secret remains **32 bytes**, matching the ECDH shared-secret size. This highlights that PQC migration does not impose a uniform overhead across every cryptographic object or operation; the impact depends on the specific primitive and workflow component being replaced.
