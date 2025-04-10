# NiS Tight-Binding Model (Slater-Koster Formalism)

This project implements a tight-binding simulation of NiS based on the Slater-Koster formalism, aimed at reproducing **Eq. (2), Eq. (4), and Figs. 6 & 7** from the paper:

> **"Deterministic role of chemical bonding in the formation of altermagnetism"**  
> [arXiv:2501.00453v2](https://arxiv.org/abs/2501.00453)

---

## Objective

- Construct a Slater-Koster-based Hamiltonian to study **altermagnetic spin splitting (ASS)**.
- Model orbital-resolved hopping between Ni-d and S-p orbitals.
- Replicate band structures in AFM and altermagnetic phases as shown in the reference.

---

## Features

- **Spin-resolved 8×8 Hamiltonian** using Slater-Koster terms.
- Modular hopping definitions via a symbolic `lambda` registry.
- Symbolic support in JSON for lattice vectors and k-points (e.g., `"a/2"`, `"c/4"`).
- Dynamic dispatcher selects correct orbital hopping function based on config.

---

## Project Structure

| File                | Role |
|---------------------|------|
| `main.py`           | Main runner and plot generator |
| `config_loader.py`  | Parses and evaluates symbolic JSON config |
| `hamiltonian.py`    | Builds the 8×8 Hamiltonian matrix |
| `sk_hoppings.py`    | Contains all orbital-pair hopping functions |
| `bandstructure.py`  | Eigenvalue solver and plot writer |
| `input_config.json` | User-defined orbitals, vectors, k-path, SK parameters |

---

## Supported Orbital Combinations

Includes (and expandable):
- `dxy_{px, py, pz}`, `dyz_{px, py, pz}`
- `dx2y2_{px, py, pz}`, `dz2_{px, py, pz}`

---

## Target Figures

- **Fig. 6:** AFM band structure without S–S′ coupling
- **Fig. 7:** Altermagnetic band structure with S–S′ hybridization

---

## Designed for

- Testing chemical symmetry and orbital hybridization effects
- Exploring tight-binding models with realistic SK hopping
- Educational insight into ASS and Slater-Koster-based band modeling