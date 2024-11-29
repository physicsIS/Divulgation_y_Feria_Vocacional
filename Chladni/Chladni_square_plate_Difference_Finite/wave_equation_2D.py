import numpy as np

def wave_equation_2D(x_i, x_f, y_i, y_f, Nx, Ny, T, dt, c):
    """
    Solución de la ecuación de onda 2D usando diferencias finitas
    """
    # Definición de los pasos espaciales
    hx = (x_f - x_i) / (Nx + 1)
    hy = (y_f - y_i) / (Ny + 1)

    # Crear los vectores de malla
    x = np.linspace(x_i, x_f, Nx + 2)  # Incluye las condiciones de frontera
    y = np.linspace(y_i, y_f, Ny + 2)

    # Crear mallas 2D para las posiciones
    X, Y = np.meshgrid(x, y)

    # Inicializar matrices para el tiempo
    Z = np.zeros((Nx + 2, Ny + 2, T))

    # Condiciones iniciales: onda gaussiana
    for i in range(1, Nx + 1):
        for j in range(1, Ny + 1):
            Z[i, j, 0] = np.exp(-((x[i] - (x_i + x_f) / 2) ** 2 + (y[j] - (y_i + y_f) / 2) ** 2))
            Z[i, j, 1] = Z[i, j, 0]  # Suponiendo derivada temporal inicial cero

    # Bucle en el tiempo
    for t in range(2, T):
        for i in range(1, Nx + 1):
            for j in range(1, Ny + 1):
                Z[i, j, t] = (2 * Z[i, j, t - 1] - Z[i, j, t - 2] +
                              (c**2 * dt**2 / hx**2) * 
                              (Z[i + 1, j, t - 1] - 2 * Z[i, j, t - 1] + Z[i - 1, j, t - 1]) +
                              (c**2 * dt**2 / hy**2) * 
                              (Z[i, j + 1, t - 1] - 2 * Z[i, j, t - 1] + Z[i, j - 1, t - 1]))

    return Z, X, Y
