# Shape Optimization of Medical Implants via Finite Element Method

[![Python | FEniCS](https://img.shields.io/badge/Stack-Python%20%7C%20FEniCS-blue.svg)](https://fenicsproject.org/)
[![Optimization: Nelder-Mead](https://img.shields.io/badge/Optimization-Nelder--Mead-green.svg)](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html)

Computational design of a hormone-releasing torus implant. This project implements a full PDE-constrained optimization pipeline, from Mathematical Modeling (Fisher's Equation) to 3D Finite Element Simulation and Inverse Design.

## 🚀 Key Highlights

*   **PDE-Constrained Optimization**: Solved the inverse problem to find optimal geometric parameters ($R, r, \rho$) satisfying specific clinical drug-release targets ($M=\{10, 15, 30\}$ mmol).
*   **Adaptive Mesh Refinement (AMR)**: Derived and implemented an *a posteriori* error estimator $\eta_i$ to automatically refine meshes around singularities, optimizing computational cost.
*   **Geometric Embedding**: Modeled complex torus geometry via Level-Set Initial Conditions on a bounding domain, avoiding expensive body-fitted mesh generation.

## 📊 Technical Visuals

### 1. Adaptive Mesh Refinement (1D)
Nodes automatically concentrate around the discontinuities in the source function, validating the error estimator.
<img src="AppliedFEM/ProblemB1_FinestMeshes.png" width="400" />

### 2. 3D Diffusion Simulation
Simulation of hormone concentration field $u(\mathbf{x}, t)$ evolving over 30 days.
<img src="AppliedFEM/ProblemB3_Solution_T_30.png" width="400" />

### 3. Parameter Sensitivity & Mass Loss
Tracking cumulative mass loss to match clinical targets.
<img src="AppliedFEM/Part3_Task2_Massloss.png" width="400" />

## 🛠️ Methodology

1.  **Governing Equation**: Fisher's Reaction-Diffusion Equation.
    $$ \frac{\partial u}{\partial t} - \alpha \Delta u = \beta u (1 - \gamma u) $$
2.  **Solver**: Crank-Nicolson (Time) + Galerkin FEM (Space).
3.  **Optimization**: Nelder-Mead Simplex Algorithm (Derivative-free).
