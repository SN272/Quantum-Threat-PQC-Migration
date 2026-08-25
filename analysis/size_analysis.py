import csv
from pathlib import Path


INPUT = Path("data/sizes/cryptographic_sizes.csv")
OUTPUT = Path("analysis/size_summary.csv")
COMPARISON_OUTPUT = Path("analysis/size_comparison.csv")


#-------------Load size dataset---------------------------------------

with open(INPUT, newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))


print("Total size measurements:", len(rows))


#---------------Create lookup--------------------------------------

sizes = {}

for row in rows:

    key = (
        row["algorithm"],
        row["parameter"],
        row["object_type"]
    )

    sizes[key] = {
        "size": int(row["size_bytes"]),
        "serialization": row["serialization"]
    }


#------------------Write normalized size summary-------------------

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "algorithm",
        "parameter",
        "object_type",
        "size_bytes",
        "serialization"
    ])

    for row in rows:
        writer.writerow([
            row["algorithm"],
            row["parameter"],
            row["object_type"],
            row["size_bytes"],
            row["serialization"]
        ])


#----------Migration-relevant comparisons---------------------------

comparisons = [
    (
        "ECDSA_to_ML-DSA_Signature",
        ("ECDSA", "P-256", "Signature"),
        ("ML-DSA", "65", "Signature")
    ),

    (
        "ECDH_to_ML-KEM_PublicKey",
        ("ECDH", "P-256", "PublicKey"),
        ("ML-KEM", "768", "PublicKey")
    ),

    (
        "ECDH_to_ML-KEM_PrivateKey",
        ("ECDH", "P-256", "PrivateKey"),
        ("ML-KEM", "768", "PrivateKey")
    ),

    (
        "ECDH_to_ML-KEM_SharedSecret",
        ("ECDH", "P-256", "SharedSecret"),
        ("ML-KEM", "768", "SharedSecret")
    ),

    (
        "ML-KEM_Ciphertext_vs_ECDH_PublicKey",
        ("ECDH", "P-256", "PublicKey"),
        ("ML-KEM", "768", "Ciphertext")
    ),

    (
        "RSA_to_ML-DSA_PublicKey",
        ("RSA", "2048", "PublicKey"),
        ("ML-DSA", "65", "PublicKey")
    ),

    (
        "RSA_to_ML-KEM_PublicKey",
        ("RSA", "2048", "PublicKey"),
        ("ML-KEM", "768", "PublicKey")
    ),
]


with open(
    COMPARISON_OUTPUT,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "comparison",
        "classical_algorithm",
        "classical_parameter",
        "classical_object",
        "pqc_algorithm",
        "pqc_parameter",
        "pqc_object",
        "classical_size_bytes",
        "pqc_size_bytes",
        "size_ratio_pqc_to_classical",
        "additional_bytes"
    ])

    for (
        label,
        classical_key,
        pqc_key
    ) in comparisons:

        classical = sizes[classical_key]
        pqc = sizes[pqc_key]

        classical_size = classical["size"]
        pqc_size = pqc["size"]

        writer.writerow([
            label,
            classical_key[0],
            classical_key[1],
            classical_key[2],
            pqc_key[0],
            pqc_key[1],
            pqc_key[2],
            classical_size,
            pqc_size,
            pqc_size / classical_size,
            pqc_size - classical_size
        ])


print("Size analysis complete.")
print("Output:", OUTPUT)
print("Output:", COMPARISON_OUTPUT)