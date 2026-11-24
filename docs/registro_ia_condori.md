# Registro de Uso de Inteligencia Artificial — Proyecto POO (Sabor Valluno)

- **Estudiante:** Thiago Condori
- **Repositorio:** https://github.com/thiagocondori-beep/Proyecto-POO
- **Variante asignada:** Variante A (10% de descuento en combos; Chicharrón disponible únicamente los domingos)
- **Herramienta utilizada:** Gemini

---

## Bitácora de Consultas y Verificación

### 1. Implementación de la jerarquía de productos (`modelo/productos.py`)
- **Objetivo:** Implementar la clase abstracta `Producto` y las subclases `Plato`, `Bebida` y `Combo` respetando encapsulamiento con `@property`, validaciones en setters, recursividad en combos (patrón Composite) y reglas de la Variante A.
- **Acción realizada:** Se generó la estructura base de las clases y se adaptó la sintaxis para mantener el código limpio (sin anotaciones de tipo ni comprensiones complejas) con el fin de facilitar su lectura y defensa.
- **Verificación:** Se creó y ejecutó `pruebas_productos.py` comprobando cálculo de precios con descuento del 10 %, restricción de disponibilidad del Chicharrón solo los domingos, conteo recursivo de platos y bloqueo de ciclos en combos.

### 2. Implementación de clientes, pagos y pedidos (`modelo/clientes.py`, `modelo/pagos.py`, `modelo/pedidos.py`)
- **Objetivo:** Desarrollar las clases de dominio para clientes, métodos de pago polimórficos (`Efectivo`, `PagoQR`, `Tarjeta`) y pedidos (`PedidoLocal`, `PedidoLlevar`, `PedidoDelivery`) con control estricto de transiciones de estado.
- **Acción realizada:** Se estructuraron los tres módulos aplicando herencia, clases abstractas (`ABC`), composición (`ItemPedido` dentro de `Pedido`) y validaciones de negocio (teléfono boliviano de 8 dígitos iniciado en 6 o 7, dirección obligatoria en delivery y bloqueo de edición fuera del estado `pendiente`).
- **Verificación:** Se creó y ejecutó `pruebas_pedidos.py` validando la integración completa entre clientes, productos, cálculo de cargos extra, cambio en efectivo y flujo de estados hasta `entregado`.

### 3. Interfaz de consola y resolución de conflictos en Git (`main.py`)
- **Objetivo:** Construir un menú interactivo en terminal para demostrar el sistema y sincronizar el historial de commits en GitHub.
- **Acción realizada:** Se implementó `main.py` conectando todas las clases del paquete `modelo` y se resolvieron conflictos de sincronización de ramas (`rebase`) para mantener el historial ordenado en el repositorio remoto.
- **Verificación:** Se ejecutó `python main.py` comprobando el flujo completo de visualización de catálogo, registro de pedidos, cobro y actualización de estados.