import matplotlib.pyplot as plt
import numpy as np
from .solver import FEMSolver
from .config import PhysicsParams, ClinicalTargets

def plot_final_result(R, r, rho):
    print(f"Visualizing result for: R={R:.4f}, r={r:.4f}, rho={rho:.4f}")
    
    # Setup
    params = PhysicsParams()
    targets = ClinicalTargets()
    solver = FEMSolver(params)
    
    # Run Simulation
    history = solver.run_simulation(R, r, rho)
    times = [h[0] for h in history]
    mass_loss = [h[1] for h in history]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(times, mass_loss, 'b-', linewidth=2, label='Simulated Mass Loss')
    
    # Plot Targets
    plt.scatter(targets.checkpoints, targets.targets, color='red', s=100, zorder=5, label='Clinical Targets')
    
    plt.title(f"Optimization Result\nParameters: R={R:.3f}, r={r:.3f}, rho={rho:.1f}")
    plt.xlabel("Time (Days)")
    plt.ylabel("Cumulative Mass Loss (mmol)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    output_file = "simulation_result.png"
    plt.savefig(output_file)
    print(f"Figure saved to {output_file}")

if __name__ == "__main__":
    # Parameters from the optimization run
    R_opt = 0.5283
    r_opt = 0.3194
    rho_opt = 30.5018
    
    plot_final_result(R_opt, r_opt, rho_opt)
