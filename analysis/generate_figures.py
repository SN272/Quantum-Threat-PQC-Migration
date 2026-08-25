import csv
from pathlib import Path

import matplotlib.pyplot as plt


TIMING = Path("analysis/timing_summary.csv")
WORKFLOW = Path("analysis/migration_workflow_comparison.csv")
SIZES = Path("analysis/size_comparison.csv")

OUTPUT = Path("analysis/figures")
OUTPUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


timing = read_csv(TIMING)
workflow = read_csv(WORKFLOW)
sizes = read_csv(SIZES)


#---------------------Helper: add values above bars--------------------------

def add_bar_labels(bars, values, suffix="", decimals=2):
    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.{decimals}f}{suffix}",
            ha="center",
            va="bottom"
        )


#-----------------1. Classical operation timing------------------------

classical = [
    row for row in timing
    if row["algorithm"] in ("RSA", "ECDSA", "ECDH")
]

labels = [
    f"{row['algorithm']}\n{row['operation']}"
    for row in classical
]

values = [
    float(row["mean_seconds"]) * 1000
    for row in classical
]

plt.figure(figsize=(11, 6))

bars = plt.bar(labels, values)

plt.ylabel("Mean execution time (ms)")
plt.title("Mean Classical Cryptographic Operation Time")
plt.xticks(rotation=45, ha="right")

add_bar_labels(bars, values, suffix=" ms", decimals=3)

plt.tight_layout()
plt.savefig(
    OUTPUT / "01_classical_operation_time.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


#---------------------2. PQC operation timing------------------------

pqc = [
    row for row in timing
    if row["algorithm"] in ("ML-KEM", "ML-DSA")
]

labels = [
    f"{row['algorithm']}\n{row['operation']}"
    for row in pqc
]

values = [
    float(row["mean_seconds"]) * 1000
    for row in pqc
]

plt.figure(figsize=(11, 6))

bars = plt.bar(labels, values)

plt.ylabel("Mean execution time (ms)")
plt.title("Mean Post-Quantum Cryptographic Operation Time")
plt.xticks(rotation=45, ha="right")

add_bar_labels(bars, values, suffix=" ms", decimals=3)

plt.tight_layout()
plt.savefig(
    OUTPUT / "02_pqc_operation_time.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


#------------3. End-to-end workflow overhead--------------------------

labels = [
    "ECDH → ML-KEM",
    "ECDSA → ML-DSA"
]

values = [
    float(row["mean_ratio_pqc_to_classical"])
    for row in workflow
]

plt.figure(figsize=(8, 5))

bars = plt.bar(labels, values)

plt.ylabel("PQC / Classical mean time (×)")
plt.title("End-to-End Modeled PQC Workflow Overhead")

add_bar_labels(bars, values, suffix="×", decimals=2)

plt.tight_layout()
plt.savefig(
    OUTPUT / "03_workflow_overhead.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


#---------------------4. Digital signature size--------------------
row = next(
    row for row in sizes
    if row["comparison"] == "ECDSA_to_ML-DSA_Signature"
)

labels = [
    "ECDSA-P256",
    "ML-DSA-65"
]

values = [
    int(row["classical_size_bytes"]),
    int(row["pqc_size_bytes"])
]

plt.figure(figsize=(7, 5))

bars = plt.bar(labels, values)

plt.ylabel("Signature size (bytes)")
plt.title("Digital Signature Size: Classical vs PQC")

add_bar_labels(bars, values, suffix=" B", decimals=0)

plt.tight_layout()
plt.savefig(
    OUTPUT / "04_signature_size_comparison.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


#------------5. Key-establishment object sizes---------------------------

public_key_row = next(
    row for row in sizes
    if row["comparison"] == "ECDH_to_ML-KEM_PublicKey"
)

ciphertext_row = next(
    row for row in sizes
    if row["comparison"] == "ML-KEM_Ciphertext_vs_ECDH_PublicKey"
)

labels = [
    "ECDH\nPublic Key",
    "ML-KEM\nPublic Key",
    "ML-KEM\nCiphertext"
]

values = [
    int(public_key_row["classical_size_bytes"]),
    int(public_key_row["pqc_size_bytes"]),
    int(ciphertext_row["pqc_size_bytes"])
]

plt.figure(figsize=(8, 5))

bars = plt.bar(labels, values)

plt.ylabel("Size (bytes)")
plt.title("Key-Establishment Object Sizes")

add_bar_labels(bars, values, suffix=" B", decimals=0)

plt.tight_layout()
plt.savefig(
    OUTPUT / "05_kem_communication_sizes.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


#------------------6. Migration size overhead------------------------

comparisons = [
    (
        "ECDH public key\n→ ML-KEM public key",
        "ECDH_to_ML-KEM_PublicKey"
    ),
    (
        "ECDH public key\n→ ML-KEM ciphertext",
        "ML-KEM_Ciphertext_vs_ECDH_PublicKey"
    ),
    (
        "ECDSA signature\n→ ML-DSA signature",
        "ECDSA_to_ML-DSA_Signature"
    )
]

labels = []
values = []

for label, comparison in comparisons:

    row = next(
        row for row in sizes
        if row["comparison"] == comparison
    )

    labels.append(label)
    values.append(
        float(row["size_ratio_pqc_to_classical"])
    )


plt.figure(figsize=(9, 5))

bars = plt.bar(labels, values)

plt.ylabel("PQC / Classical size (×)")
plt.title("PQC Migration Size Overhead")

add_bar_labels(bars, values, suffix="×", decimals=2)

plt.tight_layout()
plt.savefig(
    OUTPUT / "06_migration_size_overhead.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


#-----------------------------------------------------------------------

print("Figures generated successfully.")

for figure in sorted(OUTPUT.glob("*.png")):
    print(figure)