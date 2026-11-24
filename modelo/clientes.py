class Cliente:
    def __init__(self, nombre, telefono, direccion=""):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        tel = str(valor).strip()
        if len(tel) != 8 or not tel.isdigit() or tel[0] not in ("6", "7"):
            raise ValueError("El teléfono debe tener 8 dígitos y empezar con 6 o 7.")
        self._telefono = tel

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        if valor is None:
            self._direccion = ""
        else:
            self._direccion = str(valor).strip()

    def tiene_direccion(self):
        return len(self._direccion) > 0