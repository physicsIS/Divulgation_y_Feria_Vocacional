from vpython import *
import numpy as np

# Constantes del sistema
M1 = 10.0  # Masa del bloque 1
M2 = 20.0  # Masa del bloque 2
k = 120.0  # Constante del resorte
g = 9.81  # Aceleración debido a la gravedad
L = 15 # Longitud de equilibrio del resorte
LL = 20 # Largo de la cuerda


# Parámetros de la ecuación de desplazamiento
alpha = (M2 * g) / (M1 + M2)
beta = k / (M1 + M2)

# Condición Inicial
#y_m1(t=0) = y0 ---> y0 = 0
ym1 = L


# Crear la escena
scene = canvas(title='Sistema Masa-Resorte-Polea', width=800, height=600)


# Ejes

largoeje = 20
anchoeje= 2/5

Xarrow = arrow(axis = vector(largoeje,0,0), color = color.blue, shaftwidth = anchoeje)
labelx = label(pos= vector(1.2*largoeje,0,0), text = "X", box = 0)

Yarrow = arrow(axis = vector(0,largoeje,0), color = color.green, shaftwidth = anchoeje)
labely = label(pos= vector(0,1.2*largoeje,0), text = "Y", box = 0)

Zarrow = arrow(axis = vector(0,0,largoeje), color = color.red, shaftwidth = anchoeje)
labelz = label(pos= vector(0,0,1.2*largoeje), text = "Z", box = 0)



# Crear el suelo
ground = box(pos=vector(0, 0, 0), size=vector(50, -0.1, 50), color=color.green)

# Crear la polea
pulley = cylinder(pos = vector(0,35,0), axis = vector(0,0,-2), radius = 8, color = color.orange)

# Crear el bloque M1 (IZQUIERDO)
block1 = box(pos = vector(-pulley.radius,ym1,-1), size=vector(3, 3, 3), color=color.yellow, mass=M2)

# Crear el bloque M2 (DERECHO)
block2 = box(pos = vector(pulley.radius,LL-block1.pos.y,-1), size=vector(3, 3, 3), color=color.red, mass=M1)

# Crear el resorte
spring = helix(pos = vector(-pulley.radius,0,-1), axis = vector(0,block1.pos.y-1.5,0) , radius = 1 , thickness = 0.5, coils = 8, color=color.blue)

# cuerda

cuerda_path = []
theta = 0
pi = 3.14
while theta <= pi:
    cuerda_path.append(vector(pulley.radius*cos(theta), pulley.radius*sin(theta)+pulley.pos.y,-1))
    theta += pi/1000
arco = curve(cuerda_path, radius = 0.5)

cuerda1 = curve(pos = [vector(-pulley.radius,block1.pos.y+1.5,-1), vector(-pulley.radius,pulley.pos.y,-1)], radius = 0.5) # Extremo izquierdo
cuerda2 = curve(pos = [vector(pulley.radius,block2.pos.y+1.5,-1), vector(pulley.radius,pulley.pos.y,-1)], radius = 0.5) # Extremo derecho




def displacement(t):
    return (alpha / beta) * (1 - np.cos(np.sqrt(beta) * t))

# Configurar el tiempo
t = 0
dt = 0.01

# Bucle de simulación
while t < 30.0:  # Simular durante 10 segundos
    rate(100)  # Controlar la velocidad de la simulación
    # Calcular el desplazamiento
    y = displacement(t)
    # Actualizar la posición del bloque M1
    block1.pos.y = y + L
    # Actualizar la posición del bloque M2
    block2.pos.y = LL-block1.pos.y
    # Actualizar la cuerda
    cuerda1.clear()
    cuerda2.clear()
    cuerda1 = curve(pos = [vector(-pulley.radius,block1.pos.y+1.5,-1), vector(-pulley.radius,pulley.pos.y,-1)], radius = 0.5) # Extremo izquierdo
    cuerda2 = curve(pos = [vector(pulley.radius,block2.pos.y+1.5,-1), vector(pulley.radius,pulley.pos.y,-1)], radius = 0.5) # Extremo derecho
    # Actualizar resorte
    spring.axis.y = block1.pos.y-1.5
    # Actualizar el tiempo
    t += dt
