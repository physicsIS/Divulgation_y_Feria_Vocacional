
from vpython import sphere, vector, color, rate, mag, norm, cross, scene
from math import sqrt
import numpy as np  

#NOTA: AGREGAR VALORES REALES DESPUES
G=6.67e-11
m1=7.35e22    #Luna
m2=5.97e24    # Tierra
rdist=2e10 #Distancia entre la Tierra y la Luna
M=m1+m2
x1=-(m2/M)*rdist
x2=(m1/M)*rdist
tierra_texture = "Tierra_skin.jpg"
luna_texture = "Luna_skin.jpg"
star1=sphere(pos=vector(x1,0,0), radius=1.737e6, texture=luna_texture, make_trail=True)
star2=sphere(pos=vector(x2,0,0), radius=6.671e6, texture=tierra_texture, make_trail=True)
Rcom=(star1.pos*m1+star2.pos*m2)/M
r=star2.pos-star1.pos
v1circle=sqrt(G*m2*mag(star1.pos)/mag(r)**2)

star1.v=vector(0,v1circle,0)
star1.p=m1*star1.v
star2.p=-star1.p

t=0
dt=1000
while t<1e9:
  rate(100)
  r=star2.pos-star1.pos
  F2=-G*m1*m2*norm(r)/mag(r)**2
  star2.p=star2.p+F2*dt
  star1.p=star1.p-F2*dt
  star1.pos=star1.pos+star1.p*dt/m1
  star2.pos=star2.pos+star2.p*dt/m2
  t=t+dt

# Mantener la ventana abierta
while True:
    pass
    