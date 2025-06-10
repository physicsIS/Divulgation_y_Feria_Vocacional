import matplotlib.pyplot as plt
from typing import List, Optional


# Definición de la clase Estado
class Estado:
	"""
	Representa un estado termodinámico de un sistema.

	Attributes:
		nombre (str): Nombre identificador del estado.
		modelo (ModeloTermodinamico): Modelo termodinámico asociado.
		P (float): Presión en Pa.
		T (float): Temperatura en Kelvin.
		v (float): Volumen específico en m³/kg.
		u (float): Energía interna específica en J/kg.
		h (float): Entalpía específica en J/kg.
		s (float): Entropía específica en J/kg·K.
	"""


	def __init__(self, modelo, nombre=""):
		"""
		Inicializa el estado con un modelo y un nombre.

		Args:
			modelo (ModeloTermodinamico): Modelo para calcular propiedades.
			nombre (str, optional): Nombre del estado. Por defecto "".
		"""
		self.nombre = nombre
		self.modelo = modelo
		
		# Propiedades termodinámicas
		self.P = None # Presion Pa
		self.T = None # Temperatura k
		self.v = None # Volumen especifico
		self.u = None # Energia interna especifica
		self.h = None # Entalpia especifica
		self.s = None # Entropia especifica

	def actualizar(self, **kwargs):
		"""
		Actualiza las propiedades del estado usando el modelo asociado.

		Args:
			**kwargs: Propiedades conocidas (por ejemplo, P, T, s, h...).
		"""
		self.modelo.calcular_estado(self, **kwargs)

	def resumen(self):
		"""
		Devuelve un resumen legible del estado actual.

		Returns:
			str: Descripción con las propiedades termodinámicas.
		"""
		return (f"{self.nombre}: P={self.P:.2f} Pa, T={self.T:.2f} K, "
				f"v={self.v:.5f} m³/kg,u={self.u:.2f} J/kg, h={self.h:.2f} J/kg, s={self.s:.2f} J/kg·K")
	
# Definición de la clase CicloTermodinamico
class CicloTermodinamico:
	"""
	Representa un ciclo compuesto por una serie de estados termodinámicos.

	Atributes:
		modelo (ModeloTermodinamico): Modelo termodinámico utilizado.
		estados (list[Estado]): Lista de estados que componen el ciclo.
	"""

	def __init__(self, modelo):
		self.modelo = modelo
		self.estados = []

	def agregar_estado(self, nombre, **kwargs):
		"""
		Crea y agrega un nuevo estado al ciclo.

		Args:
			nombre (str): Nombre identificador del estado.
			**kwargs: Propiedades conocidas para calcular el estado.
		"""
		estado = Estado(self.modelo, nombre)
		estado.actualizar(**kwargs)
		self.estados.append(estado)

	def mostrar_ciclo(self):
		"""
		Muestra por pantalla un resumen de todos los estados en el ciclo.
		"""
		for estado in self.estados:
			print(estado.resumen())




	def diagrama_Ts(self, ax=None, **kwargs):
		"""
		Grafica el diagrama Temperatura vs Entropía (T-s) para el ciclo.

		Args:
			ax (matplotlib.axes.Axes, optional): Eje donde dibujar.
			**kwargs: Argumentos adicionales para plt.subplots().

		Returns:
			matplotlib.axes.Axes: Eje con la gráfica.
		"""
		if ax is None:
			fig, ax = plt.subplots(**kwargs)

		T = [e.T for e in self.estados if e.T is not None and e.s is not None]
		s = [e.s for e in self.estados if e.T is not None and e.s is not None]
		nombres = [e.nombre for e in self.estados if e.T is not None and e.s is not None]

		# Cerrar el ciclo conectando el último punto con el primero
		T.append(T[0])
		s.append(s[0])

		ax.plot(s, T, 'b-o', linewidth=2, markersize=8)
		
		for i, txt in enumerate(nombres):
			ax.annotate(txt, (s[i], T[i]), textcoords="offset points", xytext=(5,5), ha='center')

		ax.set_xlabel("Entropía [J/kg·K]")
		ax.set_ylabel("Temperatura [K]")
		ax.set_title("Diagrama T-s")
		ax.grid(True, linestyle='--', alpha=0.7)
		
		return ax

	def diagrama_Pv(self, ax=None, **kwargs):
		"""
		Grafica el diagrama Presión vs Volumen específico (P-v) para el ciclo.

		Args:
			ax (matplotlib.axes.Axes, optional): Eje donde dibujar.
			**kwargs: Argumentos adicionales para plt.subplots().

		Returns:
			matplotlib.axes.Axes: Eje con la gráfica.
		"""
		if ax is None:
			fig, ax = plt.subplots(**kwargs)

		P = [e.P for e in self.estados if e.P is not None and e.v is not None]
		v = [e.v for e in self.estados if e.P is not None and e.v is not None]
		nombres = [e.nombre for e in self.estados if e.P is not None and e.v is not None]

		# Cerrar el ciclo conectando el último punto con el primero
		P.append(P[0])
		v.append(v[0])

		ax.plot(v, P, 'r-o', linewidth=2, markersize=8)
		
		for i, txt in enumerate(nombres):
			ax.annotate(txt, (v[i], P[i]), textcoords="offset points", xytext=(5,5), ha='center')

		ax.set_xlabel("Volumen específico [m³/kg]")
		ax.set_ylabel("Presión [Pa]")
		ax.set_title("Diagrama P-v")
		ax.grid(True, linestyle='--', alpha=0.7)
		
		return ax

	def diagrama_hs(self, ax=None, **kwargs):
		"""
		Grafica el diagrama Entalpía vs Entropía (h-s) para el ciclo.

		Args:
			ax (matplotlib.axes.Axes, optional): Eje donde dibujar.
			**kwargs: Argumentos adicionales para plt.subplots().

		Returns:
			matplotlib.axes.Axes: Eje con la gráfica.
		"""
		if ax is None:
			fig, ax = plt.subplots(**kwargs)

		h = [e.h for e in self.estados if e.h is not None and e.s is not None]
		s = [e.s for e in self.estados if e.h is not None and e.s is not None]
		nombres = [e.nombre for e in self.estados if e.h is not None and e.s is not None]

		# Cerrar el ciclo conectando el último punto con el primero
		h.append(h[0])
		s.append(s[0])

		ax.plot(s, h, 'g-o', linewidth=2, markersize=8)
		
		for i, txt in enumerate(nombres):
			ax.annotate(txt, (s[i], h[i]), textcoords="offset points", xytext=(5,5), ha='center')

		ax.set_xlabel("Entropía [J/kg·K]")
		ax.set_ylabel("Entalpía [J/kg]")
		ax.set_title("Diagrama h-s (Mollier)")
		ax.grid(True, linestyle='--', alpha=0.7)
		
		return ax

	def graficar_diagramas(self):
		"""
		Grafica los diagramas T-s, P-v y h-s en una sola figura.
		"""
		fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
		
		self.diagrama_Ts(ax=ax1)
		self.diagrama_Pv(ax=ax2)
		self.diagrama_hs(ax=ax3)
		
		plt.tight_layout()
		return fig





'''
	def diagrama_Ts(self, ax=None):
		"""
		Grafica el diagrama Temperatura vs Entropía (T-s) para un ciclo termodinámico.

		Args:
			ciclo (CicloTermodinamico): Ciclo que contiene los estados a graficar.
			ax (matplotlib.axes.Axes, optional): Eje de matplotlib donde dibujar. Si no se proporciona, se crea uno nuevo.

		Returns:
			matplotlib.axes.Axes: Objeto Axes con la gráfica generada.
		"""

		if ax is None:
			fig, ax = plt.subplots()

		T = [e.T for e in self.estados if e.T is not None and e.s is not None]
		s = [e.s for e in self.estados if e.T is not None and e.s is not None]
		nombres = [e.nombre for e in self.estados if e.T is not None and e.s is not None]

		ax.plot(s, T, marker='o')
		for i, txt in enumerate(nombres):
			ax.annotate(txt, (s[i], T[i]))

		ax.set_xlabel("Entropía [J/kg·K]")
		ax.set_ylabel("Temperatura [K]")
		ax.set_title("Diagrama T-s")
		ax.grid(True)

		return ax
	
	def diagrama_Pv(self, ax=None):
		"""
		Grafica el diagrama Presión vs Volumen específico (P-v) para un ciclo termodinámico.

		Args:
			ciclo (CicloTermodinamico): Ciclo que contiene los estados a graficar.
			ax (matplotlib.axes.Axes, optional): Eje de matplotlib donde dibujar. Si no se proporciona, se crea uno nuevo.

		Returns:
			matplotlib.axes.Axes: Objeto Axes con la gráfica generada.
		"""

		if ax is None:
			fig, ax = plt.subplots()

		P = [e.P for e in self.estados if e.P is not None and e.v is not None]
		v = [e.v for e in self.estados if e.P is not None and e.v is not None]
		nombres = [e.nombre for e in self.estados if e.P is not None and e.v is not None]

		ax.plot(v, P, marker='o')
		for i, txt in enumerate(nombres):
			ax.annotate(txt, (v[i], P[i]))

		ax.set_xlabel("Volumen específico [m³/kg]")
		ax.set_ylabel("Presión [Pa]")
		ax.set_title("Diagrama P-v")
		ax.grid(True)

		return ax
	
	def diagrama_hs(self, ax=None):
		"""
		Grafica el diagrama Entalpía vs Entropía (h-s) para un ciclo termodinámico.

		Args:
			ciclo (CicloTermodinamico): Ciclo que contiene los estados a graficar.
			ax (matplotlib.axes.Axes, optional): Eje de matplotlib donde dibujar. Si no se proporciona, se crea uno nuevo.

		Returns:
			matplotlib.axes.Axes: Objeto Axes con la gráfica generada.
		"""


		if ax is None:
			fig, ax = plt.subplots()

		h = [e.h for e in self.estados if e.h is not None and e.s is not None]
		s = [e.s for e in self.estados if e.h is not None and e.s is not None]
		nombres = [e.nombre for e in self.estados if e.h is not None and e.s is not None]

		ax.plot(s, h, marker='o')
		for i, txt in enumerate(nombres):
			ax.annotate(txt, (s[i], h[i]))

		ax.set_xlabel("Entropía [J/kg·K]")
		ax.set_ylabel("Entalpía [J/kg]")
		ax.set_title("Diagrama h-s")
		ax.grid(True)

		return ax
'''
