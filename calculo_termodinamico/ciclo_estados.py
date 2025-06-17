import matplotlib.pyplot as plt
import numpy as np

# Definición de la clase estado
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


	def __init__(self, modelo, nombre=0):
		"""
		Inicializa el estado con un modelo y un nombre.

		Args:
			modelo (ModeloTermodinamico): Modelo para calcular propiedades. 
			nombre (str, optional): Nombre del estado. Por defecto "". Corresponde al numero (int) del estado, mas que un nombre es un identificador.
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
		Asigna las propiedades conocidas de un estado a su respectivo objeto.

		Args:
			**kwargs: Propiedades conocidas (por ejemplo, P, T, s, h...).
		"""
		
		# A continuacion se presentan los casos que va a revisar el programa si se tiene los datos y calcula los datos faltantes si es posible
		
		atributos_validos = ['P', 'T', 'v', 'u', 'h', 's']
		for key, value in kwargs.items():
			if key in atributos_validos:
				setattr(self, key, value)
			else:
				raise AttributeError(f"'{key}' no es una propiedad válida del estado.")

	def calcular_propiedades(self):
		'''
		Calcula las propiedades termodinamicas de los estados del ciclo.
		'''
		self.modelo.calcular_estado(self)

	def resumen(self):
		"""
		Devuelve un resumen legible del self actual.

		Returns:
			str: Descripción con las propiedades termodinámicas.
		"""
		def format_prop(prop, unidad=""):
			return f"{prop:.2f} {unidad}" if prop is not None else "N/A"

		return (f"{self.nombre}: P={format_prop(self.P, 'Pa')}, T={format_prop(self.T, 'K')}, "
				f"v={format_prop(self.v, 'm³/kg')}, u={format_prop(self.u, 'J/kg')}, "
				f"h={format_prop(self.h, 'J/kg')}, s={format_prop(self.s, 'J/kg·K')}")
	
# Definición de la clase CicloTermodinamico
class CicloTermodinamico:
	"""
	Representa un ciclo compuesto por una serie de estados termodinámicos.

	Atributes:
		modelo (ModeloTermodinamico): Modelo termodinámico utilizado.
		n_estados (int): Número de estados que conforman el ciclo.
		n_values (int): Número de estados internos a cada proceso del ciclo. Default n_values = 35
		estados (list[Estado]): Lista de estados que componen el ciclo.
	"""

	def __init__(self, modelo,n_estados, n_values = 35):
		self.modelo = modelo
		self.n_values = n_values
		self.estados = np.empty(n_estados, dtype=object) # Se conocen la cantidad de estados que tiene el ciclo
		self.estados_internos = np.empty((n_estados,n_values), dtype=object) # Se genera una lista para los estados internos entre cada proceso.
		self._indice_estado_actual = 0  # Contador de estado
		self._indice_proceso_actual = 0 # Contador de proceso

	def agregar_estado(self, nombre, **kwargs):
		"""
		Crea y agrega un nuevo estado al ciclo. Se espera que se coloquen en el orden que se va a recorrer el ciclo.

		Args:
			nombre (str): Nombre identificador del estado.
			**kwargs: Propiedades conocidas para calcular el estado.
		"""

		if self._indice_estado_actual >= len(self.estados):
			raise IndexError("Se han agregado más estados de los permitidos.")

		estado = Estado(self.modelo, nombre)
		estado.actualizar(**kwargs)
		self.estados[self._indice_estado_actual] = estado
		self._indice_estado_actual +=1

	def _generar_estado_interno(self, **kwargs):
		"""
		Genera un nuevo estado interno a un proceso del ciclo.

		Args:
			**kwargs: Propiedades conocidas para calcular el estado.
		"""
		estado_interno = Estado(self.modelo)
		estado_interno.actualizar(**kwargs)
		estado_interno.calcular_propiedades()
		return estado_interno

	def proceso_isocorico(self, estado_in, estado_out):
		'''
		Relaciona dos estados de un ciclo termodinámico mediante un proceso isocórico o a volumen constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''

		result = self.modelo.resolver_isocorico(estado_in,estado_out)
		P_values = np.linspace(np.min([estado_in.P,estado_out.P]), np.max([estado_in.P,estado_out.P]), self.n_values)
		T_values = result(P_values)
		for i in range(self.n_values):
			self.estados_internos[estado_in.nombre-1][i] = self._generar_estado_interno(P = P_values[i], T=T_values[i])

		
		self._indice_proceso_actual += 1

	def proceso_isotermico(self, estado_in, estado_out):
		'''
		Relaciona dos estados de un ciclo termodinámico mediante un proceso isotérmico o a temperatura constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''

		result = self.modelo.resolver_isotermico(estado_in,estado_out)
		v_values = np.linspace(np.min([estado_in.v,estado_out.v]), np.max([estado_in.v,estado_out.v]), self.n_values)
		P_values = result(v_values)
		for i in range(self.n_values):
			self.estados_internos[estado_in.nombre-1][i] = self._generar_estado_interno(v = v_values[i], P=P_values[i])

		self._indice_proceso_actual += 1

	def proceso_isobarico(self, estado_in, estado_out):
		'''
		Relaciona dos estados de un ciclo termodinámico mediante un proceso isobárico o a presión constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''

		result = self.modelo.resolver_isobarico(estado_in,estado_out)
		v_values = np.linspace(np.min([estado_in.v,estado_out.v]), np.max([estado_in.v,estado_out.v]), self.n_values)
		T_values = result(v_values)
		for i in range(self.n_values):
			self.estados_internos[estado_in.nombre-1][i] = self._generar_estado_interno(v = v_values[i], T=T_values[i])
		
		self._indice_proceso_actual += 1

	def proceso_isoentalipico(self, estado_in, estado_out):
		'''
		Relaciona dos estados de un ciclo termodinámico mediante un proceso isoentálpico o a entalpía constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''

		result = self.modelo.resolver_isoentalpico(estado_in,estado_out)
		v_values = np.linspace(np.min([estado_in.v,estado_out.v]), np.max([estado_in.v,estado_out.v]), self.n_values)
		P_values = result(v_values)
		for i in range(self.n_values):
			self.estados_internos[estado_in.nombre-1][i] = self._generar_estado_interno(v = v_values[i], P=P_values[i])
		
		self._indice_proceso_actual += 1

	def proceso_isoentropico(self, estado_in, estado_out):
		'''
		Relaciona dos estados de un ciclo termodinámico mediante un proceso isoentrópico o a entropía constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''

		result = self.modelo.resolver_isoentropico(estado_in,estado_out)
		v_values = np.linspace(np.min([estado_in.v,estado_out.v]), np.max([estado_in.v,estado_out.v]), self.n_values)
		P_values = result(v_values)
		for i in range(self.n_values):
			self.estados_internos[estado_in.nombre-1][i] = self._generar_estado_interno(v=v_values[i], P = P_values[i])

		self._indice_proceso_actual += 1

	def proceso_in_or_out_calor(self,estado_in, estado_out, calor):
		'''
		Relaciona dos estados de un ciclo termodinámico mediante un proceso de adicion o rechazo de calor a temperatura constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
			calor (float): Calor de entrada (positivo) o salida (negativo) del proceso.
		'''
		result = self.modelo.resolver_in_or_out_calor(estado_in, estado_out, calor)
		v_values = np.linspace(np.min([estado_in.v,estado_out.v]), np.max([estado_in.v,estado_out.v]), self.n_values)
		P_values = result(v_values)
		for i in range(self.n_values):
			self.estados_internos[estado_in.nombre-1][i] = self._generar_estado_interno(v=v_values[i], P = P_values[i])
	
		self._indice_proceso_actual += 1

	"""def proceso_interenfriamiento_recalentamiento(self,estado_in, estado_out, delta_T):
		'''
		Relaciona dos estados de un ciclo termodinámico mediante un proceso de adicion o rechazo de calor con un cambio de temperatura determinado.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
			calor (float): Calor de entrada (positivo) o salida (negativo) del proceso.
		'''
		result = self.modelo.resolver_interenfriamiento_recalentamiento(estado_in, estado_out, delta_T)
		v_values = np.linspace(np.min([estado_in.v,estado_out.v]), np.max([estado_in.v,estado_out.v]), self.n_values)
		T_values = result(v_values)
		for i in range(self.n_values):
			self.estados_internos[estado_in.nombre-1][i] = self._generar_estado_interno(v=v_values[i], T = T_values[i])
	
		self._indice_proceso_actual += 1 """


	def mostrar_ciclo(self):
		"""
		Muestra por pantalla un resumen de todos los estados en el ciclo.
		"""
		for estado in self.estados:
			print(estado.resumen())

	def graficar_diagrama_Ts(self, nombre_ciclo="Ciclo termodinámico", ax=None):
		"""
		Grafica el diagrama T-s del ciclo termodinámico.

		Args:
			nombre_ciclo (str): Título del gráfico.
			ax (matplotlib.axes.Axes, opcional): Eje sobre el que se grafica. Si no se proporciona, se crea uno nuevo.

		Returns:
			fig, ax: Figura y eje del gráfico.
		"""
		if ax is None:
			fig, ax = plt.subplots(figsize=(6, 4))
		else:
			fig = ax.figure

		colores = plt.cm.tab10.colors

		# Graficar tramos y puntos intermedios
		for i, tramo in enumerate(self.estados_internos):
			s_vals = [estado.s for estado in tramo if estado is not None]
			T_vals = [estado.T for estado in tramo if estado is not None]
			ax.plot(s_vals, T_vals, color=colores[i % len(colores)],
					label=f"Tramo {i+1} → {i+2 if i+2 <= len(self.estados) else 1}")
			ax.scatter(s_vals, T_vals, color=colores[i % len(colores)], s=20)

		# Estados principales
		for estado in self.estados:
			if estado is not None:
				ax.scatter(estado.s, estado.T, color='black', s=60,
							edgecolor='white', zorder=5)
				ax.annotate(text=estado.nombre, xy = (estado.s + estado.s/100,estado.T + estado.T/100))

		# Estética
		ax.set_xlabel('Entropía específica [J/kg·K]')
		ax.set_ylabel('Temperatura [K]')
		ax.set_title(f'Diagrama T-s: {nombre_ciclo}')
		ax.grid(True)
		ax.legend()
		fig.tight_layout()

		return fig, ax
	
	def graficar_diagrama_Pv(self, nombre_ciclo="Ciclo termodinámico", ax=None):
		"""
		Grafica el diagrama P-v del ciclo termodinámico.

		Args:
			nombre_ciclo (str): Título del gráfico.
			ax (matplotlib.axes.Axes, opcional): Eje sobre el que se grafica. Si no se proporciona, se crea uno nuevo.

		Returns:
			fig, ax: Figura y eje del gráfico.
		"""
		import matplotlib.pyplot as plt

		if ax is None:
			fig, ax = plt.subplots(figsize=(6, 4))
		else:
			fig = ax.figure

		colores = plt.cm.tab10.colors

		# Graficar tramos y puntos intermedios
		for i, tramo in enumerate(self.estados_internos):
			v_vals = [estado.v for estado in tramo if estado is not None]
			P_vals = [estado.P for estado in tramo if estado is not None]
			ax.plot(v_vals, P_vals, color=colores[i % len(colores)],
					label=f"Tramo {i+1} → {i+2 if i+2 <= len(self.estados) else 1}")
			ax.scatter(v_vals, P_vals, color=colores[i % len(colores)], s=20)

		# Estados principales
		for estado in self.estados:
			if estado is not None:
				ax.scatter(estado.v, estado.P, color='black', s=60,
						edgecolor='white', zorder=5)
				ax.annotate(text=estado.nombre, xy = (estado.v + estado.v/100,estado.P + estado.P/100))

		# Estética
		ax.set_xlabel(r'Volumen específico [$m^3$/kg]')
		ax.set_ylabel('Presión [Pa]')
		ax.set_title(f'Diagrama P-v: {nombre_ciclo}')
		ax.grid(True)
		ax.legend()
		fig.tight_layout()

		return fig, ax