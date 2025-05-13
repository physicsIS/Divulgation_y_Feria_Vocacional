import numpy as np

class ModeloTermodinamico:
    def calcular_estado(self, estado, **kwargs):
        raise NotImplementedError("Este método debe ser implementado en una subclase.")
    

class ModeloGasIdeal(ModeloTermodinamico):
    def __init__(self, R=287, cp=1005, cv = 0.718, T0=0.1, P0=1):

        """
        Modelo de gas ideal para calcular propiedades termodinámicas. Considerando Cp y Cv constantes. Por defecto esta configurado para el aire
        """
        self.R = R # Constante del gas
        self.cp = cp # Capacidad calorifica a presion constante
        self.cv = cv # Capacidad calorifica a volumen constante
        self.T0 = T0 # Temperatura base para hacer los calculos, todos los calculos se deben realizar sobre la misma temperatura
        self.P0 = P0 # Presion base para hacer los calculos, todos los calculos se deben realizar sobre la misma presion

    def calcular_estado(self, estado, **kwargs):
        """
        Calcula las propiedades del estado en función de las variables proporcionadas.
        Permite distintas combinaciones: (P, T), (P, v), (T, v), (P, h), (T, s), etc.
        """
        keys = kwargs.keys()
        
		# A continuacion se presentan los casos que va a revisar el programa si se tiene los datos y calcula los datos faltantes si es posible
        
        # Caso 1: Conozco Presión (P) y Temperatura (T)
        if 'P' in keys and 'T' in keys:
            estado.P = kwargs['P']
            estado.T = kwargs['T']
            estado.v = self.R * estado.T / estado.P
            estado.u = self.cv*(estado.T - self.T0)
            estado.h = self.cp * estado.T
            estado.s = self.cp * np.log(estado.T / self.T0) - self.R * np.log(estado.P / self.P0)

        # Caso 2: Conozco Presión (P) y Volumen (v)
        elif 'P' in keys and 'v' in keys:
            estado.P = kwargs['P']
            estado.v = kwargs['v']
            estado.T = estado.P * estado.v / self.R
            estado.u = self.cv*(estado.T - self.T0)
            estado.h = self.cp * estado.T
            estado.s = self.cp * np.log(estado.T / self.T0) - self.R * np.log(estado.P / self.P0)

        # Caso 3: Conozco Temperatura (T) y Volumen (v)
        elif 'T' in keys and 'v' in keys:
            estado.T = kwargs['T']
            estado.v = kwargs['v']
            estado.P = self.R * estado.T / estado.v
            estado.u = self.cv*(estado.T - self.T0)
            estado.h = self.cp * estado.T
            estado.s = self.cp * np.log(estado.T / self.T0) - self.R * np.log(estado.P / self.P0)

        # Caso 4: Conozco Presión (P) y Entalpía (h)
        elif 'P' in keys and 'h' in keys:
            estado.P = kwargs['P']
            estado.h = kwargs['h']
            estado.T = estado.h / self.cp
            estado.u = self.cv*(estado.T - self.T0)
            estado.v = self.R * estado.T / estado.P
            estado.s = self.cp * np.log(estado.T / self.T0) - self.R * np.log(estado.P / self.P0)

        else:
            raise ValueError("Combinación de propiedades no soportada o insuficiente.")