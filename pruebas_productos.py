from modelo.productos import Producto, Plato, Bebida, Combo


def probar_productos():
    try:
        Producto("Prueba", 10)
        assert False, "No debería permitir instanciar Producto"
    except TypeError:
        pass

    silpancho = Plato("Silpancho", 35.0)
    mocochinchi_vaso = Bebida("Mocochinchi", 6.0, es_jarra=False)
    mocochinchi_jarra = Bebida("Mocochinchi", 6.0, es_jarra=True)

    assert silpancho.calcular_precio() == 35.0
    assert silpancho.contar_platos() == 1
    assert mocochinchi_vaso.calcular_precio() == 6.0
    assert mocochinchi_vaso.contar_platos() == 0
    assert mocochinchi_jarra.calcular_precio() == 18.0

    chicharron = Plato("Chicharrón", 45.0, dias=["domingo"])
    assert chicharron.esta_disponible("domingo") is True
    assert chicharron.esta_disponible("lunes") is False

    combo_valluno = Combo("Combo Valluno", [silpancho, mocochinchi_vaso])
    assert combo_valluno.calcular_precio() == 36.90
    assert combo_valluno.contar_platos() == 1
    assert combo_valluno.esta_disponible("martes") is True

    combo_domingo = Combo("Combo Especial", [combo_valluno, chicharron])
    assert combo_domingo.calcular_precio() == 73.71
    assert combo_domingo.contar_platos() == 2
    assert combo_domingo.esta_disponible("domingo") is True
    assert combo_domingo.esta_disponible("miercoles") is False

    try:
        combo_valluno.agregar_producto(combo_valluno)
        assert False, "Un combo no debe contenerse a sí mismo"
    except ValueError:
        pass

    try:
        Plato("Error", -10)
        assert False, "No debe permitir precios negativos o cero"
    except ValueError:
        pass

    print("Todas las pruebas de la Fase 2 pasaron correctamente.")


if __name__ == "__main__":
    probar_productos()