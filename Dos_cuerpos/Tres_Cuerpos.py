#Disclaimer, realmente se hace con runge kutta para mejorar la precisión
from vpython import sphere, vector, color, rate, norm, mag
from math import sqrt

# Constantes
G = 6.67e-11

# Masas (kg)
m1 = 4e30    # Luna
m2 = 2e30    # Tierra
m3 = 5e30    # Sol

# Distancias relativas (m)
rdist_12 = 1e11  # Distancia entre la Luna y la Tierra
rdist_23 = 1.5e11  # Distancia entre la Tierra y el Sol

# Posiciones iniciales (x-coordinates calculadas usando el centro de masas)
M12 = m1 + m2
x1 = -(m2 / M12) * rdist_12
x2 = (m1 / M12) * rdist_12
x3 = x2 + rdist_23  # El Sol está más lejos del sistema Luna-Tierra

# Velocidades iniciales
v1 = vector(0, sqrt(G * m2 / abs(x1 - x2)), 0)  # Velocidad de la Luna
v2 = vector(0, -sqrt(G * m1 / abs(x2 - x1)), 0)  # Velocidad de la Tierra
v3 = vector(0, -sqrt(G * (m1 + m2) / abs(x3 - x2)), 0)  # Velocidad del Sol
tierra_texture = "Tierra_skin.jpg"
luna_texture = "Luna_skin.jpg"
sol_texture = "Sol_skin.jpg"
# Crear los cuerpos
star1 = sphere(pos=vector(x1, 0, 0), radius=4e9, texture=luna_texture, make_trail=True)   # Luna
star2 = sphere(pos=vector(x2, 0, 0), radius=8e9, texture=tierra_texture, make_trail=True)  # Tierra
star3 = sphere(pos=vector(x3, 0, 0), radius=12e9, texture=sol_texture, make_trail=True)  # Sol

# Asignar momentos lineales iniciales
star1.p = m1 * v1
star2.p = m2 * v2
star3.p = m3 * v3

# Tiempo de simulación
t = 0
dt = 1000

# Bucle de simulación
while t < 1e8:
    rate(500)  # Velocidad de simulación

    # Calcular las fuerzas entre los cuerpos
    r12 = star2.pos - star1.pos
    r13 = star3.pos - star1.pos
    r23 = star3.pos - star2.pos

    F12 = G * m1 * m2 * norm(r12) / mag(r12)**2
    F13 = G * m1 * m3 * norm(r13) / mag(r13)**2
    F23 = G * m2 * m3 * norm(r23) / mag(r23)**2

    # Actualizar los momentos lineales
    star1.p += (F12 + F13) * dt
    star2.p += (-F12 + F23) * dt
    star3.p += (-F13 - F23) * dt

    # Actualizar las posiciones
    star1.pos += star1.p * dt / m1
    star2.pos += star2.p * dt / m2
    star3.pos += star3.p * dt / m3

    # Incrementar tiempo
    t += dt

# Mantener la ventana abierta
while True:
    pass

