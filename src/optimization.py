import numpy as np
from scipy.optimize import minimize
from .solver import FEMSolver
from .config import PhysicsParams, ClinicalTargets

def objective_function(x, solver: FEMSolver, targets: ClinicalTargets):
    """
    Loss function L = sum((M_sim(t_i) - M_target_i)^2)
    x: [R, r, rho]
    """
    R, r, rho = x
    print(f"Evaluating: R={R:.3f}, r={r:.3f}, rho={rho:.3f}")
    
    # Run simulation
    history = solver.run_simulation(R, r, rho)
    
    # Interpolate to find mass at target days
    times = [h[0] for h in history]
    masses = [h[1] for h in history]
    
    loss = 0.0
    for day, target in zip(targets.checkpoints, targets.targets):
        simulated_mass = np.interp(day, times, masses)
        loss += (simulated_mass - target)**2
        
    print(f"  Loss: {loss:.4f}")
    return loss

def run_optimization():
    print("Initializing Optimization Pipeline...")
    params = PhysicsParams()
    targets = ClinicalTargets()
    solver = FEMSolver(params)
    
    # Initial guess [R, r, rho]
    x0 = [0.5, 0.3, 40.0]
    
    # Bounds for parameters
    bounds = [(0.4, 0.6), (0.2, 0.4), (20.0, 60.0)]
    
    # Nelder-Mead Optimization
    res = minimize(
        objective_function, 
        x0, 
        args=(solver, targets),
        method='Nelder-Mead',
        options={'disp': True, 'maxiter': 50}
    )
    
    print("\nOptimization Complete!")
    print(f"Optimal Parameters: R={res.x[0]:.4f}, r={res.x[1]:.4f}, rho={res.x[2]:.4f}")
    print(f"Final Residual: {res.fun:.6f}")

if __name__ == "__main__":
    run_optimization()
