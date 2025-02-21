from vpython import *
import proyectil as pr
import numpy as np
import time


escala = 1 # Para hacerlo mas didactico, 1 corresponde al tamaño real

thetaprime = 2.0*np.pi*(2.2957)/360.0 # Latitud o elevación del cañon ------> 2.0*np.pi*(2.2957)/360.0 (ideal) -----> (friccion) -----> (NI y friccion)

theta = np.pi/2 - thetaprime
phi  = 0 # Direción en el plano del suelo medida desde el eje x -------> 0 (ideal) -----> (friccion) -----> (NI y friccion)
v0 = 500 #m/s ----> magnitud de la velocidad --------> 500 Este no se cambia



########################################################################################
# Crear la escena
########################################################################################
scene = canvas(title='Tiro al blanco', width=800, height=600)
scene.background = color.black


# Ejes

largoeje = 20
anchoeje= 2/5

Xarrow = arrow(axis = vector(largoeje,0,0), color = color.blue, shaftwidth = anchoeje)
labelx = label(pos= vector(1.2*largoeje,0,0), text = "X", box = 0)

Yarrow = arrow(axis = vector(0,largoeje,0), color = color.green, shaftwidth = anchoeje, opacity = 0.5)
labely = label(pos= vector(0,1.2*largoeje,0), text = "Y", box = 0)

Zarrow = arrow(axis = vector(0,0,largoeje), color = color.red, shaftwidth = anchoeje)
labelz = label(pos= vector(0,0,1.2*largoeje), text = "Z", box = 0)

# Escenografía

# Crear el suelo
ground = box(pos=vector(1000, 0, 0), size=vector(2010, -0.3, 50), color=color.gray(0.5))

#####################################################################################################################
# Canon
#####################################################################################################################
# Base del cañón (estructura de madera)
base = box(pos=vector(-1.25, 0.9, 0), size=vector(2.5, 0.1, 1.2), color=color.orange)

# Soportes laterales del cañón
soporte1 = box(pos=vector(-0.8 +base.pos.x, base.pos.y-0.25, 0.3), size=vector(1.5, 0.5, 0.1), color=color.orange)
soporte2 = box(pos=vector(-0.8 +base.pos.x,  base.pos.y-0.25, -0.3), size=vector(1.5, 0.5, 0.1), color=color.orange)

# Eje de las ruedas
#eje = cylinder(pos=vector(-0.8, 2, 0.3), axis=vector(0, 0, -0.6), radius=0.05, color=color.gray(0.4))

# Ruedas
rueda1 = cylinder(pos=vector(-1.2 +base.pos.x, 0.55, 0.3), axis=vector(0, 0, -0.6), radius=0.4, color=color.black) # Rueda trasera
rueda2 = cylinder(pos=vector(0.8 +base.pos.x, 0.55, 0.3), axis=vector(0, 0, -0.6), radius=0.4, color=color.black) # Rueda delantera

# Tubo del cañón
angulo = radians(20)  # Ángulo de inclinación
largo_canon = 2
canon = cylinder(pos=vector(-0.8+base.pos.x, 0.9, 0), 
                axis=vector(largo_canon*cos(angulo), largo_canon*sin(angulo), 0), 
                radius=0.2, color=color.gray(0.2))

# Boca del cañón
boca = cylinder(pos=canon.pos + canon.axis, axis=vector(0.15*cos(angulo), 0.15*sin(angulo), 0), 
                radius=0.25, color=color.gray(0.1))

# Aros decorativos en el cañón
aro1 = ring(pos=vector(-0.8 +base.pos.x + 0.4*cos(angulo), canon.pos.y + 0.4*sin(angulo), 0), 
            axis=canon.axis, radius=0.22, thickness=0.03, color=color.gray(0.3))
aro2 = ring(pos=vector(-0.8 +base.pos.x + 1.5*cos(angulo), canon.pos.y + 1.5*sin(angulo), 0), 
            axis=canon.axis, radius=0.22, thickness=0.03, color=color.gray(0.3))

# Bola de cañón lista para disparo
# Hay una bola por regimen
bola_ideal = sphere(pos=canon.pos + canon.axis + vector(0.2*cos(angulo), 0.2*sin(angulo), 0), # Proyectil ideal (ROJA)
            radius=0.25, color=color.red, make_trail = True, trail_radius = 0.25, interval = 5) #  trail_type = "line",

bola_friccion = sphere(pos=canon.pos + canon.axis + vector(0.2*cos(angulo), 0.2*sin(angulo), 0), # Proyectil friccion (AZUL)
            radius=0.25, color=color.blue, make_trail = True, trail_radius = 0.25, interval = 5) #  trail_type = "line",

bola_Ni_friccion = sphere(pos=canon.pos + canon.axis + vector(0.2*cos(angulo), 0.2*sin(angulo), 0), # Proyectil no inecial friccion (ORANGE)
            radius=0.25, color=color.orange, make_trail = True, trail_radius = 0.25, interval = 5) #  trail_type = "line",

########################################################################################################################

########################################################################################################################
# Diana
########################################################################################################################
# La diana va a ser un objeto circular de 50 cm con franjas de diferentes colores, todas del mismo tamaño

# Diana compuesta por 5 cilindros concéntricos
centro_diana = vector(ground.size.x-10, 2.5, 0)  # Posición en X adelante del cañón

colores = [color.red, color.white, color.blue, color.white, color.orange]  # Alternancia de colores
radios = [5.0 + i * 5.0 for i in range(5)]  # Radios internos

# Crear los anillos de la diana
for i in range(5):
    ring(pos=centro_diana, axis=vector(1, 0, 0), radius=radios[i], thickness=2.5, color=colores[i])
##########################################################################################################################

##########################################################################################################################
# Dinamica
##########################################################################################################################


# NO TOCAR
x_0 = 0
y_0 =0
z_0 = 0.9 + 2.0*np.sin(thetaprime)
vx_0 = v0*np.sin(theta)*np.cos(phi)
vy_0 = v0*np.sin(theta)*np.sin(phi)
vz_0 = v0*np.cos(theta)
g_n = 9.81
a_n =0.05
c_n =0.001
m_n = 100
omega_n = 2*np.pi/(3600*24)
R_n = 6371*10**3
labbda_n = 1.396
t_0 = 0
t_f = 4
nn = 1000

omega_n = 2*np.pi/(3600*24)
R_n = 6.371*10**3
labbda_n = 1.396

sol_ideal = pr.proyectil_ideal(x_0,y_0,z_0,vx_0,vy_0,vz_0,g_n,np.linspace(t_0,t_f,nn))
x_ideal = sol_ideal[1]
y_ideal = sol_ideal[2]
z_ideal = sol_ideal[3]

sol_fric = pr.proyectil_friccion(x_0,y_0,z_0,vx_0,vy_0,vz_0,g_n,a_n,c_n,m_n,t_0,t_f+0.045,nn) # Extra de tiempo para que terminen en el mismo plano vertical todas
x_fric = sol_fric.y[0]
y_fric = sol_fric.y[2]
z_fric = sol_fric.y[4]

sol_Ni_fric = pr.proyectil_noinercial_friccion(x_0,y_0,z_0,vx_0,vy_0,vz_0,g_n,a_n,c_n,m_n,omega_n,R_n,labbda_n,t_0,t_f+0.045,nn) # Extra de tiempo para que terminen en el mismo plano vertical todas
x_Ni_fric = sol_Ni_fric.y[0]
y_Ni_fric = sol_Ni_fric.y[2]
z_Ni_fric = sol_Ni_fric.y[4]


i=0
condicion = True
while condicion == True:
	if i == nn:
		i=0
		time.sleep(10)
		bola_ideal.clear_trail()
		bola_friccion.clear_trail()
		bola_Ni_friccion.clear_trail()

	rate(100)
	bola_ideal.pos = vector(x_ideal[i],z_ideal[i],y_ideal[i])
	bola_friccion.pos = vector(x_fric[i],z_fric[i],y_fric[i])
	bola_Ni_friccion.pos = vector(x_Ni_fric[i], z_Ni_fric[i], y_Ni_fric[i])

	# Hacer que la cámara siga la bola
	scene.center = bola_ideal.pos  # Centro de la vista en la posición de la bola
	i+=1
