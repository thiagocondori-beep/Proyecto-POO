from abc import ABC, abstractmethod
from modelo.productos import Producto
from modelo.clientes import Cliente
from modelo.pagos import MetodoPago


class ItemPedido:
    def __init__(self, producto, cantidad=1):
        self.producto = producto
        self.cantidad = cantidad

    @property
    def producto(self):
        return self._producto

    @producto.setter
    def producto(self, valor):
        if not isinstance(valor, Producto):
            raise TypeError("El ítem debe contener una instancia de Producto.")
        self._producto = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")
        self._cantidad = valor

    def calcular_subtotal(self):
        return round(self._producto.calcular_precio() * self._cantidad, 2)


class Pedido(ABC):
    ESTADOS_VALIDOS = (
        "pendiente",
        "en_preparacion",
        "listo",
        "entregado",
        "cancelado"
    )

    TRANSICIONES_VALIDAS = {
        "pendiente": ("en_preparacion", "cancelado"),
        "en_preparacion": ("listo", "cancelado"),
        "listo": ("entregado",),
        "entregado": (),
        "cancelado": ()
    }

    def __init__(self, cliente, dia="lunes"):
        self.cliente = cliente
        self.dia = dia
        self._items = []
        self._estado = "pendiente"
        self._pago = None

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        if not isinstance(valor, Cliente):
            raise TypeError("El pedido debe estar asociado a un Cliente válido.")
        self._cliente = valor

    @property
    def dia(self):
        return self._dia

    @dia.setter
    def dia(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("Debe especificar un día válido para el pedido.")
        self._dia = str(valor).strip().lower()

    @property
    def estado(self):
        return self._estado

    @property
    def pago(self):
        return self._pago

    @property
    def items(self):
        return list(self._items)

    def _verificar_modificable(self):
        if self._estado != "pendiente":
            raise ValueError("No se puede modificar un pedido que ya no está pendiente.")

    def agregar_producto(self, producto, cantidad=1):
        self._verificar_modificable()
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar productos al pedido.")
        if not producto.esta_disponible(self._dia):
            raise ValueError(f"El producto '{producto.nombre}' no está disponible los días {self._dia}.")

        for item in self._items:
            if item.producto is producto:
                item.cantidad = item.cantidad + cantidad
                return

        nuevo_item = ItemPedido(producto, cantidad)
        self._items.append(nuevo_item)

    def eliminar_producto(self, nombre_producto):
        self._verificar_modificable()
        nombre_limpio = nombre_producto.strip().lower()
        for i in range(len(self._items)):
            if self._items[i].producto.nombre.lower() == nombre_limpio:
                self._items.pop(i)
                return
        raise ValueError("El producto no se encuentra en el pedido.")

    def calcular_subtotal(self):
        total = 0.0
        for item in self._items:
            total += item.calcular_subtotal()
        return round(total, 2)

    def contar_total_platos(self):
        total_platos = 0
        for item in self._items:
            total_platos += item.producto.contar_platos() * item.cantidad
        return total_platos

    @abstractmethod
    def calcular_cargo_extra(self):
        pass

    def calcular_total(self):
        if len(self._items) == 0:
            raise ValueError("El pedido no tiene productos.")
        return round(self.calcular_subtotal() + self.calcular_cargo_extra(), 2)

    def cambiar_estado(self, nuevo_estado):
        estado_limpio = str(nuevo_estado).strip().lower()
        if estado_limpio not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado de pedido no reconocido.")
        if estado_limpio == "en_preparacion" and len(self._items) == 0:
            raise ValueError("No se puede preparar un pedido vacío.")
        if estado_limpio not in self.TRANSICIONES_VALIDAS[self._estado]:
            raise ValueError(f"No se puede pasar de '{self._estado}' a '{estado_limpio}'.")
        self._estado = estado_limpio

    def registrar_pago(self, metodo_pago):
        if self._estado == "cancelado":
            raise ValueError("No se puede pagar un pedido cancelado.")
        if self._pago is not None:
            raise ValueError("Este pedido ya fue pagado.")
        if not isinstance(metodo_pago, MetodoPago):
            raise TypeError("Debe proporcionar un método de pago válido.")
        total_pedido = self.calcular_total()
        if round(metodo_pago.monto, 2) != total_pedido:
            raise ValueError(f"El monto del pago (Bs. {metodo_pago.monto:.2f}) no coincide con el total (Bs. {total_pedido:.2f}).")
        if metodo_pago.procesar_pago():
            self._pago = metodo_pago


class PedidoLocal(Pedido):
    def __init__(self, cliente, numero_mesa, dia="lunes"):
        super().__init__(cliente, dia)
        self.numero_mesa = numero_mesa

    @property
    def numero_mesa(self):
        return self._numero_mesa

    @numero_mesa.setter
    def numero_mesa(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El número de mesa debe ser un entero positivo.")
        self._numero_mesa = valor

    def calcular_cargo_extra(self):
        return 0.0


class PedidoLlevar(Pedido):
    COSTO_EMPAQUE = 2.0

    def __init__(self, cliente, dia="lunes"):
        super().__init__(cliente, dia)

    def calcular_cargo_extra(self):
        return self.COSTO_EMPAQUE


class PedidoDelivery(Pedido):
    COSTO_ENVIO = 10.0

    def __init__(self, cliente, dia="lunes"):
        if not isinstance(cliente, Cliente) or not cliente.tiene_direccion():
            raise ValueError("Para un pedido Delivery el cliente debe tener una dirección registrada.")
        super().__init__(cliente, dia)

    def calcular_cargo_extra(self):
        return self.COSTO_ENVIO