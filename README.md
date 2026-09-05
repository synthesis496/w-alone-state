# |W_Alone⟩ — W-space Equation (Extended W-State)

**Author / Concept by:** synthesis496
**License:** AGPL-3.0 (with optional Commercial License — see [COMMERCIAL-LICENSE.md](./COMMERCIAL-LICENSE.md))

## Overview

This repository documents an original theoretical concept: a **single unified equation**
that extends the standard quantum **W-state** into a symmetric, two-perspective
formulation called **`|W_Alone⟩`**.

The core idea is to combine:

1. The **original W-state** — a superposition where exactly *one* qubit is `1`
   and the rest are `0`, cyclically permuted across all qubit positions.
2. Its **complement (mirror/reflection)** — a superposition where exactly *one*
   qubit is `0` and the rest are `1`.

into a single normalized quantum state, representing a *"two-sided symmetric
viewpoint"* of the same underlying structure.

## The Equation

$$|W_{Alone}\rangle = \frac{1}{\sqrt{2N}} \sum_{b\in\{0,1\}}\sum_{k=1}^{N} |\mathbf{b}^{\otimes N}\oplus \mathbf{e}_k\rangle$$

Where:

- **N** — number of qubits in the system.
- **b ∈ {0, 1}** — a background/polarity switch variable. Selects between the
  "all-zero" background (`b=0`) and the "all-one" background (`b=1`).
- **b^⊗N** — the background basis state where every qubit shares the same value
  (e.g. `0000` or `1111`).
- **e_k** — the standard basis (unit) vector with a `1` at position `k`. Used
  here as an XOR mask.
- **⊕ e_k** — XOR operation at position `k`, flipping the bit at position `k`
  to be the *opposite* of the background — creating a single "lonely" (alone) bit.
- **Σ_{k=1}^{N}** — cyclic permutation: the "lonely" bit position sweeps across
  all N positions in the system.
- **1/√(2N)** — normalization constant. Since there are `2N` total basis states
  in the superposition (N states from `b=0`, N states from `b=1`), each with equal
  amplitude, the normalization factor is `1/√(2N)` (compared to `1/√N` for a
  standard single-sided W-state).

## Intuition

- When **b = 0**: the term `0^⊗N ⊕ e_k` generates the standard W-state family —
  basis states with exactly **one `1`** cycling through all N positions.
- When **b = 1**: the term `1^⊗N ⊕ e_k` performs a bitwise NOT, generating the
  complementary family — basis states with exactly **one `0`** (all other bits `1`)
  cycling through all N positions.
- The two families are combined with equal amplitude, producing a state that is
  symmetric under bit-flip (NOT) — i.e., invariant in structure whether you view
  it from the "mostly 0s" or "mostly 1s" perspective.

## Expansion Table (N = 4, 5, 6)

| N | Normalization | b=0 states (one `1`) | b=1 states (one `0`) |
|---|---|---|---|
| 4 | 1/√8  | 1000, 0100, 0010, 0001 | 0111, 1011, 1101, 1110 |
| 5 | 1/√10 | 10000, 01000, 00100, 00010, 00001 | 01111, 10111, 11011, 11101, 11110 |
| 6 | 1/√12 | 100000, 010000, 001000, 000100, 000010, 000001 | 011111, 101111, 110111, 111011, 111101, 111110 |

Each row confirms: total number of basis states = `2N`, each with amplitude
`1/√(2N)`, so the sum of squared amplitudes = `2N × (1/2N) = 1` ✅ (properly normalized).

## Verifying Normalization

For general N:

- Number of basis states in superposition: `2N` (N from b=0, N from b=1, all distinct
  since a string with exactly one `1` can never equal a string with exactly one `0`
  for N ≥ 1).
- Each amplitude: `1/√(2N)`.
- Sum of squared amplitudes: `2N × (1/√(2N))² = 2N × 1/(2N) = 1`.

✅ The state is correctly normalized for any N ≥ 1.

## Simulation

See [`simulate_w_alone.py`](./simulate_w_alone.py) for a Qiskit-based construction
and verification of `|W_Alone⟩` for N = 4, 5, 6 qubits.

## License

This work is licensed under **AGPL-3.0**. See [LICENSE](./LICENSE).

For commercial / closed-source use, see [COMMERCIAL-LICENSE.md](./COMMERCIAL-LICENSE.md).
