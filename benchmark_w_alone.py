"""
benchmark_w_alone.py

Empirical comparison between the standard |W> state and the |W_Alone> state,
addressing the open questions raised in Section 6/7 of the preprint
(paper/w_alone_preprint.md):

  1. Entanglement entropy (single-qubit reduced density matrix, von Neumann
     entropy) for both states.
  2. Fidelity under a simple depolarizing-noise channel, sweeping the noise
     probability.
  3. Robustness to qubit loss: fidelity of the reduced state after tracing
     out one qubit, compared against the "ideal" reduced state with no loss.

This script produces numbers that can be inserted into Section 6 of the
preprint once results are validated. All results printed here are RAW
EMPIRICAL DATA -- interpretation / claims should be added to the paper only
after review.

Requirements:
    pip install qiskit qiskit-aer numpy

Author / Concept: Chutiphong Bunloed (synthesis496)
License: AGPL-3.0 (see LICENSE). Commercial use requires a separate license
(see COMMERCIAL-LICENSE.md).
"""

import numpy as np

try:
    from qiskit.quantum_info import (
        Statevector,
        DensityMatrix,
        partial_trace,
        entropy,
        state_fidelity,
    )
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


# ---------------------------------------------------------------------------
# State construction
# ---------------------------------------------------------------------------

def build_standard_w_statevector(n: int):
    """Standard |W> state: one '1' among otherwise all-'0' qubits."""
    dim = 2 ** n
    vec = np.zeros(dim, dtype=complex)
    amp = 1.0 / np.sqrt(n)
    for k in range(n):
        bits = ["0"] * n
        bits[k] = "1"
        bitstring = "".join(bits)
        index = int(bitstring, 2)  # little-endian (Qiskit convention)
        vec[index] = amp
    return Statevector(vec)


def build_w_alone_statevector(n: int):
    """|W_Alone> state: mirror-symmetric superposition (b=0 and b=1 families)."""
    dim = 2 ** n
    vec = np.zeros(dim, dtype=complex)
    amp = 1.0 / np.sqrt(2 * n)
    for b in (0, 1):
        for k in range(n):
            bits = [str(b)] * n
            bits[k] = str(1 - b)
            bitstring = "".join(bits)
            index = int(bitstring, 2)
            vec[index] += amp
    return Statevector(vec)


# ---------------------------------------------------------------------------
# Metric 1: Entanglement entropy (single-qubit reduced state)
# ---------------------------------------------------------------------------

def single_qubit_entanglement_entropy(sv: "Statevector", n: int, qubit: int = 0) -> float:
    """
    Von Neumann entropy (base 2) of the reduced density matrix obtained by
    tracing out all qubits except `qubit`. For a pure global state, this
    equals the entanglement entropy between that qubit and the rest.
    """
    trace_out = [i for i in range(n) if i != qubit]
    rho = partial_trace(sv, trace_out)
    return float(entropy(rho, base=2))


# ---------------------------------------------------------------------------
# Metric 2: Fidelity under depolarizing noise
# ---------------------------------------------------------------------------

def depolarize_density_matrix(rho: "DensityMatrix", p: float) -> "DensityMatrix":
    """
    Apply a global depolarizing channel with probability `p`:
        rho -> (1-p) * rho + p * I/dim
    This is a simplified, basis-independent noise model (not a full Kraus
    per-qubit channel), used here as a first-pass robustness probe.
    """
    dim = rho.dim
    identity_mixed = np.eye(dim, dtype=complex) / dim
    noisy = (1 - p) * rho.data + p * identity_mixed
    return DensityMatrix(noisy)


def fidelity_under_depolarizing(sv: "Statevector", probs) -> dict:
    """Return {p: fidelity(rho_noisy, rho_ideal)} for each p in `probs`."""
    rho_ideal = DensityMatrix(sv)
    results = {}
    for p in probs:
        rho_noisy = depolarize_density_matrix(rho_ideal, p)
        results[p] = float(state_fidelity(rho_ideal, rho_noisy))
    return results


# ---------------------------------------------------------------------------
# Metric 3: Robustness to qubit loss
# ---------------------------------------------------------------------------

def qubit_loss_fidelity(sv: "Statevector", n: int, num_lost: int = 1) -> float:
    """
    Simulate losing `num_lost` qubits (traced out / discarded) and compare
    the resulting mixed state's purity via fidelity with itself as a proxy
    for "how mixed" the remaining state becomes. Returns the purity
    Tr(rho^2) of the reduced density matrix on the remaining qubits -- 1.0
    means still pure (no information loss), lower means more mixed
    (more sensitive to qubit loss).
    """
    lost_qubits = list(range(num_lost))
    remaining_rho = partial_trace(sv, lost_qubits)
    purity = float(np.real(np.trace(remaining_rho.data @ remaining_rho.data)))
    return purity


# ---------------------------------------------------------------------------
# Main benchmark runner
# ---------------------------------------------------------------------------

def run_benchmark(n: int):
    print(f"\n=== N = {n} qubits ===")

    sv_w = build_standard_w_statevector(n)
    sv_walone = build_w_alone_statevector(n)

    # Sanity checks
    print(f"|W> norm: {np.sum(np.abs(sv_w.data)**2):.10f}")
    print(f"|W_Alone> norm: {np.sum(np.abs(sv_walone.data)**2):.10f}")

    # --- Metric 1: entanglement entropy ---
    ent_w = single_qubit_entanglement_entropy(sv_w, n)
    ent_walone = single_qubit_entanglement_entropy(sv_walone, n)
    print(f"\n[Entanglement entropy, single-qubit reduced state, base-2]")
    print(f"  |W>       : {ent_w:.6f} bits")
    print(f"  |W_Alone> : {ent_walone:.6f} bits")

    # --- Metric 2: fidelity under depolarizing noise ---
    probs = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]
    fid_w = fidelity_under_depolarizing(sv_w, probs)
    fid_walone = fidelity_under_depolarizing(sv_walone, probs)
    print(f"\n[Fidelity under global depolarizing noise]")
    print(f"  {'p':>6} | {'F(|W>)':>10} | {'F(|W_Alone>)':>14}")
    for p in probs:
        print(f"  {p:>6.2f} | {fid_w[p]:>10.6f} | {fid_walone[p]:>14.6f}")

    # --- Metric 3: robustness to qubit loss (purity of remaining state) ---
    purity_w = qubit_loss_fidelity(sv_w, n, num_lost=1)
    purity_walone = qubit_loss_fidelity(sv_walone, n, num_lost=1)
    print(f"\n[Purity Tr(rho^2) of remaining (N-1)-qubit state after losing 1 qubit]")
    print(f"  |W>       : {purity_w:.6f}")
    print(f"  |W_Alone> : {purity_walone:.6f}")
    print("  (1.0 = still pure / no information loss, lower = more mixed)")


def main():
    if not QISKIT_AVAILABLE:
        print("qiskit is required for this benchmark. Run `pip install qiskit`.")
        return

    print("############################################")
    print("# Benchmark: |W> vs |W_Alone>")
    print("# Raw empirical data -- see paper/w_alone_preprint.md Section 6")
    print("# for context on what these numbers do/do not establish.")
    print("############################################")

    for n in (4, 5, 6, 8):
        run_benchmark(n)


if __name__ == "__main__":
    main()
