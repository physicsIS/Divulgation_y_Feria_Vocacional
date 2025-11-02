import fenics as fe

CANTILEVER_LENGTH = 1.0
CANTILEVER_WIDTH = 0.2

N_POINTS_LENGHT = 10
N_POINTS_WIDTH = 3

LAME_MU = 1.0
LAME_LAMBDA = 1.25
DENSITY = 1.0
GRAVITY = 9.81/100

def main():

    # Mesh and vector space

    mesh = fe.BoxMesh(
        fe.Point(0.0 , 0.0 , 0.0),
        fe.Point(CANTILEVER_LENGTH,CANTILEVER_WIDTH,CANTILEVER_WIDTH),
        N_POINTS_LENGHT,
        N_POINTS_WIDTH,
        N_POINTS_WIDTH
    )

    lagrange_vector_space_first_order = fe.VectorFunctionSpace(
        mesh,
        "Lagrange",
        1
    )

    # Boundary conditions

    def clamped_boundary(x, on_boundary):
        return on_boundary and x[0] < fe.DOLFIN_EPS

    dirichlet_boundary = fe.DirichletBC(
        lagrange_vector_space_first_order,
        fe.Constant((0.0,0.0,0.0)),
        clamped_boundary
    )

    # Define strain an stress

    def epsilon(u):
        engineering_strain = 0.5*(fe.nabla_grad(u) + fe.nabla_grad(u).T)
        return engineering_strain
    
    def sigma(u):
        cauchy_stress = (
            LAME_LAMBDA*fe.tr(epsilon(u)) * fe.Identity(3) + 2*LAME_MU*epsilon(u)
        )
        return cauchy_stress
    
    # define weak form

    u_trial = fe.TrialFunction(lagrange_vector_space_first_order)
    v_test = fe.TestFunction(lagrange_vector_space_first_order)
    forcing = fe.Constant((0, 0, -DENSITY*GRAVITY))
    traction = fe.Constant((0.0 ,0.0 ,0.0))

    weak_form_lhs = fe.inner(sigma(u_trial), epsilon(v_test)) * fe.dx
    weak_form_rhs = (fe.dot(forcing,v_test) * fe.dx +fe.dot(traction,v_test)*fe.ds)

    # compute solution

    u_solution = fe.Function(lagrange_vector_space_first_order)
    fe.solve(
        weak_form_lhs == weak_form_rhs,
        u_solution,
        dirichlet_boundary
    )

    # compute the von Mises Stress

    deviatoric_stress_tensor = (
        sigma(u_solution) - 1/3 * fe.tr(sigma(u_solution)) * fe.Identity(3)
    )

    von_Mises_stress = fe.sqrt(3/2 *fe.inner(deviatoric_stress_tensor,deviatoric_stress_tensor))

    lagrange_scalar_space_first_order = fe.FunctionSpace(
        mesh,
        'Lagrange',
        1
    )
    von_Mises_stress = fe.project(von_Mises_stress, lagrange_scalar_space_first_order)

    # write our fields for visualization with paraview

    u_solution.rename("Displacement Vector","")
    von_Mises_stress.rename("von Mises stress","")

    beam_deflection_file = fe.XDMFFile("beam_deflection.xdmf")
    beam_deflection_file.parameters["flush_output"] = True
    beam_deflection_file.parameters["functions_share_mesh"] = True
    beam_deflection_file.write(u_solution,0.0)
    beam_deflection_file.write(von_Mises_stress,0.0)

if __name__== "__main__":
    main()