import numpy as np

def wave_equation_2D(x_i, x_f, y_i, y_f, Nx, Ny, T, dt, c):
    """
    Resuelve la ecuación de onda en 2D utilizando diferencias finitas.

    Args:
        x_i: Coordenada x inicial del dominio
        x_f: Coordenada x final del dominio
        y_i: Coordenada y inicial del dominio
        y_f: Coordenada y final del dominio
        Nx: Número de puntos en la dirección x
        Ny: Número de puntos en la dirección y
        T: Número de pasos de tiempo
        dt: Tamaño del paso de tiempo
        c: Velocidad de la onda

    Returns:
        Z: Matriz de la solución en cada punto de la malla y en cada instante de tiempo
        X: Matriz de coordenadas x de la malla
        Y: Matriz de coordenadas y de la malla
    """

    # Definición de los pasos espaciales
    hx = (x_f - x_i) / (Nx+1)
    hy = (y_f - y_i) / (Ny+1)
    # Crear los vectores de malla
    x = np.linspace(x_i, x_f, Nx+2) # Vectores de posición en x
    y = np.linspace(y_i, y_f, Ny+2) # Vectores de posición en y

    # Crear mallas 2D para las posiciones
    X, Y = np.meshgrid(x, y)

    # Inicializar matriz para la solución
    Z = np.zeros((Nx+2, Ny+2, T))

    # Aplicar condiciones de frontera de Dirichlet
    Z[0, :, :] = 0
    Z[-1, :, :] = 0
    Z[:, 0, :] = 0
    Z[:, -1, :] = 0

    # Condiciones iniciales (onda gaussiana)
    for i in range(1, Nx+1):
        for j in range(1, Ny+1):
            Z[i, j, 0] = np.exp(-((x[i] - (x_i + x_f)/2)**2 + (y[j] - (y_i + y_f)/2)**2))
    Z[:, :, 1] = Z[:, :, 0]  # Suponiendo derivada temporal inicial cero

    # Bucle en el tiempo
    for t in range(2, T):
        Z[1:-1, 1:-1, t] = 2 * Z[1:-1, 1:-1, t-1] - Z[1:-1, 1:-1, t-2] + \
                         (c**2 * dt**2 / hx**2) * (Z[2:, 1:-1, t-1] - 2 * Z[1:-1, 1:-1, t-1] + Z[:-2, 1:-1, t-1]) + \
                         (c**2 * dt**2 / hy**2) * (Z[1:-1, 2:, t-1] - 2 * Z[1:-1, 1:-1, t-1] + Z[1:-1, :-2, t-1])

    return Z, X, Y
