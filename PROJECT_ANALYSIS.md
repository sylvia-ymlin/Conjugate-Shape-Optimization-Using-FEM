# Project Analysis: Conjugate Shape Optimization Using FEM

## 1. Surface Layer: Project Objective and Scope
**Objective**: The primary goal of this project involves the computational design of a hormone-releasing medical implant (a torus). The design objective is to optimize the geometric dimensions and initial chemical concentration to achieve a specific drug release profile over a 30-day period.

**Methodology**: The engineering challenge is formulated as an inverse design problem constrained by a reaction-diffusion partial differential equation (PDE).

**Key Inputs and Outputs**:
*   **Design Parameters**: Major radius ($R$), minor radius ($r$), and initial hormone density ($\rho$).
*   **Output**: The cumulative mass loss curve over time, representing the drug dosage delivered to the biological system.

**Technology Stack**:
*   **MATLAB**: Used for fundamental numerical verification, including 1D adaptive mesh refinement and 2D convergence analysis.
*   **Python (FEniCS)**: Utilized for high-fidelity 3D Finite Element Method (FEM) simulations.
*   **SciPy**: Employed for the Nelder-Mead optimization algorithm.

## 2. Middle Layer: Numerical Verification and Validation
To ensure simulation reliability, the numerical methods were rigorously validated on lower-dimensional models before deployment to the full 3D problem.

### 2.1 Adaptive Mesh Refinement (1D)
*   **Problem**: Uniform meshes fail to efficiently capture solutions with sharp gradients or singularities.
*   **Method**: An *a posteriori* error estimator was mathematically derived based on the residual of the discrete solution:
    $$ \eta_i = h_i \| f + \alpha u_h'' \|_{L^2(I_i)} $$
*   **Implementation**: A refinement algorithm was implemented to mark elements with the highest error contribution and bisect them.
*   **Result**: The mesh successfully concentrated nodes around discontinuities in the source function, achieving the target error tolerance with optimal computational cost.

### 2.2 Convergence Analysis (2D)
*   **Method**: The standard Poisson equation was solved on a circular domain using linear finite elements.
*   **Metric**: The error was measured in the Energy Norm $\|u - u_h\|_E$.
*   **Conclusion**: The observed convergence rate was approximately 1.0, consistent with theoretical expectations ($O(h)$) for piecewise linear basis functions. This validated the correctness of the stiffness and mass matrix assembly routines.

## 3. Deep Layer: Physics Modeling and Inverse Design
The core complexity lies in solving the time-dependent, non-linear multiphysics problem and integrating it into an optimization loop.

### 3.1 Mathematical Modeling
The drug release process is governed by Fisher's Equation, a reaction-diffusion PDE:
$$ \frac{\partial u}{\partial t} - \alpha \Delta u = \beta u (1 - \gamma u) $$
*   **Diffusion Term** ($-\alpha \Delta u$): Models the transport of the hormone through the tissue.
*   **Reaction Term** ($\beta u (1 - \gamma u)$): Models the biological degradation or binding of the drug.
*   **Discretization**: A mixed explicit-implicit time-stepping scheme was employed. The diffusion term is treated implicitly (Crank-Nicolson) for unconditional stability, while the non-linear reaction term is linearized explicitly to avoid Newton iterations at every time step.

### 3.2 Geometric Embedding
Generating body-fitted meshes for toroidal geometries is computationally expensive. This project utilizes an embedded boundary approach:
*   The computational domain is a simple bounding sphere/cube.
*   The complex torus geometry is defined via the Initial Condition:
    $$ u(\mathbf{x}, 0) = \begin{cases} \rho & \text{if } \mathbf{x} \in \text{Torus}(R, r) \\ 0 & \text{else} \end{cases} $$
This level-set-like method simplifies the meshing process while preserving geometric fidelity through mesh resolution.

### 3.3 Optimization Pipeline
*   **Objective Function**: A least-squares functional is defined to measure the deviation between the simulated mass loss $M(T)$ and the clinical targets at days 5, 7, and 30.
*   **Algorithm**: The Nelder-Mead simplex algorithm was selected for its robustness in derivative-free optimization, suitable for non-smooth objective landscapes common in PDE-constrained problems.
*   **Outcome**: The optimization loop successfully converged to a unique set of design parameters ($\rho \approx 40.9, R \approx 0.50, r \approx 0.30$) that met the prescribed therapeutic requirements.
