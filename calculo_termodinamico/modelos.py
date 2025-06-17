import numpy as np

class ModeloTermodinamico:
	"""
	Clase base abstracta para modelos termodinámicos.

	Métodos:
		resolver_xxxxxx(self, estado_in, estado_out, **kwargs): Resuelve el respectivo proceso, tal que se definan las variables termodinámicas de cada estado.
		calcular_estado(estado, **kwargs): Calcula las propiedades termodinámicas de un estado.
	"""

	def resolver_isocorico(self, estado_in, estado_out):
		'''
		Esta función relaciona dos estados a través de un proceso isocórico o a volumen constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''
		# Definir alguno de los estados involucrados si es posible:
		if sum(value is not None for value in vars(estado_in).values()) >= 2:
			if sum(value is not None for value in vars(estado_in).values()) ==6:
				print(f"{estado_in.nombre} esta definido")
			else:
				self.calcular_estado(estado_in)
		elif sum(value is not None for value in vars(estado_out).values()) >= 2:
			if sum(value is not None for value in vars(estado_out).values()) ==6:
				print(f"{estado_out.nombre} esta definido")
			else:
				self.calcular_estado(estado_out)

		# Ambos están definidos
		if estado_in.v is not None and estado_out.v is not None:
			if estado_in.v == estado_out.v:
				print(f"Los volúmenes de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos y son iguales.")
			else:
				print(f"Los volúmenes de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos pero no son iguales. Se recomienda revisar.")
		
		# Solo el estado_in tiene volumen definido
		elif estado_in.v is not None:
			estado_out.v = estado_in.v
		
		# Solo el estado_out tiene volumen definido
		elif estado_out.v is not None:
			estado_in.v = estado_out.v
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene el volumen definido. Se requiere al menos uno.")

	def resolver_isotermico(self, estado_in, estado_out):
		'''
		Esta función relaciona dos estados a través de un proceso isotermico o a temperatura constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''
		# Definir alguno de los estados involucrados si es posible:
		if sum(value is not None for value in vars(estado_in).values()) >= 2:
			if sum(value is not None for value in vars(estado_in).values()) ==6:
				print(f"{estado_in.nombre} esta definido")
			else:
				self.calcular_estado(estado_in)
		elif sum(value is not None for value in vars(estado_out).values()) >= 2:
			if sum(value is not None for value in vars(estado_out).values()) ==6:
				print(f"{estado_out.nombre} esta definido")
			else:
				self.calcular_estado(estado_out)
	
		# Ambos están definidos
		if estado_in.T is not None and estado_out.T is not None:
			if estado_in.T == estado_out.T:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas y son iguales.")
			else:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas pero no son iguales. Se recomienda revisar.")
		
		# Solo el estado_in tiene volumen definido
		elif estado_in.T is not None:
			estado_out.T = estado_in.T
		
		# Solo el estado_out tiene volumen definido
		elif estado_out.T is not None:
			estado_in.T = estado_out.T
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene la temperatura definida. Se requiere al menos una.")

	def resolver_isobarico(self,estado_in, estado_out):
		'''
		Esta función relaciona dos estados a través de un proceso isobarico o a presión constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''
		# Definir alguno de los estados involucrados si es posible:
		if sum(value is not None for value in vars(estado_in).values()) >= 2:
			if sum(value is not None for value in vars(estado_in).values()) ==6:
				print(f"{estado_in.nombre} esta definido")
			else:
				self.calcular_estado(estado_in)
		elif sum(value is not None for value in vars(estado_out).values()) >= 2:
			if sum(value is not None for value in vars(estado_out).values()) ==6:
				print(f"{estado_out.nombre} esta definido")
			else:
				self.calcular_estado(estado_out)

		if estado_in.P is not None and estado_out.P is not None:
			if estado_in.P == estado_out.P:
				print(f"Las presiones de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas y son iguales.")
			else:
				print(f"Las presiones de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas pero no son iguales. Se recomienda revisar.")
		
		# Solo el estado_in tiene volumen definido
		elif estado_in.P is not None:
			estado_out.P = estado_in.P
		
		# Solo el estado_out tiene volumen definido
		elif estado_out.P is not None:
			estado_in.P = estado_out.P
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene la presión definida. Se requiere al menos una.")
	
	def resolver_isoentalpico(self, estado_in, estado_out):
		'''
		Esta función relaciona dos estados a través de un proceso isoentalpico o a entalpía constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''
		# Definir alguno de los estados involucrados si es posible:
		if sum(value is not None for value in vars(estado_in).values()) >= 2:
			if sum(value is not None for value in vars(estado_in).values()) ==6:
				print(f"{estado_in.nombre} esta definido")
			else:
				self.calcular_estado(estado_in)
		elif sum(value is not None for value in vars(estado_out).values()) >= 2:
			if sum(value is not None for value in vars(estado_out).values()) ==6:
				print(f"{estado_out.nombre} esta definido")
			else:
				self.calcular_estado(estado_out)

		# Ambos están definidos
		if estado_in.h is not None and estado_out.h is not None:
			if estado_in.h == estado_out.h:
				print(f"Las entalpias de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas y son iguales.")
			else:
				print(f"Las entalpias de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas pero no son iguales. Se recomienda revisar.")
		
		# Solo el estado_in tiene volumen definido
		elif estado_in.h is not None:
			estado_out.h = estado_in.h
		
		# Solo el estado_out tiene volumen definido
		elif estado_out.h is not None:
			estado_in.h = estado_out.h
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene la entalpía definida. Se requiere al menos una.")

	def resolver_isoentropico(self, estado_in, estado_out):
		'''
		Esta función relaciona dos estados a través de un proceso isoentropico o a entropía constante.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''
		# Definir alguno de los estados involucrados si es posible:
		if sum(value is not None for value in vars(estado_in).values()) >= 2:
			if sum(value is not None for value in vars(estado_in).values()) ==6:
				print(f"{estado_in.nombre} esta definido")
			else:
				self.calcular_estado(estado_in)
		elif sum(value is not None for value in vars(estado_out).values()) >= 2:
			if sum(value is not None for value in vars(estado_out).values()) ==6:
				print(f"{estado_out.nombre} esta definido")
			else:
				self.calcular_estado(estado_out)

		# Ambos están definidos
		if estado_in.s is not None and estado_out.s is not None:
			if estado_in.s == estado_out.s:
				print(f"Las entropías de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas y son iguales.")
			else:
				print(f"Las entropías de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas pero no son iguales. Se recomienda revisar.")
		
		# Solo el estado_in tiene volumen definido
		elif estado_in.s is not None:
			estado_out.s = estado_in.s
		
		# Solo el estado_out tiene volumen definido
		elif estado_out.s is not None:
			estado_in.s = estado_out.s
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene la entropía definida. Se requiere al menos una.")

	def resolver_politropico(self, estado_in, estado_out, n):
		raise NotImplementedError()
	
	def resolver_in_or_out_calor(self, estado_in, estado_out, calor):
		'''
		Esta función relaciona dos estados a través de agregar o sacar calor a temperatura constante.

		La funcion maneja la convencion de que el calor entrante es positivo y el calor saliente es negativo.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
		'''
		# Definir alguno de los estados involucrados si es posible:
		if sum(value is not None for value in vars(estado_in).values()) >= 2:
			if sum(value is not None for value in vars(estado_in).values()) ==6:
				print(f"{estado_in.nombre} esta definido")
			else:
				self.calcular_estado(estado_in)
		elif sum(value is not None for value in vars(estado_out).values()) >= 2:
			if sum(value is not None for value in vars(estado_out).values()) ==6:
				print(f"{estado_out.nombre} esta definido")
			else:
				self.calcular_estado(estado_out)

		# Revisar que las temperatura de los estados sean la misma

		# Ambos están definidos
		if estado_in.T is not None and estado_out.T is not None:
			if estado_in.T == estado_out.T:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas y son iguales.")
			else:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas pero no son iguales. Se recomienda revisar.")
		
		# Solo el estado_in tiene temperatura definido
		elif estado_in.T is not None:
			estado_out.T = estado_in.T
		
		# Solo el estado_out tiene temperatura definido
		elif estado_out.T is not None:
			estado_in.T = estado_out.T
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene la temperatura definida. Se requiere al menos una.")
	
	""" def resolver_interenfriamiento_recalentamiento(self, estado_in, estado_out, delta_T):
		'''
		Esta función relaciona dos estados a través de agregar o sacar calor con un cambio conocido de T.

		La funcion maneja la convencion de que el calor entrante es positivo y el calor saliente es negativo.

		Args:
			estado_in (Estado): Estado de entrada en la secuencia del ciclo.
			estado_out (Estado): Estado de salida en la secuencia del ciclo.
			delta_T (float): Cambio de temperatura estado_out.T - estado_in.T.
		'''
		# Definir alguno de los estados involucrados si es posible:
		if sum(value is not None for value in vars(estado_in).values()) >= 2:
			if sum(value is not None for value in vars(estado_in).values()) ==6:
				print(f"{estado_in.nombre} esta definido")
			else:
				self.calcular_estado(estado_in)
		elif sum(value is not None for value in vars(estado_out).values()) >= 2:
			if sum(value is not None for value in vars(estado_out).values()) ==6:
				print(f"{estado_out.nombre} esta definido")
			else:
				self.calcular_estado(estado_out)

		# Revisar que las temperatura de los estados sean la misma

		# Ambos están definidos
		if estado_in.T is not None and estado_out.T is not None:
			if (estado_in.T - estado_out.T) < 1e-6:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas y son iguales. Se recomienda revisar, no es el comportamiento esperado para este proceso.")
				if estado_in.P is not None and estado_out.P is not None:
					if (estado_in.P - estado_out.P)<1e-6:
						print(f"Las presiones de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos y son iguales. Correcto para un proceso de interenfriamiento o recalentamiento")
						print("No es posible calcular el proceso ni definir los estados.")
					else:
						print(f"Las presiones de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos y NO SON IGUALES. NO ES congruente con el proceso de interenfriamiento o recalentamiento")
						print("No es posible calcular el proceso ni definir los estados.")
			else:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas pero no son iguales. Es un comportamiento esperado.")
				if estado_in.P is not None and estado_out.P is not None:
					if (estado_in.P - estado_out.P)<1e-6:
						print(f"Las presiones de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos y son iguales. Correcto para un proceso de interenfriamiento o recalentamiento")
					else:
						print(f"Las presiones de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos y NO SON IGUALES. NO ES congruente con el proceso de interenfriamiento o recalentamiento")
				elif estado_in.P is not None:
					estado_out.P = estado_in.P
					self.calcular_estado(estado_in)
					self.calcular_estado(estado_out)
				elif estado_out.P is not None:
					estado_in.P = estado_out.P
					self.calcular_estado(estado_in)
					self.calcular_estado(estado_out)
		
		# Solo el estado_in tiene temperatura definido
		elif estado_in.T is not None:
			estado_out.T = estado_in.T + delta_T
			if estado_in.P is not None and estado_out.P is not None:
					if (estado_in.P - estado_out.P)<1e-6:
						self.calcular_estado(estado_in)
						self.calcular_estado(estado_out)
			elif estado_in.P is not None:
					estado_out.P = estado_in.P
					self.calcular_estado(estado_in)
					self.calcular_estado(estado_out)
			elif estado_out.P is not None:
					estado_in.P = estado_out.P
					self.calcular_estado(estado_in)
					self.calcular_estado(estado_out)
		
		# Solo el estado_out tiene temperatura definido
		elif estado_out.T is not None:
			estado_in.T = estado_out.T - delta_T
			if estado_in.P is not None and estado_out.P is not None:
					if (estado_in.P - estado_out.P)<1e-6:
						self.calcular_estado(estado_in)
						self.calcular_estado(estado_out)
			elif estado_in.P is not None:
					estado_out.P = estado_in.P
					self.calcular_estado(estado_in)
					self.calcular_estado(estado_out)
			elif estado_out.P is not None:
					estado_in.P = estado_out.P
					self.calcular_estado(estado_in)
					self.calcular_estado(estado_out)
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene la temperatura y la presion definida. Se requiere al menos una de cada una.")
"""


	def calcular_estado(self, estado, **kwargs):
		"""
		Método abstracto para calcular las propiedades de un estado.

		Args:
			estado (Estado): Objeto Estado a actualizar.
			**kwargs: Propiedades conocidas del estado (por ejemplo, P, T, v...).

		Raises:
			NotImplementedError: Si no se implementa en una subclase.
		"""
		raise NotImplementedError("Este método debe ser implementado en una subclase.")
	
	

class ModeloGasIdeal(ModeloTermodinamico):
	r"""
	Modelo de gas ideal con capacidades caloríficas constantes. Configurado por defecto para el aire.

	La ecuación del gas ideal usada es: $P\upsilon = R_{gas}T$ con $R_{gas} = \frac{R}{M_{gas}}$.

	$R$: Constante universal de gases.

	$M_{gas}$: Masa molar del gas.

	Args:
		R_gas (float): Constante del gas usado [J/kg·K].
		cp (float): Capacidad calorífica específica a presión constante [J/kg·K].
		cv (float): Capacidad calorífica específica a volumen constante [J/kg·K].
		T0 (float): Temperatura de referencia [K].
		P0 (float): Presión de referencia [Pa].

	Métodos:
		calcular_estado(estado, **kwargs): Calcula propiedades del estado con base en combinaciones de propiedades conocidas.
	"""

	def __init__(self, R_gas=287, cp=1005, cv = 0.718, T0=298.15, P0=101325): 
		self.R_gas = float(R_gas)
		self.cp = float(cp)
		self.cv = float(cv) if cv is not None else self.cp - self.R_gas
		self.T0 = float(T0)
		self.P0 = float(P0)
		self.v0 = self.R_gas*self.T0/self.P0  # volumen específico de referencia



	def resolver_isocorico(self, estado_in, estado_out):
		super().resolver_isocorico(estado_in, estado_out)
		# Gas ideal
		self.calcular_estado(estado_in)
		self.calcular_estado(estado_out)
		def isocorico_ModeloGasIdeal(P):
			"""
			Retorna la temperatura T para un gas ideal en un proceso isocórico, dado P.
			"""
			P = np.asarray(P)  # Asegura que P se pueda vectorizar
			return estado_in.v*P/self.R_gas
		return isocorico_ModeloGasIdeal

	def resolver_isotermico(self, estado_in, estado_out, **kwargs):
		super().resolver_isotermico(estado_in, estado_out)
		# Gas ideal
		self.calcular_estado(estado_in)
		self.calcular_estado(estado_out)
		def isotermico_ModeloGasIdeal(v):
			"""
			Retorna la presión P para un gas ideal en un proceso isotermico, dado v.
			"""
			v = np.asarray(v)
			return (self.R_gas*estado_in.T)/v
		return isotermico_ModeloGasIdeal
	
	def resolver_isobarico(self, estado_in, estado_out):
		super().resolver_isobarico(estado_in, estado_out)
		# Gas ideal
		self.calcular_estado(estado_in)
		self.calcular_estado(estado_out)
		def isobarico_ModeloGasIdeal(v):
			"""
			Retorna la temperatura T para un gas ideal en un proceso isobarico, dado v.
			"""
			v = np.asarray(v)
			return (estado_in.P/self.R_gas)*v
		return isobarico_ModeloGasIdeal

	
	def resolver_isoentalpico(self, estado_in, estado_out):
		super().resolver_isoentalpico(estado_in, estado_out)
		# Gas ideal
		self.calcular_estado(estado_in)
		self.calcular_estado(estado_out)
		# En gases ideales, los procesos isoentalpicos siguen isotermas

		# Ambos están definidos
		if estado_in.T is not None and estado_out.T is not None:
			if estado_in.T == estado_out.T:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas y son iguales.")
			else:
				print(f"Las temperaturas de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidas pero no son iguales. Se recomienda revisar.")
		
		# Solo el estado_in tiene volumen definido
		elif estado_in.T is not None:
			estado_out.T = estado_in.T
		
		# Solo el estado_out tiene volumen definido
		elif estado_out.T is not None:
			estado_in.T = estado_out.T
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} tiene la temperatura definida. Se requiere al menos una.")

		def isoentalpico_ModeloGasIdeal(v):
			"""
			Retorna la presión P para un gas ideal en un proceso isoentalpico -> isotermico, dado v.
			"""
			v = np.asarray(v)
			return (self.R_gas*estado_in.T)/v
		return isoentalpico_ModeloGasIdeal

	def resolver_isoentropico(self, estado_in, estado_out):
		super().resolver_isoentropico(estado_in, estado_out)
		# Gas ideal
		self.calcular_estado(estado_in)
		self.calcular_estado(estado_out)
		def isoentropico_ModeloGasIdeal(v):
			"""
			Retorna la presión P para un gas ideal en un proceso isoentropico, dado v.
			"""
			# Ambos están definidos
			v = np.asarray(v)
			if estado_in.v is not None:
				if estado_in.P is not None:
					return estado_in.P*(estado_in.v/v)**(self.cp/self.cv)
				else:
					print("ERROR: No estan definida la presion en el estado de entrada")
					return None
			elif estado_out.v is not None:
				if estado_out.P is not None:
					return  estado_out.P*(estado_out.v/v)**(self.cp/self.cv)
				else:
					print("ERROR: No estan definida la presion en el estado de salida")
					return None
			else:
				print("ERROR: No estan definidos los volumenes")
				return None
		return isoentropico_ModeloGasIdeal
	

	def resolver_in_or_out_calor(self, estado_in, estado_out, calor):
		super().resolver_in_or_out_calor(estado_in, estado_out, calor)
		# Gas ideal
		# La entropia
		if estado_in.s is not None and estado_out.s is not None:
			if estado_in.s == estado_out.s:
				print(f"Las entropias de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos y son iguales. Esto es un error, agragar o sacar calor cambia la entropia.")
			else:
				if (estado_in.s -(estado_out.s + calor/estado_out.T)< 1e-6):
					print(f"Las entropias de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos pero no son iguales. Son congruentes con el cambio esperado")
				else:
					print(f"Las entropias de los estados {estado_in.nombre} y {estado_out.nombre} fueron definidos pero no son iguales. NO SON congruentes con el cambio esperado " + r"$\Delta$ s =" + f"{estado_in.s - estado_out.s}" + r"Q/T =" +f"{calor/estado_out.T}")
		
		# Solo el estado_in tiene volumen definido
		elif estado_in.s is not None:
			estado_out.s =  estado_in.s + calor/estado_out.T
			self.calcular_estado(estado_in)
			self.calcular_estado(estado_out)
		
		# Solo el estado_out tiene volumen definido
		elif estado_out.s is not None:
			estado_in.s = estado_out.s - calor/estado_out.T
			self.calcular_estado(estado_in)
			self.calcular_estado(estado_out)
		
		# Ninguno tiene volumen definido
		else:
			print(f"Ninguno de los estados {estado_in.nombre} ni {estado_out.nombre} puede ser definido.")

		def in_or_out_calor_ModeloGasIdeal(v):
			"""
			Retorna la presión P para un gas ideal en un proceso de adicion o rechazo de calor -> isotermico, dado v.
			"""
			v = np.asarray(v)
			return (self.R_gas*estado_in.T)/v
		return in_or_out_calor_ModeloGasIdeal
	
	""" def resolver_interenfriamiento_recalentamiento(self, estado_in, estado_out, delta_T):
		super().resolver_interenfriamiento_recalentamiento(estado_in, estado_out, delta_T)
		# Gas ideal

		def interenfriamiento_recalentamiento_ModeloGasIdeal(v):
			'''
			Retorna la presión T para un gas ideal en un proceso de adicion o rechazo de calor, dado v.
			'''
			v = np.asarray(v)
			return (estado_in.P/self.R_gas)*v
		return interenfriamiento_recalentamiento_ModeloGasIdeal """

	def resolver_politropico(self, estado_in, estado_out, n, **kwargs):
		super().resolver_politropico(estado_in, estado_out)
		# Gas ideal

	def calcular_estado(self, estado):
		"""
		Calcula las propiedades del estado en función de combinaciones de propiedades conocidas.

		Combinaciones aceptables: 
		- (P, T)
		- (P, v)
		- (T, v)
		- (P, h)
		- (s,v)
		- (s,P)
		- (T, s)

		Args:
			estado (Estado): Instancia del estado a calcular.
			**kwargs: Combinaciones posibles de propiedades como 'P', 'T', 'v', 'h', 's'. 
		
		Raises:
			ValueError: Si la combinación de propiedades no es soportada.
		"""
		
		# A continuacion se presentan los casos que va a revisar el programa si se tiene los datos y calcula los datos faltantes si es posible
		
		# Caso 1: Conozco Presión (P) y Temperatura (T)
		if (estado.P is not None) and (estado.T is not None):
			estado.v = self.R_gas * estado.T / estado.P
			estado.u = self.cv*estado.T
			estado.h = self.cp * estado.T
			estado.s = self.cp * np.log(estado.T / self.T0) - self.R_gas * np.log(estado.P / self.P0)

		# Caso 2: Conozco Presión (P) y Volumen (v)
		elif (estado.P is not None) and (estado.v is not None):
			estado.T = estado.P * estado.v / self.R_gas
			estado.u = self.cv*estado.T
			estado.h = self.cp * estado.T
			estado.s = self.cp * np.log(estado.T / self.T0) - self.R_gas * np.log(estado.P / self.P0)

		# Caso 3: Conozco Temperatura (T) y Volumen (v)
		elif (estado.T is not None) and (estado.v is not None):
			estado.P = self.R_gas * estado.T / estado.v
			estado.u = self.cv*estado.T
			estado.h = self.cp * estado.T
			estado.s = self.cp * np.log(estado.T / self.T0) - self.R_gas * np.log(estado.P / self.P0)

		# Caso 4: Conozco Presión (P) y Entalpía (h)
		elif (estado.P is not None) and (estado.h is not None):
			estado.T = estado.h / self.cp
			estado.u = self.cv*estado.T
			estado.v = self.R_gas * estado.T / estado.P
			estado.s = self.cp * np.log(estado.T / self.T0) - self.R_gas * np.log(estado.P / self.P0)
		
		# Caso 5: Conozco Entropía (s) y Volumen (v)
		elif (estado.s is not None) and (estado.v is not None):
			estado.T = self.T0*np.exp((1/self.cv)*(estado.s-self.R_gas*np.log(estado.v/self.v0)))
			estado.P = self.R_gas * estado.T / estado.v
			estado.u = self.cv*estado.T
			estado.h = self.cp * estado.T

		# Caso 6: Conozco Entropía (s) y Presion (P)
		elif (estado.s is not None) and (estado.P is not None):
			estado.T = self.T0*np.exp((1/self.cp)*(estado.s+self.R_gas*np.log(estado.P/self.P0)))
			estado.v = self.R_gas * estado.T / estado.P
			estado.u = self.cv*estado.T
			estado.h = self.cp * estado.T

		# Caso 7: Conozco Entropía (s) y Temperatura (T)
		elif (estado.s is not None) and (estado.T is not None):
			estado.P = self.P0*np.exp((1/self.R_gas)*(self.cp*np.log(estado.T/self.T0)-estado.s))
			estado.v = self.R_gas * estado.T / estado.P
			estado.u = self.cv*estado.T
			estado.h = self.cp * estado.T

		else:
			print(f"Combinación de propiedades no soportada o insuficiente.")
		
from scipy.optimize import fsolve

######################################
######################################
######################################
#           Cocinando
######################################
######################################
######################################

class ModeloVanDerWaals(ModeloTermodinamico):
	"""
	Modelo termodinámico basado en la ecuación de Van der Waals.

	Parámetros
	----------
	a : float
		Constante de atracción (Pa·m⁶/mol²).
	b : float
		Volumen excluido por mol (m³/mol).
	R_gas : float, opcional
		Constante del gas (por mol), por defecto 8.314 J/mol·K.
	T0 : float, opcional
		Temperatura de referencia (K).
	P0 : float, opcional
		Presión de referencia (Pa).
	"""

	def __init__(self, a, b, R_gas=8.314, T0=298.15, P0=101325):
		self.a = a
		self.b = b
		self.R_gas = R_gas
		self.T0 = T0
		self.P0 = P0
		self.v0 = self.R_gas * self.T0 / self.P0  # volumen molar de referencia (ideal)

	def calcular_estado(self, estado, **kwargs):
		"""
		Calcula propiedades termodinámicas a partir de combinaciones válidas.

		Soporta combinaciones como: (P, T), (T, v), (P, v), (s, v), (s, P), (T, s), etc.
		"""

		keys = kwargs.keys()

		if 'P' in keys and 'T' in keys:
			estado.P = kwargs['P']
			estado.T = kwargs['T']
			estado.v = self._resolver_volumen(estado.T, estado.P)
			self._calcular_propiedades(estado)

		elif 'T' in keys and 'v' in keys:
			estado.T = kwargs['T']
			estado.v = kwargs['v']
			estado.P = self._presion(estado.T, estado.v)
			self._calcular_propiedades(estado)

		elif 'P' in keys and 'v' in keys:
			estado.P = kwargs['P']
			estado.v = kwargs['v']
			estado.T = self._temperatura(estado.P, estado.v)
			self._calcular_propiedades(estado)

		elif 'P' in keys and 'h' in keys:
			estado.P = kwargs['P']
			estado.h = kwargs['h']
			raise NotImplementedError("Cálculo desde (P, h) no implementado para Van der Waals.")

		elif 's' in keys and 'v' in keys:
			estado.s = kwargs['s']
			estado.v = kwargs['v']
			estado.T = self._resolver_temperatura_desde_sv(estado.s, estado.v)
			estado.P = self._presion(estado.T, estado.v)
			self._calcular_propiedades(estado)

		elif 's' in keys and 'P' in keys:
			raise NotImplementedError("Cálculo desde (s, P) no implementado para Van der Waals.")

		elif 's' in keys and 'T' in keys:
			raise NotImplementedError("Cálculo desde (s, T) no implementado para Van der Waals.")

		else:
			raise ValueError("Combinación de propiedades no soportada o insuficiente.")

	def _presion(self, T, v):
		"""Devuelve la presión (Pa) usando la ecuación de Van der Waals."""
		return (self.R_gas * T) / (v - self.b) - self.a / v**2

	def _temperatura(self, P, v):
		"""Devuelve la temperatura (K) a partir de presión y volumen."""
		return ((P + self.a / v**2) * (v - self.b)) / self.R_gas

	def _resolver_volumen(self, T, P):
		"""Resuelve numéricamente el volumen molar usando fsolve."""
		def f(v):
			return P - self._presion(T, v)
		v_guess = self.R_gas * T / P  # estimación inicial (gas ideal)
		v_solution, = fsolve(f, v_guess)
		return v_solution

	def _resolver_temperatura_desde_sv(self, s, v):
		"""Calcula T desde entropía y volumen."""
		T_guess = self.T0
		def f(T):
			s_calc = self.R_gas * np.log((T / self.T0) * ((v - self.b) / self.v0))
			return s_calc - s
		T_solution, = fsolve(f, T_guess)
		return T_solution

	def _calcular_propiedades(self, estado):
		"""
		Calcula u, h, s a partir de P, T y v. Se asume gas monoatómico (Cv = 3/2 R).
		"""
		Cv = 1.5 * self.R_gas
		Cp = Cv + self.R_gas

		estado.u = Cv * estado.T - self.a / estado.v
		estado.h = estado.u + estado.P * estado.v
		estado.s = self.R_gas * np.log((estado.T / self.T0) * ((estado.v - self.b) / self.v0))