from dataclasses import dataclass
import tensorly as tl

@dataclass
class PhysicsParams:
    """Physical constants for the Fisher Equation."""
    alpha: float = 0.01   # Diffusion coefficient
    beta: float = 0.2     # Reaction rate
    gamma: float = 0.5    # Saturation parameter
    total_time: float = 30.0  # Days
    dt: float = 0.1       # Time step size

@dataclass
class GeometryParams:
    """Geometric constraints for the Torus implant."""
    R_min: float = 0.4    # Min Major radius
    R_max: float = 0.6    # Max Major radius
    r_min: float = 0.2    # Min Minor radius
    r_max: float = 0.4    # Max Minor radius
    
@dataclass
class ClinicalTargets:
    """Target mass loss milestones."""
    checkpoints = [5, 7, 30]  # Days
    targets = [10.0, 15.0, 30.0]  # mmol released
    tolerance: float = 1e-3
