from vpython import *
import numpy as np

# Constantes del sistema
M1 = 1.0  # Masa del bloque 1
M2 = 2.0  # Masa del bloque 2
k = 10.0  # Constante del resorte
g = 9.81  # Aceleración debido a la gravedad

# Parámetros de la ecuación de desplazamiento
alpha = (M2 * g) / (M1 + M2)
beta = k / (M1 + M2)

# Crear la escena
scene = canvas(title='Sistema Masa-Resorte-Polea', width=800, height=600)
# Crear el suelo
ground = box(pos=vector(0, -0.5, 0), size=vector(10, 0.1, 10), color=color.green)
# Crear el resorte
spring = helix(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=0.5, coils=10, thickness=0.1, color=color.blue)
# Crear el bloque M1
block1 = box(pos=vector(0, spring.axis.y, 0), size=vector(1, 1, 1), color=color.red, mass=M1)
# Crear la polea
pulley = cylinder(pos=vector(0, 5, 0), axis=vector(0, 0, 1), radius=1, color=color.orange)
# Crear el bloque M2
block2 = box(pos=vector(0, pulley.pos.y - 2, 0), size=vector(1, 1, 1), color=color.yellow, mass=M2)
# Crear la cuerda
rope = curve(color=color.white, radius=0.05)

def displacement(t):
    return (alpha / beta) * (1 - np.cos(np.sqrt(beta) * t))

# Configurar el tiempo
t = 0
dt = 0.01

# Bucle de simulación
while t < 30:  # Simular durante 10 segundos
    rate(100)  # Controlar la velocidad de la simulación
    # Calcular el desplazamiento
    y = displacement(t)
    # Actualizar la posición del bloque M1
    block1.pos.y = y
    # Actualizar la posición del bloque M2
    block2.pos.y = pulley.pos.y - (y + 2)
    # Actualizar la cuerda
    rope.clear()
    rope.append(pos=block1.pos)
    rope.append(pos=pulley.pos)
    rope.append(pos=block2.pos)
    # Actualizar el tiempo
    t += dt
