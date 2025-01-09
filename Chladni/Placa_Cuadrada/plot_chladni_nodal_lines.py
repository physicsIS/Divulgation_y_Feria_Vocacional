import numpy as np
import matplotlib.pyplot as plt

def plot_chladni_nodal_lines(L, n, m):
    # Definir el rango de x y y
    x = np.linspace(0, L, 100)
    y = np.linspace(0, L, 100)
    
    # Crear la malla de coordenadas (X, Y)
    X, Y = np.meshgrid(x, y)
    
    # Usar la solución analítica para ver las líneas nodales
    Z = np.cos(n * np.pi * X / L) * np.cos(m * np.pi * Y / L) - \
        np.cos(m * np.pi * X / L) * np.cos(n * np.pi * Y / L)
    
    # Graficar el patrón de Chladni con líneas nodales
    plt.figure()
    cp = plt.contour(X, Y, Z, levels=[0], colors='black', linewidths=2)
    plt.title(f'Patrón Chladni para n = {n}, m = {m}')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.axis('equal')
    plt.grid(True)
    plt.show()