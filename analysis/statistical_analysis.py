import csv
import statistics
from pathlib import Path
from collections import Counter


INPUT = Path("data/raw/benchmark_results.csv")
OUTPUT = Path("analysis/timing_summary.csv")


def load_data():
    with open(INPUT, newline="") as file:
        return list(csv.DictReader(file))


data = load_data()

print("Total observations:", len(data))

#--------------------Dataset validation-------------------------------


expected_iterations = 1500

counts = Counter(
    (row["algorithm"], row["operation"])
    for row in data
)

print("\nAlgorithm + operation counts:")

for (algorithm, operation), count in sorted(counts.items()):
    print(f"{algorithm:8} {operation:15} {count}")

if len(data) != 24000:
    raise ValueError(
        f"Expected 24000 observations, found {len(data)}"
    )

if any(count != expected_iterations for count in counts.values()):
    raise ValueError(
        "One or more algorithm-operation groups "
        "does not contain exactly 1500 observations."
    )

print("\nDataset validation: PASSED")

#-----------------Statistical analysis----------------------------

groups = {}

for row in data:

    key = (
        row["algorithm"],
        row["parameter"],
        row["operation"]
    )

    groups.setdefault(key, []).append(
        float(row["time_seconds"])
    )


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(OUTPUT, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "algorithm",
        "parameter",
        "operation",
        "iterations",
        "mean_seconds",
        "median_seconds",
        "minimum_seconds",
        "maximum_seconds",
        "standard_deviation_seconds"
    ])

    for (
        algorithm,
        parameter,
        operation
    ), values in sorted(groups.items()):

        writer.writerow([
            algorithm,
            parameter,
            operation,
            len(values),
            statistics.mean(values),
            statistics.median(values),
            min(values),
            max(values),
            statistics.stdev(values)
        ])


print("\nStatistical analysis complete.")
print("Output:", OUTPUT)


#--------------Classical vs PQC comparison---------------------------

summary = {}

with open(OUTPUT, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        key = (row["algorithm"], row["operation"])

        summary[key] = {
            "mean": float(row["mean_seconds"]),
            "median": float(row["median_seconds"]),
        }


comparisons = [
    ("RSA", "KeyGen", "ML-KEM", "KeyGen", "RSA_to_ML-KEM"),
    ("ECDH", "KeyGen", "ML-KEM", "KeyGen", "ECDH_to_ML-KEM"),
    ("ECDH", "SharedSecret", "ML-KEM", "Encapsulation", "ECDH_to_ML-KEM"),
    ("ECDH", "SharedSecret", "ML-KEM", "Decapsulation", "ECDH_to_ML-KEM"),
    ("ECDSA", "KeyGen", "ML-DSA", "KeyGen", "ECDSA_to_ML-DSA"),
    ("ECDSA", "Signing", "ML-DSA", "Signing", "ECDSA_to_ML-DSA"),
    ("ECDSA", "Verification", "ML-DSA", "Verification", "ECDSA_to_ML-DSA"),
]


comparison_output = Path(
    "analysis/classical_pqc_comparison.csv"
)

with open(comparison_output, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "comparison",
        "classical_algorithm",
        "classical_operation",
        "pqc_algorithm",
        "pqc_operation",
        "classical_mean_seconds",
        "pqc_mean_seconds",
        "mean_ratio_pqc_to_classical",
        "classical_median_seconds",
        "pqc_median_seconds",
        "median_ratio_pqc_to_classical"
    ])

    for (
        classical_algorithm,
        classical_operation,
        pqc_algorithm,
        pqc_operation,
        label
    ) in comparisons:

        classical = summary[
            (classical_algorithm, classical_operation)
        ]

        pqc = summary[
            (pqc_algorithm, pqc_operation)
        ]

        mean_ratio = (
            pqc["mean"] /
            classical["mean"]
        )

        median_ratio = (
            pqc["median"] /
            classical["median"]
        )

        writer.writerow([
            label,
            classical_algorithm,
            classical_operation,
            pqc_algorithm,
            pqc_operation,
            classical["mean"],
            pqc["mean"],
            mean_ratio,
            classical["median"],
            pqc["median"],
            median_ratio
        ])


print(
    "Comparison analysis complete."
)

print(
    "Output:",
    comparison_output
)

#--------------End-to-end migration workflow comparison----------------

workflow_output = Path(
    "analysis/migration_workflow_comparison.csv"
)

workflow_groups = {
    "ECDH": [
        ("ECDH", "KeyGen"),
        ("ECDH", "SharedSecret"),
    ],
    "ML-KEM": [
        ("ML-KEM", "KeyGen"),
        ("ML-KEM", "Encapsulation"),
        ("ML-KEM", "Decapsulation"),
    ],
    "ECDSA": [
        ("ECDSA", "KeyGen"),
        ("ECDSA", "Signing"),
        ("ECDSA", "Verification"),
    ],
    "ML-DSA": [
        ("ML-DSA", "KeyGen"),
        ("ML-DSA", "Signing"),
        ("ML-DSA", "Verification"),
    ],
}


workflow_results = {}

for workflow, operations in workflow_groups.items():

    mean_total = sum(
        summary[(algorithm, operation)]["mean"]
        for algorithm, operation in operations
    )

    median_total = sum(
        summary[(algorithm, operation)]["median"]
        for algorithm, operation in operations
    )

    workflow_results[workflow] = {
        "mean": mean_total,
        "median": median_total,
    }


workflow_comparisons = [
    ("ECDH", "ML-KEM", "ECDH_to_ML-KEM"),
    ("ECDSA", "ML-DSA", "ECDSA_to_ML-DSA"),
]


with open(
    workflow_output,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "migration",
        "classical_workflow",
        "pqc_workflow",
        "classical_mean_seconds",
        "pqc_mean_seconds",
        "mean_ratio_pqc_to_classical",
        "classical_median_seconds",
        "pqc_median_seconds",
        "median_ratio_pqc_to_classical"
    ])

    for classical, pqc, label in workflow_comparisons:

        classical_mean = workflow_results[classical]["mean"]
        pqc_mean = workflow_results[pqc]["mean"]

        classical_median = workflow_results[classical]["median"]
        pqc_median = workflow_results[pqc]["median"]

        writer.writerow([
            label,
            classical,
            pqc,
            classical_mean,
            pqc_mean,
            pqc_mean / classical_mean,
            classical_median,
            pqc_median,
            pqc_median / classical_median
        ])


print(
    "Workflow comparison complete."
)

print(
    "Output:",
    workflow_output
)