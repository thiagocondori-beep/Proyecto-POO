from modelo.productos import Plato, Bebida, Combo
from modelo.clientes import Cliente
from modelo.pagos import Efectivo, PagoQR, Tarjeta
from modelo.pedidos import PedidoLocal, PedidoLlevar, PedidoDelivery


def probar_sistema_completo():
    cliente_local = Cliente("Carlos Mamani", "71234567")
    cliente_delivery = Cliente("Ana Quispe", "68901234", "Av. Blanco Galindo km 5")

    try:
        Cliente("Error Tel", "51234567")
        assert False, "No debe aceptar teléfonos que no empiecen con 6 o 7"
    except ValueError:
        pass

    silpancho = Plato("Silpancho", 35.0)
    chicharron = Plato("Chicharrón", 45.0, dias=["domingo"])
    mocochinchi = Bebida("Mocochinchi", 6.0, es_jarra=True)
    combo_familiar = Combo("Combo Familiar", [silpancho, mocochinchi])

    pedido_mesa = PedidoLocal(cliente_local, numero_mesa=4, dia="martes")
    pedido_mesa.agregar_producto(combo_familiar, 1)
    assert pedido_mesa.calcular_subtotal() == 47.70
    assert pedido_mesa.calcular_cargo_extra() == 0.0
    assert pedido_mesa.calcular_total() == 47.70
    assert pedido_mesa.contar_total_platos() == 1

    try:
        pedido_mesa.agregar_producto(chicharron, 1)
        assert False, "No debe permitir Chicharrón un martes"
    except ValueError:
        pass

    pago_efectivo = Efectivo(47.70, 50.0)
    assert pago_efectivo.calcular_cambio() == 2.30
    pedido_mesa.registrar_pago(pago_efectivo)

    pedido_mesa.cambiar_estado("en_preparacion")
    try:
        pedido_mesa.agregar_producto(silpancho, 1)
        assert False, "No se debe modificar un pedido que ya está en preparación"
    except ValueError:
        pass

    pedido_mesa.cambiar_estado("listo")
    pedido_mesa.cambiar_estado("entregado")
    assert pedido_mesa.estado == "entregado"

    try:
        PedidoDelivery(cliente_local, dia="domingo")
        assert False, "No debe permitir delivery sin dirección"
    except ValueError:
        pass

    pedido_domicilio = PedidoDelivery(cliente_delivery, dia="domingo")
    pedido_domicilio.agregar_producto(chicharron, 2)
    assert pedido_domicilio.calcular_subtotal() == 90.0
    assert pedido_domicilio.calcular_cargo_extra() == 10.0
    assert pedido_domicilio.calcular_total() == 100.0
    assert pedido_domicilio.contar_total_platos() == 2

    pago_qr = PagoQR(100.0, "QR987654")
    pedido_domicilio.registrar_pago(pago_qr)
    assert pedido_domicilio.pago is pago_qr

    pedido_llevar = PedidoLlevar(cliente_local, dia="viernes")
    pedido_llevar.agregar_producto(silpancho, 1)
    assert pedido_llevar.calcular_total() == 37.0
    pago_tarjeta = Tarjeta(37.0, "4321", tipo="debito")
    pedido_llevar.registrar_pago(pago_tarjeta)

    print("Todas las pruebas de la Fase 3 pasaron correctamente.")


if __name__ == "__main__":
    probar_sistema_completo()