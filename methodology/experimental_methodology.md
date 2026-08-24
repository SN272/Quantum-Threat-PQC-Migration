# Experimental Methodology

## Objective

Evaluate classical cryptographic algorithms and post-quantum
cryptographic algorithms in terms of execution time, key/signature/
ciphertext size, and migration trade-offs.

## Classical Algorithms

- RSA-2048
- ECDSA-P256
- ECDH-P256
- AES-256
- HKDF-SHA256

## Post-Quantum Algorithms

- ML-KEM-768
- ML-DSA-65

## Quantum Demonstrations

- Shor's Algorithm demonstration using N=15
- Grover's Algorithm demonstration using a 2-qubit search space

## Timing Methodology

- Python `time.perf_counter()` is used for high-resolution timing.
- 1500 recorded iterations are used for each benchmark.
- 100 Warm-up executions are performed before recording 1500 measurements.
- Only the cryptographic operation is included in the timed region.
- Individual measurements are retained for statistical analysis.

## Statistical Measures

The following statistics will be calculated:

- Mean
- Median
- Minimum
- Maximum
- Standard deviation
- Distribution/percentile analysis where appropriate

## Size Measurements

Cryptographic object sizes are measured using a consistent
serialization methodology. Raw key material and serialized
representations are distinguished where necessary.

## Environment

Python and cryptographic library versions are recorded alongside
the final experimental results.

## Dataset

The final dataset will contain individual benchmark observations
rather than only aggregated statistics.

## Limitations

Benchmark results are dependent on hardware, operating-system
activity, Python runtime behavior, and cryptographic library
implementation.