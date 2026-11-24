from modelo.productos import Plato, Bebida, Combo
from modelo.clientes import Cliente
from modelo.pagos import Efectivo, PagoQR, Tarjeta
from modelo.pedidos import PedidoLocal, PedidoLlevar, PedidoDelivery


def crear_catalogo():
    silpancho = Plato("Silpancho", 35.0)
    pique = Plato("Pique Macho", 55.0)
    chicharron = Plato("Chicharrón", 45.0, dias=["domingo"])
    mocochinchi = Bebida("Mocochinchi", 6.0, es_jarra=False)
    jarra_mocochinchi = Bebida("Mocochinchi", 6.0, es_jarra=True)
    combo_valluno = Combo("Combo Valluno", [silpancho, mocochinchi])
    return [silpancho, pique, chicharron, mocochinchi, jarra_mocochinchi, combo_valluno]


def mostrar_catalogo(catalogo):
    print("\n--- MENÚ SABOR VALLUNO ---")
    for i in range(len(catalogo)):
        prod = catalogo[i]
        print(f"{i + 1}. {prod.nombre} - Bs. {prod.calcular_precio():.2f}")


def iniciar_sistema():
    catalogo = crear_catalogo()
    pedidos = []

    while True:
        print("\n=== SISTEMA DE GESTIÓN DE PEDIDOS ===")
        print("1. Ver menú de productos")
        print("2. Registrar nuevo pedido")
        print("3. Ver pedidos registrados")
        print("4. Cambiar estado de un pedido")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_catalogo(catalogo)

        elif opcion == "2":
            try:
                nombre = input("Nombre del cliente: ")
                telefono = input("Teléfono (8 dígitos, empieza con 6 o 7): ")
                direccion = input("Dirección (opcional si no es delivery): ")
                cliente = Cliente(nombre, telefono, direccion)

                dia = input("Día del pedido (ej. lunes, domingo): ")
                print("Tipo de pedido: 1. Local | 2. Para llevar | 3. Delivery")
                tipo = input("Elija tipo: ").strip()

                if tipo == "1":
                    mesa = int(input("Número de mesa: "))
                    pedido = PedidoLocal(cliente, mesa, dia)
                elif tipo == "2":
                    pedido = PedidoLlevar(cliente, dia)
                elif tipo == "3":
                    pedido = PedidoDelivery(cliente, dia)
                else:
                    print("Tipo de pedido inválido.")
                    continue

                while True:
                    mostrar_catalogo(catalogo)
                    eleccion = input("Número de producto (o 0 para terminar): ").strip()
                    if eleccion == "0":
                        break
                    indice = int(eleccion) - 1
                    if indice < 0 or indice >= len(catalogo):
                        print("Producto fuera de rango.")
                        continue
                    cantidad = int(input("Cantidad: "))
                    pedido.agregar_producto(catalogo[indice], cantidad)
                    print("Producto agregado.")

                total = pedido.calcular_total()
                print(f"\nSubtotal: Bs. {pedido.calcular_subtotal():.2f}")
                print(f"Cargo extra: Bs. {pedido.calcular_cargo_extra():.2f}")
                print(f"Total a pagar: Bs. {total:.2f}")

                print("Método de pago: 1. Efectivo | 2. QR | 3. Tarjeta")
                metodo = input("Elija método: ").strip()

                if metodo == "1":
                    recibido = float(input("Monto recibido: "))
                    pago = Efectivo(total, recibido)
                elif metodo == "2":
                    codigo = input("Código de transacción QR (mínimo 6 caracteres): ")
                    pago = PagoQR(total, codigo)
                elif metodo == "3":
                    digitos = input("Últimos 4 dígitos de la tarjeta: ")
                    tipo_tarjeta = input("Tipo (debito/credito): ")
                    pago = Tarjeta(total, digitos, tipo_tarjeta)
                else:
                    print("Método inválido. Pedido no registrado.")
                    continue

                pedido.registrar_pago(pago)
                pedidos.append(pedido)
                print("Pedido registrado y pagado con éxito.")
                print(pago.obtener_comprobante())

            except (ValueError, TypeError) as error:
                print(f"Error: {error}")

        elif opcion == "3":
            if len(pedidos) == 0:
                print("\nNo hay pedidos registrados.")
            else:
                print("\n--- PEDIDOS ---")
                for i in range(len(pedidos)):
                    p = pedidos[i]
                    print(f"{i + 1}. Cliente: {p.cliente.nombre} | Estado: {p.estado} | Platos: {p.contar_total_platos()} | Total: Bs. {p.calcular_total():.2f}")

        elif opcion == "4":
            if len(pedidos) == 0:
                print("\nNo hay pedidos para actualizar.")
                continue
            for i in range(len(pedidos)):
                print(f"{i + 1}. {pedidos[i].cliente.nombre} (Estado actual: {pedidos[i].estado})")
            try:
                idx = int(input("Seleccione el número de pedido: ")) - 1
                if idx < 0 or idx >= len(pedidos):
                    print("Pedido inválido.")
                    continue
                nuevo_estado = input("Nuevo estado (en_preparacion, listo, entregado, cancelado): ")
                pedidos[idx].cambiar_estado(nuevo_estado)
                print("Estado actualizado correctamente.")
            except ValueError as error:
                print(f"Error: {error}")

        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    iniciar_sistema()