# Hernán Barquero Chaves

import numpy as np
from scipy.integrate  import solve_ivp
#######################################################
def proyectil_ideal(x0:float,y0:float,z0:float,vx0:float,vy0:float,vz0:float,g:float,t:np.ndarray):
	"""
	Calcula el vector posición de un proyectil ideal en el espacio 3D con respecto al tiempo.

	Calcula la posición de un objeto denominado proyectil ideal, sin resistencia con el aire y sin interacción con el viento y con un marco de referencia inercical, con respecto al tiempo para un espacio 3D. La función utiliza un marco de referencia en que el eje -Z contiene la dirección del vector de gravedad.

	Args:
		x0 (float): Posición inicial del objeto en el eje x.
		y0 (float): Posición inicial del objeto en el eje y.
		z0 (float): Posición inicial del objeto en el eje z.
		vx0 (float): Velocidad inicial del objeto en el eje x.
		vy0 (float): Velocidad inicial del objeto en el eje x.
		vz0 (float): Velocidad inicial del objeto en el eje x.
		g (float): Magnitud de la aceleración gravitacional.
		t (numpy.ndarray): Puentos temporales que serán utilizados para obtener la posición del objeto.

	Returns:
		r (numpy.ndarray): Vector que contiene las posiciones del objeto en cada paso temporal evaluado (t,x,y,z).
	
	Example:
		>>> import numpy as np
		>>> t = np.linspace(0.0,5.0,100)
		>>> r = proyectil_ideal(0.0,0.0,5.0,0.0,0.0,0.0,9.81,t)
	"""

	xf = x0 + vx0*t
	yf = y0 + vy0*t
	zf = z0 + vz0*t - 0.5*g*t**2
	r = np.array([t,xf,yf,zf])
	return r
#######################################################

#######################################################################################
def proyectil_friccion(x0:float,y0:float,z0:float,vx0:float,vy0:float,vz0:float,g:float,a:float,c:float,m:float,t0:float,tf:float,n:int):
	"""
	Calcula el vector posición de un proyectil no tan ideal en el espacio 3D con respecto al tiempo.

	Calcula la posición de un objeto denominado proyectil no tan ideal, con resistencia con el aire y sin interacción con el viento y con un marco de referencia inercical, con respecto al tiempo para un espacio 3D. La función utiliza un marco de referencia en que el eje -Z contiene la dirección del vector de gravedad.

	Args:
		x0 (float): Posición inicial del objeto en el eje x.
		y0 (float): Posición inicial del objeto en el eje y.
		z0 (float): Posición inicial del objeto en el eje z.
		vx0 (float): Velocidad inicial del objeto en el eje x.
		vy0 (float): Velocidad inicial del objeto en el eje x.
		vz0 (float): Velocidad inicial del objeto en el eje x.
		g (float): Magnitud de la aceleración gravitacional.
		a (float): Coeficiente del término lineal de la resistencia con el aire (Fuerza) $f = -a*v$.
		c (float): Coeficiente del término cuadrático de la resistencia con el aire (Fuerza) $f = -c*v**2$.
		m (float): Masa del objeto.
		t0 float): Tiempo inicial.
		tf (float): Tiempo final.
		n (int): Número de pasos a realizar entre t0 y tf.

	Returns:
		sol (scipy.integrate.solve_ivp): Vector que contiene las posiciones del objeto en cada paso temporal evaluado.
	
	Example:
		>>> sol = proyectil_friccion(0.0,0.0,5.0,0.0,0.0,0.0,9.81,0.025,0.035,10.0,0.0,10.0,1000)
		>>> t = sol.t # Devuelve el vector de tiempo
		>>> r = sol.y # Devuelve el vector posición (x,y,z)
	"""

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
	
	t_n = np.linspace(t0,tf,n)
	condiciones_iniciales = [x0,vx0,y0,vy0,z0,vz0]
	sol = solve_ivp(dSdt, t_span = (t0,tf), t_eval = t_n, y0 = condiciones_iniciales)
	return sol
##############################################################################################

###############################################################################################################################################################
def proyectil_noinercial_friccion(x0:float,y0:float,z0:float,vx0:float,vy0:float,vz0:float,g:float,a:float,c:float,m:float,omega:float,R:float,labbda:float,t0:float,tf:float,n:int):
	"""
	Calcula el vector posición de un proyectil no tan ideal en el espacio 3D con respecto al tiempo.

	Calcula la posición de un objeto denominado proyectil no tan ideal, con resistencia con el aire, con un marco de referencia no inercial y sin interacción con el viento; con respecto al tiempo para un espacio 3D. La función está pensada para estudiar el movimiento de proyectiles en planetas, por lo que espera que se le entregue una velocidad de rotación del planeta, un radio a la superficie donde se encuentra el observador y la colatitud en que se encuentra el observador. Además, la función utiliza un marco de referencia en que el eje -Z contiene la dirección del vector de gravedad.

	Args:
		x0 (float): Posición inicial del objeto en el eje x.
		y0 (float): Posición inicial del objeto en el eje y.
		z0 (float): Posición inicial del objeto en el eje z.
		vx0 (float): Velocidad inicial del objeto en el eje x.
		vy0 (float): Velocidad inicial del objeto en el eje x.
		vz0 (float): Velocidad inicial del objeto en el eje x.
		g (float): Magnitud de la aceleración gravitacional.
		a (float): Coeficiente del término lineal de la resistencia con el aire (Fuerza) $f = -a*v$.
		c (float): Coeficiente del término cuadrático de la resistencia con el aire (Fuerza) $f = -c*v**2$.
		m (float): Masa del objeto.
		omega (float): Velocidad angular de la rotación del planeta.
		R (float): Distancia radial entre el centro del planeta y la ubicación del observador.
		labbda (float): Colatitud en que se encuentra el observador.
		t0 float): Tiempo inicial.
		tf (float): Tiempo final.
		n (int): Número de pasos a realizar entre t0 y tf.

	Returns:
		sol (scipy.integrate.solve_ivp): Vector que contiene las posiciones del objeto en cada paso temporal evaluado.
	
	Example:
		>>> sol = proyectil_friccion(0.0,0.0,5.0,0.0,0.0,0.0,9.81,0.025,0.035,10.0,360.0/(24.0*3600.0),6378.0e3,1.396,0.0,10.0,1000)
		>>> t = sol.t # Devuelve el vector de tiempo
		>>> r = sol.y # Devuelve el vector posición (x,y,z)
	"""


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
	
	t_n = np.linspace(t0,tf,n)
	condiciones_iniciales = [x0,vx0,y0,vy0,z0,vz0]
	extra_argumentos = (g,a,c,m,R,labbda,omega)
	sol = solve_ivp(dSdt, t_span = (t0,tf), t_eval = t_n, y0 = condiciones_iniciales, args = extra_argumentos)
	return sol
###############################################################################################################################################################

def proyectil_noinercial_friccion_forzado(x0:float, y0:float, z0:float, vx0:float, vy0:float, vz0:float, g:float, a:float, c:float, m:float, omega:float, R:float, labbda:float, Fx:callable, Fy:callable, Fz:callable, t0:float, tf:float, n:int):

	"""
	Calcula el vector posición de un proyectil no ideal en el espacio 3D con respecto al tiempo.

	Calcula la posición de un objeto denominado proyectil no tan ideal, con resistencia con el aire, con un marco de referencia no inercial y con interacción con el viento; con respecto al tiempo para un espacio 3D. La función está pensada para estudiar el movimiento de proyectiles en planetas, por lo que espera que se le entregue una velocidad de rotación del planeta, un radio a la superficie donde se encuentra el observador y la colatitud en que se encuentra el observador. Junto a lo anterior, se debe contemplar el campo de fuerza que genere los vientos u otras interacciones que se deseen agregar. Además, la función utiliza un marco de referencia en que el eje -Z contiene la dirección del vector de gravedad.

	Args:
		x0 (float): Posición inicial del objeto en el eje x.
		y0 (float): Posición inicial del objeto en el eje y.
		z0 (float): Posición inicial del objeto en el eje z.
		vx0 (float): Velocidad inicial del objeto en el eje x.
		vy0 (float): Velocidad inicial del objeto en el eje x.
		vz0 (float): Velocidad inicial del objeto en el eje x.
		g (float): Magnitud de la aceleración gravitacional.
		a (float): Coeficiente del término lineal de la resistencia con el aire (Fuerza) $f = -a*v$.
		c (float): Coeficiente del término cuadrático de la resistencia con el aire (Fuerza) $f = -c*v**2$.
		m (float): Masa del objeto.
		omega (float): Velocidad angular de la rotación del planeta.
		R (float): Distancia radial entre el centro del planeta y la ubicación del observador.
		labbda (float): Colatitud en que se encuentra el observador.
		Fx (callable): Componente en el eje X del campo de fuerza.
		Fy (callable): Componente en el eje Y del campo de fuerza.
		Fz (callable): Componente en el eje Z del campo de fuerza.
		t0 float): Tiempo inicial.
		tf (float): Tiempo final.
		n (int): Número de pasos a realizar entre t0 y tf.

	Returns:
		sol (scipy.integrate.solve_ivp): Vector que contiene las posiciones del objeto en cada paso temporal evaluado.
	
	Example:
		>>> def FX(t,x,y,z):
			return x**2
		>>> def FY(t,x,y,z):
			return y
		>>>	def FZ(t,x,y,z):
			return z**-1

		>>> sol = proyectil_friccion(0.0,0.0,5.0,0.0,0.0,0.0,9.81,0.025,0.035,10.0,360.0/(24.0*3600.0),6378.0e3,1.396,FX,FY,FZ,0.0,10.0,1000)
		>>> t = sol.t # Devuelve el vector de tiempo
		>>> r = sol.y # Devuelve el vector posición (x,y,z)
	"""

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
