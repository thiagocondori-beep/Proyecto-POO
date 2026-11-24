from abc import ABC, abstractmethod


class Producto(ABC):
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = round(float(valor), 2)

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass

class Plato(Producto):
    def __init__(self, nombre, precio, dias=None):
        if precio <= 0:
            raise ValueError("El precio del plato debe ser mayor que cero.")
        super().__init__(nombre, precio)
        self.dias = dias

    @property
    def dias(self):
        return list(self._dias)

    @dias.setter
    def dias(self, valor):
        if valor is None:
            self._dias = [
                "lunes", "martes", "miercoles", "jueves",
                "viernes", "sabado", "domingo"
            ]
        else:
            self._dias = [d.strip().lower() for d in valor]

    def calcular_precio(self):
        return self.precio

    def esta_disponible(self, dia):
        dia_limpio = dia.strip().lower().replace("é", "e").replace("á", "a")
        dias_limpios = [d.replace("é", "e").replace("á", "a") for d in self._dias]
        return dia_limpio in dias_limpios

    def contar_platos(self):
        return 1


class Bebida(Producto):
    def __init__(self, nombre, precio, es_jarra=False):
        if precio <= 0:
            raise ValueError("El precio de la bebida debe ser mayor que cero.")
        super().__init__(nombre, precio)
        self.es_jarra = es_jarra

    @property
    def es_jarra(self):
        return self._es_jarra

    @es_jarra.setter
    def es_jarra(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("es_jarra debe ser True o False.")
        self._es_jarra = valor

    def calcular_precio(self):
        if self.es_jarra:
            return round(self.precio * 3, 2)
        return self.precio

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0