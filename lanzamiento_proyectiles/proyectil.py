# Hernán Barquero Chaves

import numpy as np
import scipy as sp
#######################################################
def proyectil_ideal(x0,y0,z0,vx0,vy0,vz0,g,t):
    xf = x0 + vx0*t
    yf = y0 + vy0*t
    zf = z0 + vz0*t - (1/2)*g*t**2
    r = np.array([t,xf,yf,zf])
    return r
#######################################################

#######################################################################################
def proyectil_friccion(x0,y0,z0,vx0,vy0,vz0,g,a,c,m,t0,tf,n):
    # Funciones de aceleración considerando la fricción
    def max(vx, vy, vz):
        return -a*vx - c*np.sqrt(vx**2 + vy**2 + vz**2) * vx

    def may(vx, vy, vz):
        return -a*vy - c*np.sqrt(vx**2 + vy**2 + vz**2) * vy

    def maz(vx, vy, vz):
        return -m*g - a*vz - c*np.sqrt(vx**2 + vy**2 + vz**2) * vz
    

    # Definir la función de derivadas del sistema
    def dSdt(t, S):
        x, vx, y, vy, z, vz = S
        ax = max(vx, vy, vz) / m
        ay = may(vx, vy, vz) / m
        az = maz(vx, vy, vz) / m
        return [vx, ax, vy, ay, vz, az]
    

    from scipy.integrate  import solve_ivp
    t_n = np.linspace(t0,tf,n)
    condiciones_iniciales = [x0,vx0,y0,vy0,z0,vz0]
    sol = solve_ivp(dSdt, t_span = (t0,tf), t_eval = t_n, y0 = condiciones_iniciales)
    return sol
##############################################################################################

######################################################################################################################################################################
def proyectil_noinercial_friccion(x0,y0,z0,vx0,vy0,vz0,g,a,c,m,omega,R,labbda,t0,tf,n):
    # vector de velocidad angular del planeta
    omega_vector = np.array([-omega*np.sin(labbda),0,omega*np.cos(labbda)])


    # Funciones de aceleración considerando la fricción
    def max(x,vx, y,vy, z,vz):
        return -a*vx - c*np.sqrt(vx**2 + vy**2 + vz**2) * vx -2*m*omega*(vz*np.sin(labbda) - vy*np.cos(labbda)) +m*omega**2 * x**2

    def may(x,vx, y,vy, z,vz):
        return -a*vy - c*np.sqrt(vx**2 + vy**2 + vz**2) * vy -2*m*omega*np.cos(labbda)*vx - m*omega**2 *np.cos(labbda)*((z+ R)*np.sin(labbda) - y*np.cos(labbda))

    def maz(x,vx, y,vy, z,vz):
        return -m*g - a*vz - c*np.sqrt(vx**2 + vy**2 + vz**2) * vz +2*m*omega*np.sin(labbda)*vx + m*omega**2 *np.sin(labbda)*((z+R)*np.sin(labbda) - y*np.cos(labbda))
    
    # Definir la función de derivadas del sistema
    def dSdt(t, S,g,a,c,m,R,labbda,omega):
        x, vx, y, vy, z, vz = S
        ax = max(x,vx, y,vy, z,vz) / m
        ay = may(x,vx, y,vy, z,vz) / m
        az = maz(x,vx, y,vy, z,vz) / m
        return [vx, ax, vy, ay, vz, az]
    
    from scipy.integrate  import solve_ivp
    t_n = np.linspace(t0,tf,n)
    condiciones_iniciales = [x0,vx0,y0,vy0,z0,vz0]
    extra_argumentos = (g,a,c,m,R,labbda,omega)
    sol = solve_ivp(dSdt, t_span = (t0,tf), t_eval = t_n, y0 = condiciones_iniciales, args = extra_argumentos)
    return sol
########################################################################################################################################################################

def proyectil_noinercial_friccion_forzado(x0, y0, z0, vx0, vy0, vz0, g, a, c, m, omega, R, labbda, Fx, Fy, Fz, t0, tf, n):
    import numpy as np
    from scipy.integrate import solve_ivp

    # Funciones de aceleración considerando la fricción y el sistema no inercial
    def max(x, vx, y, vy, z, vz):
        return -a * vx - c * np.sqrt(vx**2 + vy**2 + vz**2) * vx - 2 * m * omega * (vz * np.sin(labbda) - vy * np.cos(labbda)) + m * omega**2 * x

    def may(x, vx, y, vy, z, vz):
        return -a * vy - c * np.sqrt(vx**2 + vy**2 + vz**2) * vy - 2 * m * omega * np.cos(labbda) * vx - m * omega**2 * np.cos(labbda) * ((z + R) * np.sin(labbda) - y * np.cos(labbda))

    def maz(x, vx, y, vy, z, vz):
        return -m * g - a * vz - c * np.sqrt(vx**2 + vy**2 + vz**2) * vz + 2 * m * omega * np.sin(labbda) * vx + m * omega**2 * np.sin(labbda) * ((z + R) * np.sin(labbda) - y * np.cos(labbda))

    # Definir la función de derivadas del sistema
    def dSdt(t, S):
        x, vx, y, vy, z, vz = S
        ax = (max(x, vx, y, vy, z, vz) + Fx(t, x, y, z)) / m
        ay = (may(x, vx, y, vy, z, vz) + Fy(t, x, y, z)) / m
        az = (maz(x, vx, y, vy, z, vz) + Fz(t, x, y, z)) / m
        return [vx, ax, vy, ay, vz, az]

    # Crear un rango de tiempo con más puntos evaluados
    t_n = np.linspace(t0, tf, n)
    condiciones_iniciales = [x0, vx0, y0, vy0, z0, vz0]

    # Resolver el sistema de ecuaciones diferenciales
    sol = solve_ivp(dSdt, t_span=(t0, tf), t_eval=t_n, y0=condiciones_iniciales, method='RK45', rtol=1e-8, atol=1e-10)

    return sol
