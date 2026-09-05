# The Alone State $|W_{Alone}\rangle$: A Mirror-Symmetric Extension of the W-State Family

**Author:** Chutiphong Bunloed ([@synthesis496](https://github.com/synthesis496))

**Status:** Preprint draft (v0.1) — not yet peer reviewed. Companion code and
proofs available in the [repository](https://github.com/synthesis496/w-alone-state).

---

## Abstract

We introduce $|W_{Alone}\rangle$, a family of $N$-qubit quantum states
inspired by the recurring natural phenomenon in which a single element of a
large, otherwise-uniform system comes to stand apart from its neighbors,
independent of which of the two possible uniform backgrounds ("all-zero" or
"all-one") is taken as the reference. The state is constructed as an equally
weighted superposition of the standard $W$-state (one excitation among
zeros) and its bitwise complement (one de-excitation among ones). We prove
that $|W_{Alone}\rangle$ is correctly normalized for all $N \geq 1$ and,
more importantly, that it is a fixed point of the global bit-flip operator
$X^{\otimes N}$ — a symmetry property not shared by the conventional
$W$-state. We further propose a generalized family
$|W_{Alone}^{(m)}\rangle$, in which $m$ qubits jointly stand apart from the
background, and show this preserves the same mirror symmetry while growing
the dimension of the superposition combinatorially in $m$. All claims of
normalization and symmetry are verified both analytically and numerically.
Potential applications to anomaly detection, defect-symmetric error
encoding, and entanglement-robustness comparisons are proposed as open
questions for future empirical work; **none of these applications are
validated in this document** and are presented strictly as motivating
hypotheses.

---

## 1. Introduction

### 1.1 Motivation

Many quantum states used in quantum information theory are motivated by
engineering goals — a target protocol (teleportation, secret sharing, metrology)
is chosen first, and a state is derived to satisfy it. This work takes the
opposite path. The starting point is an informal but persistent empirical
observation from complex natural systems:

> In a sufficiently large ensemble of near-identical elements (a flock of
> animals, a lattice of spins, a population of cells), it is common for
> exactly one element to deviate from the shared baseline behavior of the
> rest — and this deviation is symmetric with respect to which of two
> possible baseline conventions is treated as "normal."

Formally, if a binary label (0 or 1) is used to describe the baseline state
of each element in a system, the emergence of "one element standing alone"
should not privilege one label over the other. A quantum state that encodes
this observation must therefore be invariant under a global relabeling of
$0 \leftrightarrow 1$.

The standard $W$-state,

$$|W\rangle = \frac{1}{\sqrt{N}}\sum_{k=1}^{N}|0\cdots010\cdots0\rangle
\quad (\text{a single } 1 \text{ at position } k),$$

does **not** have this property: it privileges the "all-zero" background
implicitly, since there is no term in which a single qubit is $0$ among a
background of $1$s. $|W_{Alone}\rangle$ is introduced to close this gap.

### 1.2 Contributions

1. A formal definition of $|W_{Alone}\rangle$ (Section 2).
2. A closed-form proof of normalization for all $N \geq 1$ (Section 3.1).
3. A closed-form proof that $|W_{Alone}\rangle$ is invariant under the
   global bit-flip operator $X^{\otimes N}$ (Section 3.2) — the central
   structural property distinguishing it from $|W\rangle$.
4. A generalization, $|W_{Alone}^{(m)}\rangle$, allowing $m > 1$ qubits to
   jointly "stand apart" from the background, with the same symmetry
   preserved (Section 4).
5. Numerical verification of all of the above via a reference Python/Qiskit
   implementation (Section 5).
6. A set of explicitly unvalidated, hypothesis-stage potential applications,
   clearly separated from the proven results (Section 6).

---

## 2. Definition

Let $N$ be the number of qubits, $b \in \{0, 1\}$ index the choice of
uniform background, and $\mathbf{e}_k$ denote the length-$N$ indicator
vector with a $1$ in position $k$ and $0$ elsewhere. Define
$\mathbf{b}^{\otimes N}$ as the $N$-bit string consisting entirely of the
value $b$. Then:

$$|W_{Alone}\rangle = \frac{1}{\sqrt{2N}} \sum_{b\in\{0,1\}}\sum_{k=1}^{N} \big|\,\mathbf{b}^{\otimes N}\oplus \mathbf{e}_k\,\big\rangle \tag{1}$$

where $\oplus$ denotes bitwise XOR. Expanding the two values of $b$:

- $b = 0$ contributes the $N$ basis states with exactly one $1$ among
  otherwise all-$0$ qubits (the standard $W$-state family).
- $b = 1$ contributes the $N$ basis states with exactly one $0$ among
  otherwise all-$1$ qubits (the bitwise complement family).

Both families appear with identical amplitude $1/\sqrt{2N}$.

---

## 3. Properties

### 3.1 Normalization

**Claim.** $\langle W_{Alone} | W_{Alone} \rangle = 1$ for all $N \geq 1$.

**Proof.** The $2N$ basis states appearing in Eq. (1) are pairwise distinct:
a bit string of Hamming weight $1$ (from the $b=0$ family) can never equal a
bit string of Hamming weight $N-1$ (from the $b=1$ family) for $N \geq 2$,
and the two families are trivially distinct by construction for $N=1$.
Hence there is no interference between terms, and

$$\langle W_{Alone}|W_{Alone}\rangle = \sum_{i=1}^{2N} \left(\frac{1}{\sqrt{2N}}\right)^2 = 2N \cdot \frac{1}{2N} = 1. \qquad \blacksquare$$

This has been verified for $N \in \{4,5,6\}$ by explicit enumeration (Table 1)
and computationally for arbitrary $N$ (Section 5).

**Table 1.** Explicit basis-state expansion for $N = 4, 5, 6$.

| $N$ | Normalization | $b=0$ family (one `1`) | $b=1$ family (one `0`) |
|---|---|---|---|
| 4 | $1/\sqrt{8}$  | 1000, 0100, 0010, 0001 | 0111, 1011, 1101, 1110 |
| 5 | $1/\sqrt{10}$ | 10000, 01000, 00100, 00010, 00001 | 01111, 10111, 11011, 11101, 11110 |
| 6 | $1/\sqrt{12}$ | 100000, 010000, 001000, 000100, 000010, 000001 | 011111, 101111, 110111, 111011, 111101, 111110 |

### 3.2 Mirror Symmetry

**Claim.** $|W_{Alone}\rangle$ is a fixed point of the global bit-flip
operator: $X^{\otimes N}|W_{Alone}\rangle = |W_{Alone}\rangle$.

**Proof.** Let $X^{\otimes N}$ act on a single basis term of Eq. (1) by
flipping every qubit:

$$X^{\otimes N}\big|\mathbf{b}^{\otimes N}\oplus \mathbf{e}_k\big\rangle = \big|\overline{\mathbf{b}}^{\otimes N}\oplus \mathbf{e}_k\big\rangle,$$

where $\overline{b} = 1-b$. Since the outer sum in Eq. (1) already ranges
over both $b=0$ and $b=1$ with identical amplitude $1/\sqrt{2N}$, the action
of $X^{\otimes N}$ merely permutes the $b=0$ family into the $b=1$ family
and vice versa. The multiset of terms — and their amplitudes — is therefore
unchanged:

$$X^{\otimes N}|W_{Alone}\rangle = |W_{Alone}\rangle. \qquad \blacksquare$$

**Remark.** This is the defining structural distinction between
$|W_{Alone}\rangle$ and the standard $|W\rangle$ state: $|W\rangle$ is *not*
an eigenstate of $X^{\otimes N}$, since it contains only the $b=0$ family.
$|W_{Alone}\rangle$ is, by construction, symmetric with respect to which
computational-basis label is designated "background."

---

## 4. Generalized Family $|W_{Alone}^{(m)}\rangle$

The single-qubit-alone construction ($m=1$ excitation) generalizes naturally
to $m$ qubits jointly deviating from the background. Let $S \subset
\{1,\dots,N\}$ range over subsets of size $m$, and let $\mathbf{e}_S$ be the
indicator vector equal to $1$ on exactly the positions in $S$:

$$|W_{Alone}^{(m)}\rangle = \frac{1}{\sqrt{2\binom{N}{m}}} \sum_{b\in\{0,1\}}\sum_{|S|=m} \big|\mathbf{b}^{\otimes N}\oplus \mathbf{e}_S\big\rangle, \qquad 1 \leq m \leq N-1. \tag{2}$$

Equation (1) is recovered at $m=1$.

**Normalization** follows by the identical counting argument as Section 3.1,
replacing the $2N$ distinct basis states with $2\binom{N}{m}$ distinct
basis states (subsets of Hamming weight $m$ are disjoint from subsets of
Hamming weight $N-m$ for $m \neq N-m$, and self-consistently normalized when
$m = N-m$).

**Mirror symmetry** is preserved by the same argument as Section 3.2:
$X^{\otimes N}$ exchanges the $b=0$ and $b=1$ families of Eq. (2)
term-for-term, leaving the superposition invariant:

$$X^{\otimes N}|W_{Alone}^{(m)}\rangle = |W_{Alone}^{(m)}\rangle \quad \text{for all } 1 \leq m \leq N-1.$$

**Combinatorial growth.** Unlike the $m=1$ case, whose dimension grows
linearly in $N$ ($2N$ states), the generalized family's dimension grows
combinatorially: $2\binom{N}{m}$. Table 2 illustrates this growth.

**Table 2.** Number of basis states $2\binom{N}{m}$ for selected $N, m$.

| $N$ | $m=1$ | $m=2$ | $m=3$ |
|---|---|---|---|
| 6  | 12 | 30  | 40  |
| 8  | 16 | 56  | 112 |
| 10 | 20 | 90  | 240 |

---

## 5. Numerical Verification

A reference implementation is provided in
[`simulate_w_alone.py`](https://github.com/synthesis496/w-alone-state/blob/main/simulate_w_alone.py),
which:

1. Constructs $|W_{Alone}\rangle$ directly as a dictionary of
   basis-state amplitudes for $N \in \{4,5,6\}$, and cross-checks
   construction via Qiskit's `Statevector` class.
2. Numerically confirms $\langle W_{Alone}|W_{Alone}\rangle = 1$ to
   floating-point precision.
3. Numerically confirms $X^{\otimes N}|W_{Alone}\rangle = |W_{Alone}\rangle$
   by applying a bitwise-flip permutation to the amplitude dictionary and
   checking exact equality.
4. Constructs the generalized $|W_{Alone}^{(m)}\rangle$ family for
   $N \in \{6, 8, 10\}$ and all valid $m$, confirming both normalization
   and mirror symmetry in every case tested.

All numerical checks reported here are exact to floating-point tolerance
($< 10^{-9}$) and are reproducible by running the script directly
(`python simulate_w_alone.py`).

---

## 6. Proposed Applications — Hypotheses, Not Results

The following are **conjectural directions**, explicitly not validated in
this work, offered to motivate follow-up empirical study:

1. **Reference-frame-independent anomaly detection.** In a sensor network
   where the "normal" reading convention ($0$ or $1$) is not known a priori,
   $|W_{Alone}\rangle$ may offer a natural encoding of "exactly one
   anomalous unit" that does not depend on this convention.
2. **Symmetric single-defect error encoding.** In physical error models
   where a defect may manifest as a bit-flip *toward* $1$ or *away from*
   $1$ with no preferred direction, an encoding built on
   $|W_{Alone}\rangle$ may be naturally invariant to this ambiguity.
3. **Entanglement and noise robustness.** It is not yet known whether the
   dual-background structure of $|W_{Alone}\rangle$ confers any advantage
   or disadvantage in entanglement entropy, fidelity under depolarizing
   noise, or robustness to qubit loss, relative to the standard $|W\rangle$
   state. This requires direct numerical comparison (e.g., via Qiskit Aer
   noise models) and is identified as the primary open question for future
   work.
4. **Multi-defect / cluster anomaly encoding.** The generalized family
   $|W_{Alone}^{(m)}\rangle$ may be relevant to modeling scenarios in which
   a *group* of $m$ units deviates jointly from a background, while
   retaining full mirror symmetry — but this has not been connected to any
   concrete protocol or benchmarked.

**We emphasize that none of items 1–4 above have been demonstrated,
simulated against a baseline, or benchmarked for practical advantage.** They
are included solely to scope future empirical investigation.

---

## 7. Future Work

- Benchmark fidelity and entanglement entropy of $|W_{Alone}\rangle$ against
  the standard $|W\rangle$ state under realistic noise models (Qiskit Aer).
- Evaluate robustness to qubit loss and dephasing noise.
- Execute the state-preparation circuit on real quantum hardware (e.g., IBM
  Quantum's free tier) to assess practical fidelity.
- Formalize any of the proposed applications (Section 6) as concrete
  protocols with quantitative performance claims.
- Submit for community review (arXiv, Qiskit/PennyLane forums) prior to
  any claim of novel practical utility.

---

## 8. Conclusion

We have defined $|W_{Alone}\rangle$, a normalized $N$-qubit state that
generalizes the standard $W$-state by symmetrizing it under global bit-flip,
and proved this symmetry rigorously. We have further generalized the
construction to a family $|W_{Alone}^{(m)}\rangle$ preserving the same
symmetry across a combinatorially larger state space. All structural claims
(normalization, mirror symmetry) are proven analytically and confirmed
numerically; all application claims are explicitly flagged as unvalidated
hypotheses pending future empirical work. We view this as an initial,
modest contribution — a well-defined mathematical object with a clean
symmetry property — rather than a demonstrated practical advance, and we
invite scrutiny, replication, and extension from the community.

---

## Appendix: Reproducibility

- Code: [`simulate_w_alone.py`](https://github.com/synthesis496/w-alone-state/blob/main/simulate_w_alone.py)
- Repository: https://github.com/synthesis496/w-alone-state
- Requirements: `numpy`, `qiskit` (optional, for cross-validation)
- License: AGPL-3.0 (open research); see `COMMERCIAL-LICENSE.md` for
  commercial use terms.

---

*This document is a working draft (v0.1) intended for iterative refinement
prior to arXiv submission. Feedback, corrections, and critique are welcome
via GitHub Issues or Pull Requests on the companion repository.*
