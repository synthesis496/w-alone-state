> 🚨 **Notice: This project is under active development.** Sections marked
> `🔬 [DRAFT / TO BE VALIDATED]` describe hypotheses or proposed use-cases that
> have not yet been empirically benchmarked. See the [Roadmap](#-roadmap) for
> current status. Contributions and rigorous scrutiny are welcome.

# ✨ |W_Alone⟩ — The Alone State

### A Symmetric, Nature-Inspired Extension of the Quantum W-State

**Author / Concept by:** Chutiphong Bunloed ([@synthesis496](https://github.com/synthesis496))
**License:** AGPL-3.0 — free for open research, commercial license available (see [COMMERCIAL-LICENSE.md](./COMMERCIAL-LICENSE.md))

---

## 🌱 Origin: Inspired by Nature, Not by Engineering

Most quantum states are designed top-down — start with an engineering goal,
then derive the math. `|W_Alone⟩` was born the opposite way: from observing a
pattern that repeats constantly in nature —

> **"Left undisturbed, nature always restores its own balance."**

Look around any natural system with many identical members (a flock, a
crystal lattice, a colony of cells, a field of spins): sooner or later, **one
element stands apart** from the rest — a mutation, a defect, an outlier — and
this happens **symmetrically**, regardless of whether the "baseline" state of
the system is what we'd label `0` or `1`. Nature does not care which label we
call "normal." Solitude (aloneness) emerges from *either* side of the
baseline, with equal likelihood.

`|W_Alone⟩` encodes exactly this symmetry into a single quantum state: one
qubit "alone," standing out from an otherwise uniform background — where the
background itself can be all-`0`s **or** all-`1`s, both superposed together
with equal weight.

This repository takes that natural observation and grounds it rigorously in
the mathematics of quantum information theory.

---

## 📐 The Equation

$$|W_{Alone}\rangle = \frac{1}{\sqrt{2N}} \sum_{b\in\{0,1\}}\sum_{k=1}^{N} |\mathbf{b}^{\otimes N}\oplus \mathbf{e}_k\rangle$$

| Symbol | Meaning |
|---|---|
| **N** | Number of qubits in the system |
| **b ∈ {0, 1}** | Background polarity switch — selects the "all-zero" world or the "all-one" world |
| **b^⊗N** | The uniform background basis state (`0000...0` or `1111...1`) |
| **e_k** | Unit vector with a `1` at position `k`, used as an XOR mask |
| **⊕ e_k** | Flips the bit at position `k` to be the opposite of the background — creating the "alone" bit |
| **Σ_{k=1}^{N}** | Cyclic permutation — the alone position sweeps through all N qubits |
| **1/√(2N)** | Normalization constant across the full `2N`-dimensional superposition |

### Intuition

- **b = 0** → standard W-state family: exactly one `1` among all `0`s, cycling through N positions.
- **b = 1** → the mirror family: exactly one `0` among all `1`s (bitwise NOT of the above).
- Both families combined with equal amplitude → a state that is **symmetric under global bit-flip**, meaning it doesn't matter which value you call the "background" — the aloneness pattern is preserved either way.

---

## 🪞 Mirror Symmetry (Formal Proof)

The deepest structural property of `|W_Alone⟩` is that it is a **complete
mirror-reflection state**: swapping the roles of `0` and `1` everywhere in
the system leaves the state completely unchanged. This is not a metaphor —
it is a provable algebraic invariance.

Let `X^{⊗N}` be the global bit-flip (NOT) operator applied to all N qubits.
Applying it to any basis state in the superposition:

$$X^{\otimes N}\,|\mathbf{b}^{\otimes N}\oplus \mathbf{e}_k\rangle = |\overline{\mathbf{b}}^{\otimes N}\oplus \mathbf{e}_k\rangle$$

where `b̄ = 1 - b` is the opposite background. Since the outer sum already
runs over **both** `b = 0` and `b = 1` with **identical amplitude**
`1/√(2N)`, flipping every qubit simply **permutes the b=0 family into the
b=1 family and vice versa** — the set of terms in the superposition is
unchanged, only reordered. Therefore:

$$X^{\otimes N}\,|W_{Alone}\rangle = |W_{Alone}\rangle$$

**`|W_Alone⟩` is a fixed point (eigenstate with eigenvalue +1) of the global
bit-flip operator.** This is the rigorous form of "the state and its mirror
reflection are the same state" — a perfect, self-contained symmetry that the
standard W-state does **not** possess (a standard `|W⟩` is *not* invariant
under `X^{⊗N}`, since it only ever contains the "one `1`" family).

This mirror-invariance is verified numerically in
[`simulate_w_alone.py`](./simulate_w_alone.py).

---

## 📊 Expansion Table (N = 4, 5, 6)

| N | Normalization | b=0 states (one `1`) | b=1 states (one `0`) |
|---|---|---|---|
| 4 | 1/√8  | 1000, 0100, 0010, 0001 | 0111, 1011, 1101, 1110 |
| 5 | 1/√10 | 10000, 01000, 00100, 00010, 00001 | 01111, 10111, 11011, 11101, 11110 |
| 6 | 1/√12 | 100000, 010000, 001000, 000100, 000010, 000001 | 011111, 101111, 110111, 111011, 111101, 111110 |

Each row confirms: total basis states = `2N`, each with amplitude `1/√(2N)`,
so the sum of squared amplitudes = `2N × (1/2N) = 1` ✅ (properly normalized).

### Proof of Normalization (general N)

- Number of basis states: `2N` (N from `b=0`, N from `b=1`, all distinct — a
  string with exactly one `1` can never equal a string with exactly one `0`
  for `N ≥ 1`).
- Each amplitude: `1/√(2N)`.
- Sum of squared amplitudes: `2N × (1/√(2N))² = 2N × 1/(2N) = 1` ✅

The state is correctly normalized for any `N ≥ 1`. Verified computationally
in [`simulate_w_alone.py`](./simulate_w_alone.py).

---

## 🌌 Generalized Family: `|W_Alone^(m)⟩` `[DRAFT / TO BE VALIDATED]`

The single-alone case (`m = 1`) is just one member of a much larger family.
Instead of exactly **one** qubit standing apart from the background, let
**m qubits** stand apart together, at any of the `C(N, m)` possible
positions — while keeping the same mirror-reflection principle intact
(the group of "different" qubits can itself be `1`s-among-`0`s **or**
`0`s-among-`1`s, with equal weight).

$$|W_{Alone}^{(m)}\rangle = \frac{1}{\sqrt{2\binom{N}{m}}} \sum_{b\in\{0,1\}}\sum_{|S|=m} |\mathbf{b}^{\otimes N}\oplus \mathbf{e}_S\rangle$$

Where `S` ranges over all subsets of `{1, ..., N}` of size `m`, and `e_S` is
the indicator vector that is `1` on exactly the positions in `S`. The
original `|W_Alone⟩` is the special case `m = 1`.

**Why this matters — combinatorial growth:**
Because the number of basis states is `2·C(N, m)` instead of `2N`, the
dimension of the superposition **grows combinatorially with m** instead of
linearly — the same mirror-symmetric structure, but spanning a vastly larger
subspace.

| N | m=1 states | m=2 states | m=3 states |
|---|---|---|---|
| 6 | 12 | 30 | 40 |
| 8 | 16 | 56 | 112 |
| 10 | 20 | 90 | 240 |

**Mirror symmetry is preserved for every m:**

$$X^{\otimes N}\,|W_{Alone}^{(m)}\rangle = |W_{Alone}^{(m)}\rangle$$

This holds by the same argument as the `m = 1` case: flipping all qubits
swaps the "m-ones-among-zeros" family with the "m-zeros-among-ones" family,
and since both are already summed with equal amplitude, the overall state is
unchanged.

**Status:** this generalization is a natural — but so far untested —
extension of the core `|W_Alone⟩` idea. It has not yet been benchmarked
computationally beyond the small-N sanity checks above. See the
[Roadmap](#-roadmap) for validation plans.

---

## 🔬 Proposed Use-Cases `[DRAFT / TO BE VALIDATED]`

These are **hypotheses to be tested**, not yet proven advantages. They are
listed here to guide the next phase of research (see [Roadmap](#-roadmap)).

1. **Reference-frame-independent anomaly detection** — a sensor network
   where you don't know in advance whether "normal" reads as `0` or `1`.
   `|W_Alone⟩` naturally represents "one anomalous unit" regardless of which
   convention is baseline.
2. **Symmetric single-defect encoding** — quantum error models where a defect
   could manifest as either a bit-flip *to* `1` or *away from* `1`, and the
   encoding should be invariant to that choice.
3. **Entanglement robustness comparison** — testing whether `|W_Alone⟩`'s
   dual-background structure offers different resilience to qubit loss or
   dephasing noise compared to a standard W-state, when traced out to fewer
   qubits.
4. **Multi-defect / cluster anomaly encoding** (via `|W_Alone^(m)⟩`) — modeling
   scenarios where a *group* of m units deviates together from the
   background, rather than a single unit, while retaining full 0↔1 mirror
   symmetry.

**None of these have been benchmarked yet.** The next milestone (see Roadmap)
is running fidelity, entanglement entropy, and noise-robustness comparisons
against a standard `|W⟩` state using Qiskit Aer, so these claims can be
confirmed, refined, or discarded based on data.

---

## 💻 Simulation & Verification

See [`simulate_w_alone.py`](./simulate_w_alone.py) — constructs `|W_Alone⟩`
for N = 4, 5, 6 qubits, verifies normalization and mirror-symmetry
(`X^{⊗N}|W_Alone⟩ = |W_Alone⟩`) computationally, and also builds the
generalized `|W_Alone^(m)⟩` family for arbitrary `m` (with optional Qiskit
`Statevector` cross-check).

```bash
pip install numpy qiskit
python simulate_w_alone.py
```

---

## 🗺️ Roadmap

- [x] Formalize the `|W_Alone⟩` equation and prove normalization
- [x] Tabulate explicit basis states for N = 4, 5, 6
- [x] Reference implementation + normalization check (Qiskit/NumPy)
- [x] Formal proof + numerical verification of mirror symmetry (`X^{⊗N}` invariance)
- [x] Define and numerically verify the generalized `|W_Alone^(m)⟩` family
- [ ] Benchmark fidelity / entanglement entropy vs. standard W-state
- [ ] Benchmark robustness to qubit loss and dephasing noise
- [ ] Run on real quantum hardware (IBM Quantum free tier)
- [ ] Publish formal write-up (arXiv preprint)
- [ ] Community review (Qiskit / PennyLane forums, r/QuantumComputing)

Contributions, critiques, and rigorous testing are welcome — open an Issue
or PR.

---

## 📜 License

This work is licensed under **AGPL-3.0**. See [LICENSE](./LICENSE).

For commercial / closed-source use, see [COMMERCIAL-LICENSE.md](./COMMERCIAL-LICENSE.md).

---

*Concept, equation, and natural-motivation framing are original work by
Chutiphong Bunloed ([@synthesis496](https://github.com/synthesis496)).
Contributions to formal benchmarking and validation are credited in commit
history.*
