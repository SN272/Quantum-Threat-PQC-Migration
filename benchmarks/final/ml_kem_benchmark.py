import csv
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import mlkem

WARMUP = 100
ITERATIONS = 1500

OUTPUT = Path("data/raw/benchmark_results.csv")

def record_operation(writer, algorithm, parameter, operation, function, input_factory=None):
    #Warm-up
    for _ in range(WARMUP):
        if input_factory:
            input_data = input_factory()
            function(input_data)
        else:
            function()

    #Recorded measurements
    for iteration in range(1, ITERATIONS+1):
        if input_factory:
            input_data = input_factory()
                
        start = time.perf_counter()

        if input_factory:
            input_data = input_factory()
            function(input_data)
        else:
            function()
        
        end = time.perf_counter()

        writer.writerow([
            algorithm,
            parameter,
            "PQC",
            operation,
            iteration,
            end-start
        ])

private_key = mlkem.MLKEM768PrivateKey.generate()
public_key = private_key.public_key()

def generate_mlkem_keypair():
    private_key = mlkem.MLKEM768PrivateKey.generate()
    private_key.public_key()

def encapsulate():
    public_key.encapsulate()

def prepare_ciphertext():
    return public_key.encapsulate()[1]

def decapsulate(ciphertext):
    private_key.decapsulate(ciphertext)

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

file_exists = OUTPUT.exists

with open(OUTPUT, "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "algorithm",
            "parameter",
            "category",
            "operation",
            "iteration",
            "time_seconds"
        ])

    #Key Generation
    record_operation(
        writer,
        "ML-KEM",
        "768",
        "KeyGen",
        generate_mlkem_keypair
    )

    #Encapsulation
    record_operation(
        writer,
        "ML-KEM",
        "768",
        "Encapsulation",
        encapsulate
    )

    #Decapsulation
    record_operation(
        writer,
        "ML-KEM",
        "768",
        "Decapsulation",
        decapsulate,
        input_factory=prepare_ciphertext
    )

print("ML-KEM-768 final benchmark complete.")