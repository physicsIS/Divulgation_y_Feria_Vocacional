from modelos import *
from ciclo_estados import *
if __name__ == "__main__":
    
    # Crear el modelo de gas ideal
    modelo = ModeloGasIdeal()
    
    # Crear un ciclo termodinámico
    ciclo = CicloTermodinamico(modelo)

    # Agregar estados con diferentes combinaciones:
    ciclo.agregar_estado("Estado 1 (P y T)", P=1e5, T=300)
    ciclo.agregar_estado("Estado 2 (P y v)", P=1e5, v=0.86167)
    ciclo.agregar_estado("Estado 3 (T y v)", T=500, v=0.5)
    ciclo.agregar_estado("Estado 4 (P y h)", P=1e5, h=301500)

    # Mostrar los estados del ciclo
    ciclo.mostrar_ciclo()