"""
simulate_w_alone.py

Constructs and verifies the |W_Alone> state family for N qubits:

    Base case (m=1):
        |W_Alone> = (1/sqrt(2N)) * sum_{b in {0,1}} sum_{k=1}^{N} |b^N XOR e_k>

    Generalized family (m qubits "alone" instead of 1):
        |W_Alone^(m)> = (1/sqrt(2*C(N,m))) * sum_{b in {0,1}} sum_{|S|=m} |b^N XOR e_S>

This script:
  1. Builds the state vector directly (statevector construction) for any m.
  2. Verifies normalization (sum of squared amplitudes == 1).
  3. Verifies mirror symmetry: X^{⊗N} |W_Alone^(m)> == |W_Alone^(m)>.
  4. Optionally builds the state using Qiskit's Statevector for N = 4, 5, 6 qubits.

Requirements:
    pip install qiskit numpy

Author / Concept: Chutiphong Bunloed (synthesis496)
License: AGPL-3.0 (see LICENSE). Commercial use requires a separate license
(see COMMERCIAL-LICENSE.md).
"""

from itertools import combinations
from math import comb
import numpy as np

try:
    from qiskit.quantum_info import Statevector
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


def bitstring_from_background_and_flip(background_bit: int, flip_index: int, n: int) -> str:
    """
    Build an N-bit string where every bit equals `background_bit`,
    except position `flip_index` (0-indexed) which is flipped.
    """
    bits = [background_bit] * n
    bits[flip_index] = 1 - background_bit
    return "".join(str(b) for b in bits)


def bitstring_from_background_and_subset(background_bit: int, subset, n: int) -> str:
    """
    Build an N-bit string where every bit equals `background_bit`,
    except the positions in `subset` (0-indexed), which are flipped.
    Used for the generalized |W_Alone^(m)> family.
    """
    bits = [background_bit] * n
    for idx in subset:
        bits[idx] = 1 - background_bit
    return "".join(str(b) for b in bits)


def build_w_alone_amplitudes(n: int) -> dict:
    """
    Build the base |W_Alone> state (m=1) as a dict of {bitstring: amplitude}.
    """
    amplitude = 1.0 / np.sqrt(2 * n)
    amplitudes = {}

    for b in (0, 1):
        for k in range(n):  # k = 0 .. N-1 (0-indexed position)
            bitstring = bitstring_from_background_and_flip(b, k, n)
            amplitudes[bitstring] = amplitudes.get(bitstring, 0.0) + amplitude

    return amplitudes


def build_w_alone_m_amplitudes(n: int, m: int) -> dict:
    """
    Build the generalized |W_Alone^(m)> state as a dict of {bitstring: amplitude}.

    m qubits (instead of just 1) stand apart from the background, at every
    possible combination of m positions out of N, mirrored across both
    background choices (b=0, b=1).
    """
    if not (1 <= m <= n - 1):
        raise ValueError("m must satisfy 1 <= m <= N-1")

    num_states = 2 * comb(n, m)
    amplitude = 1.0 / np.sqrt(num_states)
    amplitudes = {}

    for b in (0, 1):
        for subset in combinations(range(n), m):
            bitstring = bitstring_from_background_and_subset(b, subset, n)
            amplitudes[bitstring] = amplitudes.get(bitstring, 0.0) + amplitude

    return amplitudes


def verify_normalization(amplitudes: dict) -> float:
    """Return sum of squared amplitudes (should be ~1.0 for valid state)."""
    return sum(a ** 2 for a in amplitudes.values())


def apply_global_bitflip(amplitudes: dict) -> dict:
    """
    Apply the global bit-flip operator X^{⊗N} to a state given as a dict of
    {bitstring: amplitude}, by flipping every bit in every basis string.
    """
    flipped = {}
    for bitstring, amp in amplitudes.items():
        flipped_bitstring = "".join("1" if c == "0" else "0" for c in bitstring)
        flipped[flipped_bitstring] = flipped.get(flipped_bitstring, 0.0) + amp
    return flipped


def verify_mirror_symmetry(amplitudes: dict, tol: float = 1e-9) -> bool:
    """
    Verify that X^{⊗N} |state> == |state>, i.e. the state is invariant under
    a global bit-flip (mirror reflection between the 0-background and
    1-background families).
    """
    flipped = apply_global_bitflip(amplitudes)
    if set(flipped.keys()) != set(amplitudes.keys()):
        return False
    return all(abs(flipped[k] - amplitudes[k]) < tol for k in amplitudes)


def build_qiskit_statevector(amplitudes: dict, n: int):
    """
    Build a Qiskit Statevector object from a {bitstring: amplitude} dict
    (if qiskit is installed).
    """
    if not QISKIT_AVAILABLE:
        raise ImportError("qiskit is not installed. Run `pip install qiskit` first.")

    dim = 2 ** n
    vec = np.zeros(dim, dtype=complex)

    for bitstring, amp in amplitudes.items():
        # Qiskit's bit ordering: rightmost character = qubit 0 (little-endian)
        index = int(bitstring, 2)
        vec[index] = amp

    return Statevector(vec)


def main():
    print("############################################")
    print("# Base case: |W_Alone> (m = 1)")
    print("############################################")
    for n in (4, 5, 6):
        print(f"\n=== N = {n} qubits ===")
        amplitudes = build_w_alone_amplitudes(n)

        print(f"Number of basis states in superposition: {len(amplitudes)} (expected {2*n})")
        print(f"Amplitude per state: 1/sqrt(2*{n}) = {1/np.sqrt(2*n):.6f}")

        norm = verify_normalization(amplitudes)
        print(f"Sum of squared amplitudes (should be ~1.0): {norm:.10f}")

        mirror_ok = verify_mirror_symmetry(amplitudes)
        print(f"Mirror symmetry X^(N)|W_Alone> == |W_Alone>: {mirror_ok}")

        print("Basis states (b=0 family - one '1'):")
        for bs in sorted(k for k, v in amplitudes.items() if k.count('1') == 1):
            print(f"  |{bs}>")

        print("Basis states (b=1 family - one '0'):")
        for bs in sorted(k for k, v in amplitudes.items() if k.count('0') == 1):
            print(f"  |{bs}>")

        if QISKIT_AVAILABLE:
            sv = build_qiskit_statevector(amplitudes, n)
            qiskit_norm = np.sum(np.abs(sv.data) ** 2)
            print(f"Qiskit Statevector norm check: {qiskit_norm:.10f}")
        else:
            print("(Qiskit not installed - skipping Statevector construction. "
                  "Run `pip install qiskit` to enable this check.)")

    print("\n\n############################################")
    print("# Generalized family: |W_Alone^(m)> for m > 1")
    print("############################################")
    for n in (6, 8, 10):
        print(f"\n=== N = {n} qubits ===")
        for m in range(1, n):
            amplitudes_m = build_w_alone_m_amplitudes(n, m)
            expected_states = 2 * comb(n, m)
            norm = verify_normalization(amplitudes_m)
            mirror_ok = verify_mirror_symmetry(amplitudes_m)
            print(
                f"  m={m}: states={len(amplitudes_m):>4} (expected {expected_states:>4}), "
                f"norm={norm:.10f}, mirror_symmetric={mirror_ok}"
            )


if __name__ == "__main__":
    main()
