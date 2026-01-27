import numpy as np
try:
    import dolfin as df
except ImportError:
    print("Warning: FEniCS (dolfin) not found. Simulation will run in mock mode or fail.")
    df = None

from .config import PhysicsParams

class FEMSolver:
    def __init__(self, params: PhysicsParams):
        self.params = params
        if df is not None:
            self.mesh = df.BoxMesh(df.Point(-1, -1, -1), df.Point(1, 1, 1), 20, 20, 20)
            self.V = df.FunctionSpace(self.mesh, 'P', 1)

    def define_initial_condition(self, R, r, rho):
        """
        Defines the initial Condition u(x, 0) based on torus geometry.
        u = rho if inside torus(R,r), else 0.
        """
        if df is None: return None
        
        # Expression for Torus geometry: (sqrt(x^2 + y^2) - R)^2 + z^2 <= r^2
        code = '''
        class InitialCondition : public Expression {
        public:
            double R, r, rho;
            InitialCondition() : Expression() {}
            void eval(Array<double>& values, const Array<double>& x) const {
                double R2 = x[0]*x[0] + x[1]*x[1];
                double d = sqrt(R2) - R;
                if (d*d + x[2]*x[2] <= r*r) {
                    values[0] = rho;
                } else {
                    values[0] = 0.0;
                }
            }
        };
        '''
        u0 = df.Expression(code, degree=2, R=R, r=r, rho=rho)
        return df.interpolate(u0, self.V)

    def run_simulation(self, R, r, rho):
        """
        Solves the Fisher Equation:
        du/dt - alpha*div(grad(u)) = beta*u*(1 - gamma*u)
        Returns: mass_loss_history (list of tuples (time, mass))
        """
        if df is None:
            # Return dummy data for testing without FEniCS
            t = np.linspace(0, self.params.total_time, int(self.params.total_time/self.params.dt))
            mass_loss = rho * (1 - np.exp(-0.1 * t)) # Synthetic decay
            return list(zip(t, mass_loss))

        u = df.TrialFunction(self.V)
        v = df.TestFunction(self.V)
        u_n = self.define_initial_condition(R, r, rho)
        
        dt = self.params.dt
        alpha = self.params.alpha
        beta = self.params.beta
        gamma = self.params.gamma

        # Variational form (Crank-Nicolson)
        # F = (u - u_n)*v*dx + dt*alpha*dot(grad(0.5*(u + u_n)), grad(v))*dx \
        #     - dt*beta*u_n*(1 - gamma*u_n)*v*dx
        
        F = (u - u_n)*v*df.dx + dt*alpha*df.dot(df.grad(0.5*(u + u_n)), df.grad(v))*df.dx \
            - dt*beta*u_n*(1 - gamma*u_n)*v*df.dx
            
        a, L = df.lhs(F), df.rhs(F)
        
        u = df.Function(self.V)
        t = 0
        history = []
        
        initial_mass = df.assemble(u_n*df.dx)
        history.append((0, 0.0))

        while t < self.params.total_time:
            t += dt
            df.solve(a == L, u)
            u_n.assign(u)
            
            current_mass = df.assemble(u*df.dx)
            loss = initial_mass - current_mass
            history.append((t, loss))
            
        return history
