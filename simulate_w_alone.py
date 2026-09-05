"""
simulate_w_alone.py

Constructs and verifies the |W_Alone> state for N qubits:

    |W_Alone> = (1/sqrt(2N)) * sum_{b in {0,1}} sum_{k=1}^{N} |b^N XOR e_k>

This script:
  1. Builds the state vector directly (statevector construction).
  2. Verifies normalization (sum of squared amplitudes == 1).
  3. Optionally builds the state using Qiskit's Statevector / QuantumCircuit
     initialization for N = 4, 5, 6 qubits.

Requirements:
    pip install qiskit numpy

Author / Concept: synthesis496
License: AGPL-3.0 (see LICENSE). Commercial use requires a separate license
(see COMMERCIAL-LICENSE.md).
"""

from itertools import product
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


def build_w_alone_amplitudes(n: int) -> dict:
    """
    Build the |W_Alone> state as a dict of {bitstring: amplitude}.
    Returns a dictionary mapping computational basis bitstrings to their
    (real) amplitude 1/sqrt(2N).
    """
    amplitude = 1.0 / np.sqrt(2 * n)
    amplitudes = {}

    for b in (0, 1):
        for k in range(n):  # k = 0 .. N-1 (0-indexed position)
            bitstring = bitstring_from_background_and_flip(b, k, n)
            # Each basis state should be unique; if collisions occur, amplitudes add.
            amplitudes[bitstring] = amplitudes.get(bitstring, 0.0) + amplitude

    return amplitudes


def verify_normalization(amplitudes: dict) -> float:
    """Return sum of squared amplitudes (should be ~1.0 for valid state)."""
    return sum(a ** 2 for a in amplitudes.values())


def build_qiskit_statevector(n: int):
    """
    Build the |W_Alone> state as a Qiskit Statevector object (if qiskit is installed).
    """
    if not QISKIT_AVAILABLE:
        raise ImportError("qiskit is not installed. Run `pip install qiskit` first.")

    amplitudes = build_w_alone_amplitudes(n)
    dim = 2 ** n
    vec = np.zeros(dim, dtype=complex)

    for bitstring, amp in amplitudes.items():
        # Qiskit's bit ordering: rightmost character = qubit 0 (little-endian)
        index = int(bitstring, 2)
        vec[index] = amp

    sv = Statevector(vec)
    return sv


def main():
    for n in (4, 5, 6):
        print(f"\n=== N = {n} qubits ===")
        amplitudes = build_w_alone_amplitudes(n)

        print(f"Number of basis states in superposition: {len(amplitudes)} (expected {2*n})")
        print(f"Amplitude per state: 1/sqrt(2*{n}) = {1/np.sqrt(2*n):.6f}")

        norm = verify_normalization(amplitudes)
        print(f"Sum of squared amplitudes (should be ~1.0): {norm:.10f}")

        print("Basis states (b=0 family - one '1'):")
        for bs in sorted(k for k, v in amplitudes.items() if k.count('1') == 1):
            print(f"  |{bs}>")

        print("Basis states (b=1 family - one '0'):")
        for bs in sorted(k for k, v in amplitudes.items() if k.count('0') == 1):
            print(f"  |{bs}>")

        if QISKIT_AVAILABLE:
            sv = build_qiskit_statevector(n)
            qiskit_norm = np.sum(np.abs(sv.data) ** 2)
            print(f"Qiskit Statevector norm check: {qiskit_norm:.10f}")
        else:
            print("(Qiskit not installed - skipping Statevector construction. "
                  "Run `pip install qiskit` to enable this check.)")


if __name__ == "__main__":
    main()
