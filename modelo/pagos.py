from abc import ABC, abstractmethod


class MetodoPago(ABC):
    def __init__(self, monto):
        self.monto = monto

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, valor):
        if valor <= 0:
            raise ValueError("El monto a pagar debe ser mayor que cero.")
        self._monto = round(float(valor), 2)

    @abstractmethod
    def procesar_pago(self):
        pass

    @abstractmethod
    def obtener_comprobante(self):
        pass


class Efectivo(MetodoPago):
    def __init__(self, monto, monto_recibido):
        super().__init__(monto)
        self.monto_recibido = monto_recibido

    @property
    def monto_recibido(self):
        return self._monto_recibido

    @monto_recibido.setter
    def monto_recibido(self, valor):
        if valor < self.monto:
            raise ValueError("El monto recibido no puede ser menor al total a pagar.")
        self._monto_recibido = round(float(valor), 2)

    def calcular_cambio(self):
        return round(self._monto_recibido - self.monto, 2)

    def procesar_pago(self):
        return True

    def obtener_comprobante(self):
        return f"Pago en Efectivo: Bs. {self.monto:.2f} | Recibido: Bs. {self._monto_recibido:.2f} | Cambio: Bs. {self.calcular_cambio():.2f}"


class PagoQR(MetodoPago):
    def __init__(self, monto, codigo_transaccion):
        super().__init__(monto)
        self.codigo_transaccion = codigo_transaccion

    @property
    def codigo_transaccion(self):
        return self._codigo_transaccion

    @codigo_transaccion.setter
    def codigo_transaccion(self, valor):
        codigo = str(valor).strip()
        if len(codigo) < 6:
            raise ValueError("El código de transacción QR debe tener al menos 6 caracteres.")
        self._codigo_transaccion = codigo

    def procesar_pago(self):
        return True

    def obtener_comprobante(self):
        return f"Pago QR: Bs. {self.monto:.2f} | Transacción: {self._codigo_transaccion}"


class Tarjeta(MetodoPago):
    def __init__(self, monto, ultimos_digitos, tipo="debito"):
        super().__init__(monto)
        self.ultimos_digitos = ultimos_digitos
        self.tipo = tipo

    @property
    def ultimos_digitos(self):
        return self._ultimos_digitos

    @ultimos_digitos.setter
    def ultimos_digitos(self, valor):
        digitos = str(valor).strip()
        if len(digitos) != 4 or not digitos.isdigit():
            raise ValueError("Debe ingresar exactamente los 4 últimos dígitos de la tarjeta.")
        self._ultimos_digitos = digitos

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        tipo_limpio = str(valor).strip().lower()
        if tipo_limpio not in ("debito", "credito"):
            raise ValueError("El tipo de tarjeta debe ser 'debito' o 'credito'.")
        self._tipo = tipo_limpio

    def procesar_pago(self):
        return True

    def obtener_comprobante(self):
        return f"Pago con Tarjeta ({self._tipo}) terminada en {self._ultimos_digitos}: Bs. {self.monto:.2f}"