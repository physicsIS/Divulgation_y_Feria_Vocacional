import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_wave(W, T):
    """
    Visualización de la propagación de la onda en una placa cuadrada.
    
    Args:
        W: Arreglo 3D con la solución de la onda.
        T: Número de pasos de tiempo.
    """
    # Configuración de la figura
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for t in range(T):
        ax.clear()
        # Graficar la superficie
        X, Y = np.meshgrid(range(W.shape[1]), range(W.shape[0]))
        ax.plot_surface(X, Y, W[:, :, t], cmap='viridis', edgecolor='none')
        
        # Ajustar los ejes y etiquetas
        ax.set_xlim(0, W.shape[1])
        ax.set_ylim(0, W.shape[0])
        ax.set_zlim(-1, 1)  # Ajusta el rango de amplitud
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Amplitud')
        ax.set_title(f"Simulación de la propagación de la onda, t = {t}")
        
        # Barra de color
        mappable = ax.plot_surface(X, Y, W[:, :, t], cmap='viridis', edgecolor='none')
        fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10)
        
        # Control de velocidad de la animación
        plt.pause(0.01)

    plt.show()
