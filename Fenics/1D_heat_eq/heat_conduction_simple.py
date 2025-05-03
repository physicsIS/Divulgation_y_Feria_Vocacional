import fenics as fe
import matplotlib.pyplot as plt

n_elements = 32
mesh = fe.UnitIntervalMesh(n_elements)

# Define a Function Space
lagrange_polynomial_space_First_order = fe.FunctionSpace(
    mesh,
    "Lagrange",
    1
    )

# Boundary condition

u_on_boundary = fe.Constant(0.0)

# Function tho return wheter we are on the boundary or not

def boundary_boolean_function(x, on_boundary):
    return on_boundary
    
boundary_condition = fe.DirichletBC(lagrange_polynomial_space_First_order,u_on_boundary, boundary_boolean_function)

# The inicial condition
initial_condition = fe.Expression("sin(3.14*x[0])", degree =1)

u_old = fe.interpolate(initial_condition,lagrange_polynomial_space_First_order)

plt.figure()
fe.plot(u_old, label = "t = 0.0s")

time_step_lenght = 0.1

heat_source = fe.Constant(0.0)

# Create the Finite Element Problem

u_trial = fe.TrialFunction(lagrange_polynomial_space_First_order)
v_test = fe.TestFunction(lagrange_polynomial_space_First_order)

weak_form_residuum = (u_trial * v_test *fe.dx + time_step_lenght * fe.dot(fe.grad(u_trial),fe.grad(v_test)) * fe.dx  
                            - u_old*v_test*fe.dx + time_step_lenght* heat_source*v_test*fe.dx)
    
weak_form_lhs = fe.lhs(weak_form_residuum)
weak_form_rhs = fe.rhs(weak_form_residuum)

u_sol = fe.Function(lagrange_polynomial_space_First_order)

n_time_steps = 5

time_current = 0.0

for i in range(n_time_steps):
    time_current += time_step_lenght

    fe.solve(weak_form_lhs==weak_form_rhs,u_sol,boundary_condition)

    u_old.assign(u_sol)

    fe.plot(u_sol, label= f"t = {time_current:1.1f}")

plt.legend()
plt.title("Heat Conduction 1D")
plt.xlabel('x')
plt.ylabel('T')
plt.grid()
plt.show()