from vpython import *

# CONTANTES

piso = 25
altura_piso = 1
bases_silla = 12.5

altura_cascaron_cilindrico = 15
ancho_cascaron_cilindrico = 0.25



# GENERACION DE LA ESCENA Y AJUSTES DE CAMARA
scene=canvas(width=750, height=500,range=300)
scene.autoscale = True
scene.forward = vector(0,-2,-2)


# GENERACION DE LOS EJES COORDENADOS
largoeje = 30
anchoeje= 0.25

Xarrow = arrow(axis = vector(1,0,0), color = color.blue, length = largoeje, shaftwidth = anchoeje)
labelx = label(pos= vector(1.2*largoeje,0,0), text = "X", box = 0)

Yarrow = arrow(axis = vector(0,1,0), color = color.green, length = largoeje, shaftwidth = anchoeje)
labely = label(pos= vector(0,1.2*largoeje,0), text = "Y", box = 0)

Zarrow = arrow(axis = vector(0,0,1), color = color.red, length = largoeje, shaftwidth = anchoeje)
labelz = label(pos= vector(0,0,1.2*largoeje), text = "Z", box = 0)


# FIGURAS


# Piso del escenario
tabla_piso = box(pos= vector(0,0,0),length = piso, width = piso, height = altura_piso, color = color.orange)


# Base del banco
base_cuadrada1 = box(pos= vector(0,altura_piso,0),length = bases_silla, width = bases_silla/5, height = altura_piso, color = color.green)
base_cuadrada1 = box(pos= vector(0,altura_piso,0),length = bases_silla, width = bases_silla/5, height = altura_piso, color = color.green).rotate(axis=vec(0,1,0),angle = pi/2, origin = vec(0,0,0))
base_circular = cylinder(pos = vec(0,altura_piso/2,0), axis = vec(0,altura_piso,0), radius = bases_silla/4, color = color.green)

# Cascaron cilindrico del banco
cascaron_2d = shapes.rectangle(pos = [0,altura_piso/2 + altura_piso + altura_cascaron_cilindrico/2], width = ancho_cascaron_cilindrico , height = altura_cascaron_cilindrico)
cascaron_ed = extrusion(shape = cascaron_2d , path = paths.arc(radius = 2, angle1 = 0,angle2 = 2*pi + pi/250))

# Poste cilindrico y asiento
poste = cylinder(pos = vec(0,altura_piso/2 + 2*altura_piso,0) , axis = vec(0,altura_cascaron_cilindrico+1/3*altura_piso,0), radius = 1.2, color = color.red)

asiento = cylinder(pos = vec(0,altura_piso/2 + 2*altura_piso + altura_cascaron_cilindrico+1/3*altura_piso,0) , axis = vec(0,altura_piso/2,0), radius = 5 , color = color.blue)