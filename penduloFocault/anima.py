from vpython import *
import numpy as np

x,y,z,time, theta, phi = np.load("cartesianas_save.npy")

'''TENER CUIDADO

Aqui el eje z forma parte de un plano (plano xz), visto desde arriba'''



# GENERACION DE LA ESCENA Y AJUSTES DE CAMARA
scene=canvas(width=1800, height=900,range=400)
scene.autoscale = True
scene.forward = vector(-10,-15,-10)

largoeje = 100
anchoeje = 1


# Ejes Coordenados
Xarrow = arrow(axis = vector(largoeje,0,0), color = color.blue, shaftwidth = anchoeje)
Xarrown = arrow(axis = vector(-largoeje,0,0), color = color.blue, shaftwidth = anchoeje)
labelx = label(pos= vector(1.2*largoeje,0,0), text = "X", box = 0)

Yarrow = arrow(axis = vector(0,1.5*largoeje,0), color = color.green, shaftwidth = anchoeje)
labely = label(pos= vector(0,1.2*largoeje,0), text = "Y", box = 0)

Zarrow = arrow(axis = vector(0,0,largoeje), color = color.red, shaftwidth = anchoeje)
Zarrown = arrow(axis = vector(0,0,-largoeje), color = color.red, shaftwidth = anchoeje)
labelz = label(pos= vector(0,0,1.2*largoeje), text = "Z", box = 0)

# Placa base 

placa = box(pos= vector(0,0,0),length = 2*largoeje, width = 2*largoeje, height = 0.1, color = color.orange)

# Techo del pendulo

placab = box(pos= vector(0,1.2*largoeje,0),length = 10, width = 10, height = 2, color = color.white)

# Pendulo

esfera = sphere(pos = vector(10,10,10), radius = 5, color = color.purple)
cuerda = cylinder(pos=vector(0,1.2*largoeje,0), axis = vector(10,10-1.2*largoeje,10), radius = 1.5, color = color.cyan)

# Datos

# angulo plano
anguloplano = label(pos = vector(-100, 0,0), box = 0, height = 30)

# angulo azimutal

# tiempo
tiempolabel = label(pos = vector(0, 1.5*largoeje,0), box = 0, height = 30)

while True:
    for t in range(len(time)):
        rate(200)
        esfera.pos = vector(x[t],z[t]+1.2*largoeje,y[t])
        cuerda.axis = vector(x[t],z[t],y[t])
        tiempolabel.text = f"t = {round(time[t],1)}"
        phiphi = (round(phi[t],3) - round(phi[t]/np.pi,0)*np.pi)*360/(2*np.pi)

        anguloplano.text = r"\phi = " + f"{round(phiphi,2)}"