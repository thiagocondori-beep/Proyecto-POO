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


class Combo(Producto):
    def __init__(self, nombre, productos=None, descuento=0.10):
        super().__init__(nombre, 0.0)
        self.descuento = descuento
        self._productos = []
        if productos:
            for prod in productos:
                self.agregar_producto(prod)

    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, valor):
        if valor < 0 or valor >= 1:
            raise ValueError("El descuento debe estar entre 0 y 1.")
        self._descuento = float(valor)

    @property
    def productos(self):
        return list(self._productos)

    def _contiene_a(self, objetivo):
        if self is objetivo:
            return True
        for p in self._productos:
            if isinstance(p, Combo) and p._contiene_a(objetivo):
                return True
        return False

    def agregar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar productos al combo.")
        if isinstance(producto, Combo) and producto._contiene_a(self):
            raise ValueError("Un combo no puede contenerse a sí mismo.")
        self._productos.append(producto)

    def _validar_minimo_productos(self):
        if len(self._productos) < 2:
            raise ValueError("Un combo debe tener al menos 2 productos.")

    def calcular_precio(self):
        self._validar_minimo_productos()
        suma = 0
        for p in self._productos:
            suma += p.calcular_precio()
        return round(suma * (1 - self.descuento), 2)

    def esta_disponible(self, dia):
        self._validar_minimo_productos()
        for p in self._productos:
            if not p.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        self._validar_minimo_productos()
        total = 0
        for p in self._productos:
            total += p.contar_platos()
        return total