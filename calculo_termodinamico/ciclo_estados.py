# Definición de la clase Estado
class Estado:
    def __init__(self, modelo, nombre=""):
        self.nombre = nombre
        self.modelo = modelo
        
        # Propiedades termodinámicas
        self.P = None
        self.T = None
        self.v = None
        self.u = None
        self.h = None
        self.s = None

    def actualizar(self, **kwargs):
        """
        Actualiza el estado utilizando el modelo termodinámico.
        """
        self.modelo.calcular_estado(self, **kwargs)

    def resumen(self):
        """
        Devuelve un resumen del estado actual.
        """
        return (f"{self.nombre}: P={self.P:.2f} Pa, T={self.T:.2f} K, "
                f"v={self.v:.5f} m³/kg,u={self.u:.2f} J/kg, h={self.h:.2f} J/kg, s={self.s:.2f} J/kg·K")
    
# Definición de la clase CicloTermodinamico
class CicloTermodinamico:
    def __init__(self, modelo):
        self.modelo = modelo
        self.estados = []

    def agregar_estado(self, nombre, **kwargs):
        """
        Agrega un estado al ciclo y lo calcula.
        """
        estado = Estado(self.modelo, nombre)
        estado.actualizar(**kwargs)
        self.estados.append(estado)

    def mostrar_ciclo(self):
        """
        Muestra un resumen de todos los estados del ciclo.
        """
        for estado in self.estados:
            print(estado.resumen())