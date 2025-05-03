import fenics as fn

box_width = 400
box_height = 50

mesh = fn.RectangleMesh(fn.Point(0, 0),
        fn.Point(box_width, box_height),
        80, 10)

V = fn.FunctionSpace(mesh, 'P', 1)

vtk_file = fn.File('output/mesh.pvd')
vtk_file << mesh

v_1 = fn.Constant(5.0)
v_0 = fn.Constant(1.0)

def bottom_side(x, on_boundary):
    if fn.near(x[1], 0) and on_boundary:
        return True

def top_side(x, on_boundary):
    if fn.near(x[1], box_height) and on_boundary:
        return True

bot_bc = fn.DirichletBC(V, v_0, bottom_side)
top_bc = fn.DirichletBC(V, v_1, top_side)
bcs = [top_bc, bot_bc]

u = fn.TrialFunction(V)
v = fn.TestFunction(V)
f = fn.Constant(0)
a = fn.dot(fn.grad(u), fn.grad(v))*fn.dx
L = f*v*fn.dx

u = fn.Function(V)
fn.solve(a == L, u, bcs)

potential = fn.File('output/electric_potential.pvd')
potential << u

E = - fn.grad(u)
field = fn.File('output/electric_field.pvd')
field << fn.project(E)  