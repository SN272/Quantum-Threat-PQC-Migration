from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Quantum Threat & PQC Migration",
    page_icon="⚛️",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = ROOT / "analysis"

TIMING_FILE = ANALYSIS_DIR / "timing_summary.csv"
WORKFLOW_FILE = ANALYSIS_DIR / "migration_workflow_comparison.csv"
SIZE_FILE = ANALYSIS_DIR / "size_comparison.csv"


# ============================================================
# Helpers
# ============================================================

@st.cache_data
def load_csv(path):
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def markdown_table(df, columns=None, headers=None, digits=3):
    """Render a pandas DataFrame as a Markdown table without PyArrow."""
    if columns is not None:
        df = df[columns].copy()

    if headers is not None:
        df.columns = headers

    # Round numeric values for readability
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].map(
                lambda x: (
                    f"{x:.{digits}f}"
                    if isinstance(x, float)
                    else str(x)
                )
            )

    header = "| " + " | ".join(str(c) for c in df.columns) + " |"
    separator = "|" + "|".join(["---"] * len(df.columns)) + "|"

    rows = []

    for _, row in df.iterrows():
        rows.append(
            "| "
            + " | ".join(str(value) for value in row)
            + " |"
        )

    st.markdown(
        "\n".join([header, separator] + rows)
    )


def metric_card(label, value, description=None):
    st.metric(
        label,
        value,
        description,
    )


def show_bar_chart(labels, values, title, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(labels, values)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=35)

    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# Load data
# ============================================================

timing = load_csv(TIMING_FILE)
workflow = load_csv(WORKFLOW_FILE)
size_comparison = load_csv(SIZE_FILE)


# ============================================================
# Header
# ============================================================

st.title("Quantum Threat Assessment & PQC Migration")

st.caption(
    "Performance, size, and migration analysis of classical "
    "public-key cryptography and post-quantum replacements."
)

st.markdown(
    """
This dashboard presents the experimental results from the project,
focusing on **RSA-2048, ECDSA-P256, ECDH-P256, ML-KEM-768,
and ML-DSA-65**.
"""
)


# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Performance",
        "Size Analysis",
        "Threat & Migration",
        "Methodology",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "[🔗 View Project on GitHub](https://github.com/SN272/Quantum-Threat-PQC-Migration.git)"
)
st.sidebar.caption("Quantum Threat Assessment & PQC Migration")


# ============================================================
# OVERVIEW
# ============================================================

if section == "Overview":

    st.header("Project Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Total Observations", "24,000")

    with col2:
        metric_card("Iterations / Operation", "1,500")

    with col3:
        metric_card("Algorithms Evaluated", "5")

    st.markdown("---")

    st.subheader("Classical → PQC Migration")

    mapping = pd.DataFrame(
        {
            "Classical Mechanism": [
                "RSA-2048",
                "ECDH-P256",
                "ECDSA-P256",
            ],
            "Function": [
                "Encryption / signatures",
                "Key establishment",
                "Digital signatures",
            ],
            "Quantum Threat": [
                "Shor's Algorithm",
                "Shor's Algorithm",
                "Shor's Algorithm",
            ],
            "PQC Direction": [
                "ML-KEM-768 / ML-DSA-65",
                "ML-KEM-768",
                "ML-DSA-65",
            ],
        }
    )

    markdown_table(mapping)

    st.markdown("---")

    st.subheader("Key Results")

    col1, col2 = st.columns(2)

    with col1:
        metric_card(
            "ECDH → ML-KEM",
            "5.48×",
            "modeled mean workflow overhead",
        )

        metric_card(
            "ML-KEM Public Key",
            "13.01×",
            "ECDH public-key size",
        )

    with col2:
        metric_card(
            "ECDSA → ML-DSA",
            "12.95×",
            "modeled mean workflow overhead",
        )

        metric_card(
            "ML-DSA Signature",
            "45.96×",
            "ECDSA signature size",
        )

    st.markdown("---")

    st.subheader("Project Scope")

    st.markdown(
        """
The project combines:

- Quantum-threat demonstrations using **Shor's and Grover's algorithms**
- Classical and post-quantum cryptographic implementations
- Controlled performance benchmarking
- Cryptographic object-size analysis
- Statistical comparison
- Practical PQC migration assessment
"""
    )


# ============================================================
# PERFORMANCE
# ============================================================

elif section == "Performance":

    st.header("Performance Analysis")

    if timing.empty:
        st.error("Timing dataset not found.")
        st.stop()

    st.subheader("Operation Timing")

    algorithms = sorted(timing["algorithm"].unique())

    selected_algorithms = st.multiselect(
        "Algorithms",
        algorithms,
        default=algorithms,
    )

    filtered = timing[
        timing["algorithm"].isin(selected_algorithms)
    ].copy()

    filtered["mean_ms"] = filtered["mean_seconds"] * 1000

    labels = (
        filtered["algorithm"]
        + " — "
        + filtered["operation"]
    ).tolist()

    values = filtered["mean_ms"].tolist()

    show_bar_chart(
        labels,
        values,
        "Mean Cryptographic Operation Time",
        "Mean time (ms)",
    )

    st.markdown("---")

    st.subheader("Detailed Timing Results")

    timing_display = filtered.copy()

    timing_display["mean_seconds"] = timing_display[
        "mean_seconds"
    ].map(lambda x: f"{x:.8f}")

    timing_display["median_seconds"] = timing_display[
        "median_seconds"
    ].map(lambda x: f"{x:.8f}")

    timing_display["minimum_seconds"] = timing_display[
        "minimum_seconds"
    ].map(lambda x: f"{x:.8f}")

    timing_display["maximum_seconds"] = timing_display[
        "maximum_seconds"
    ].map(lambda x: f"{x:.8f}")

    timing_display["standard_deviation_seconds"] = timing_display[
        "standard_deviation_seconds"
    ].map(lambda x: f"{x:.8f}")

    markdown_table(
        timing_display,
        columns=[
            "algorithm",
            "parameter",
            "operation",
            "iterations",
            "mean_seconds",
            "median_seconds",
            "minimum_seconds",
            "maximum_seconds",
            "standard_deviation_seconds",
        ],
        headers=[
            "Algorithm",
            "Parameter",
            "Operation",
            "Iterations",
            "Mean (s)",
            "Median (s)",
            "Min (s)",
            "Max (s)",
            "Std. Dev. (s)",
        ],
    )

    st.markdown("---")

    st.subheader("Classical vs PQC Workflow Overhead")

    if workflow.empty:
        st.warning("Workflow comparison dataset not found.")
    else:

        workflow_display = workflow.copy()

        workflow_display["classical_mean_ms"] = (
            workflow_display["classical_mean_seconds"] * 1000
        )

        workflow_display["pqc_mean_ms"] = (
            workflow_display["pqc_mean_seconds"] * 1000
        )

        labels = workflow_display["migration"].tolist()

        classical_values = workflow_display[
            "classical_mean_ms"
        ].tolist()

        pqc_values = workflow_display[
            "pqc_mean_ms"
        ].tolist()

        fig, ax = plt.subplots(figsize=(9, 5))

        x = range(len(labels))
        width = 0.35

        ax.bar(
            [i - width / 2 for i in x],
            classical_values,
            width,
            label="Classical",
        )

        ax.bar(
            [i + width / 2 for i in x],
            pqc_values,
            width,
            label="PQC",
        )

        ax.set_xticks(list(x))
        ax.set_xticklabels(labels)
        ax.set_ylabel("Mean workflow time (ms)")
        ax.set_title("Classical vs PQC Workflow Time")
        ax.legend()

        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        workflow_display["mean_ratio_pqc_to_classical"] = (
            workflow_display[
                "mean_ratio_pqc_to_classical"
            ].map(lambda x: f"{x:.2f}×")
        )

        workflow_display["median_ratio_pqc_to_classical"] = (
            workflow_display[
                "median_ratio_pqc_to_classical"
            ].map(lambda x: f"{x:.2f}×")
        )

        workflow_display["classical_mean_ms"] = (
            workflow_display["classical_mean_ms"]
            .map(lambda x: f"{x:.3f}")
        )

        workflow_display["pqc_mean_ms"] = (
            workflow_display["pqc_mean_ms"]
            .map(lambda x: f"{x:.3f}")
        )

        markdown_table(
            workflow_display,
            columns=[
                "migration",
                "classical_mean_ms",
                "pqc_mean_ms",
                "mean_ratio_pqc_to_classical",
                "median_ratio_pqc_to_classical",
            ],
            headers=[
                "Migration",
                "Classical Mean (ms)",
                "PQC Mean (ms)",
                "Mean Ratio",
                "Median Ratio",
            ],
        )


# ============================================================
# SIZE ANALYSIS
# ============================================================

elif section == "Size Analysis":

    st.header("Cryptographic Object Size Analysis")

    if size_comparison.empty:
        st.error("Size comparison dataset not found.")
        st.stop()

    st.subheader("Measured Size Comparisons")

    size_display = size_comparison.copy()

    size_display["classical_size"] = size_display[
        "classical_size_bytes"
    ].map(lambda x: f"{int(x):,} B")

    size_display["pqc_size"] = size_display[
        "pqc_size_bytes"
    ].map(lambda x: f"{int(x):,} B")

    size_display["size_ratio"] = size_display[
        "size_ratio_pqc_to_classical"
    ].map(lambda x: f"{x:.2f}×")

    markdown_table(
        size_display,
        columns=[
            "comparison",
            "classical_algorithm",
            "classical_object",
            "pqc_algorithm",
            "pqc_object",
            "classical_size",
            "pqc_size",
            "size_ratio",
            "additional_bytes",
        ],
        headers=[
            "Comparison",
            "Classical",
            "Classical Object",
            "PQC",
            "PQC Object",
            "Classical Size",
            "PQC Size",
            "Size Ratio",
            "Additional Bytes",
        ],
    )

    st.markdown("---")

    st.subheader("Size Overhead")

    labels = size_comparison["comparison"].tolist()

    classical_values = size_comparison[
        "classical_size_bytes"
    ].tolist()

    pqc_values = size_comparison[
        "pqc_size_bytes"
    ].tolist()

    fig, ax = plt.subplots(figsize=(10, 6))

    x = range(len(labels))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        classical_values,
        width,
        label="Classical",
    )

    ax.bar(
        [i + width / 2 for i in x],
        pqc_values,
        width,
        label="PQC",
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("Size (bytes)")
    ax.set_title("Classical vs PQC Object Sizes")
    ax.legend()

    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        metric_card(
            "ML-KEM Public Key",
            "1,184 B",
            "13.01× ECDH P-256",
        )

        metric_card(
            "ML-KEM Ciphertext",
            "1,088 B",
        )

    with col2:
        metric_card(
            "ML-DSA Signature",
            "3,309 B",
            "45.96× ECDSA P-256",
        )

        metric_card(
            "ECDSA Signature",
            "72 B",
        )


# ============================================================
# THREAT & MIGRATION
# ============================================================

elif section == "Threat & Migration":

    st.header("Threat & Migration Assessment")

    st.subheader("Quantum Threat Mapping")

    threat_table = pd.DataFrame(
        {
            "Mechanism": [
                "RSA-2048",
                "ECDSA-P256",
                "ECDH-P256",
                "AES-256",
                "HKDF-SHA256",
            ],
            "Quantum Algorithm": [
                "Shor's Algorithm",
                "Shor's Algorithm",
                "Shor's Algorithm",
                "Grover's Algorithm",
                "No direct Shor attack",
            ],
            "Status": [
                "Vulnerable",
                "Vulnerable",
                "Vulnerable",
                "Reduced security margin",
                "Retain",
            ],
            "Migration / Action": [
                "ML-KEM-768 / ML-DSA-65",
                "ML-DSA-65",
                "ML-KEM-768",
                "Retain with adequate key size",
                "Retain",
            ],
        }
    )

    markdown_table(threat_table)

    st.markdown("---")

    st.subheader("Migration Decision")

    decisions = pd.DataFrame(
        {
            "Migration": [
                "ECDSA → ML-DSA",
                "ECDH → ML-KEM",
                "RSA-2048",
            ],
            "Priority": [
                "High",
                "High",
                "High",
            ],
            "Primary Consideration": [
                "Signature size and signing overhead",
                "Public-key, ciphertext and workflow overhead",
                "Function-dependent migration",
            ],
        }
    )

    markdown_table(decisions)

    st.markdown("---")

    st.subheader("Migration Principles")

    st.markdown(
        """
**ECDH → ML-KEM**

Used for post-quantum key establishment.

**ECDSA → ML-DSA**

Used for post-quantum digital signatures.

**RSA-2048**

Migration is function-dependent:

- Key establishment / encryption-related functionality → ML-KEM
- Digital-signature functionality → ML-DSA

The measured overheads represent engineering trade-offs that should
be considered during deployment rather than reasons to avoid PQC migration.
"""
    )


# ============================================================
# METHODOLOGY
# ============================================================

elif section == "Methodology":

    st.header("Experimental Methodology")

    st.subheader("Benchmark Design")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Total Observations", "24,000")

    with col2:
        metric_card("Iterations", "1,500 / operation")

    with col3:
        metric_card("Final Algorithms", "5")

    st.markdown(
        """
The benchmark evaluates RSA-2048, ECDSA-P256, ECDH-P256,
ML-KEM-768, and ML-DSA-65.

Measured operations include key generation, encryption/decryption,
signing/verification, shared-secret generation, encapsulation,
and decapsulation.

Cryptographic object sizes were measured separately for public keys,
private keys, signatures, ciphertexts, and shared secrets.
"""
    )

    st.markdown("---")

    st.subheader("Project Documentation")

    st.markdown(
        """
**Detailed methodology**

`methodology/experimental_methodology.md`

**Statistical findings**

`analysis/findings.md`

**PQC migration assessment**

`threat_assessment/pqc_migration_assessment.md`
"""
    )

    st.markdown("---")

    st.subheader("Limitations")

    st.info(
        "The measurements represent the specific implementations, "
        "software environment, and hardware used for this project. "
        "They should be interpreted as experimental engineering "
        "measurements rather than universal performance benchmarks."
    )


# ============================================================
# Footer
# ============================================================

st.markdown("---")

st.caption(
    "Quantum Threat Assessment & Post-Quantum Migration | "
    "RSA-2048 • ECDSA-P256 • ECDH-P256 • ML-KEM-768 • ML-DSA-65"
)