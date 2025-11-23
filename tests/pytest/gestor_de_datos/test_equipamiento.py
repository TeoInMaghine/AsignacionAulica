from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

def test_empieza_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay nada
    assert gestor.get_equipamientos_existentes() == []

    # Agregar un aula no agrega equipamiento
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    assert gestor.get_equipamientos_existentes() == []

    # Agregar una clase no agrega equipamiento
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    assert gestor.get_equipamientos_existentes() == []

def test_agregar_equipamiento_a_clase(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_equipamiento_a_clase(0, 0, 0, 'Proyector')

    assert gestor.get_equipamientos_existentes() == ['Proyector']
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['equipamiento_necesario']) == {'Proyector'}

def test_agregar_y_quitar_equipamiento_a_aula(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.agregar_equipamiento_a_aula(0, 0, 'Proyector')
    gestor.agregar_equipamiento_a_aula(0, 0, 'Compus')
    assert gestor.get_aula(0, 0).equipamiento == {'Proyector', 'Compus'}
    assert gestor.get_equipamientos_existentes() == ['Compus', 'Proyector'] # Los ordenó alfabéticamente

    gestor.borrar_equipamiento_de_aula(0, 0, 'Proyector')
    assert gestor.get_aula(0, 0).equipamiento == {'Compus'}
    assert gestor.get_equipamientos_existentes() == ['Compus']

def test_agregar_y_quitar_equipamiento_a_clase(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_equipamiento_a_clase(0, 0, 0, 'Proyector')
    gestor.agregar_equipamiento_a_clase(0, 0, 0, 'muñeco de rcp') # Este se va a cambiar a titlecase al normalizarlo
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['equipamiento_necesario']) == {'Proyector', 'Muñeco De Rcp'}
    assert gestor.get_equipamientos_existentes() == ['Muñeco De Rcp', 'Proyector'] # Los ordenó alfabéticamente

    gestor.borrar_equipamiento_de_clase(0, 0, 0, 'Muñeco De Rcp')
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['equipamiento_necesario']) == {'Proyector'}
    assert gestor.get_equipamientos_existentes() == ['Proyector']

def test_agregar_y_quitar_equipamientos_en_varios_lugares(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_clase(0, 1)

    gestor.agregar_edificio()
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.agregar_aula(1)

    assert gestor.get_equipamientos_existentes() == []

    gestor.agregar_equipamiento_a_aula(1, 0, 'A')
    assert gestor.get_aula(1, 0).equipamiento == {'A'}
    assert gestor.get_equipamientos_existentes() == ['A']

    gestor.agregar_equipamiento_a_clase(0, 0, 0, 'B')
    gestor.agregar_equipamiento_a_clase(0, 0, 0, 'A')
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['equipamiento_necesario']) == {'A', 'B'}
    assert gestor.get_equipamientos_existentes() == ['A', 'B']

    gestor.agregar_equipamiento_a_aula(0, 0, 'C')
    assert gestor.get_aula(0, 0).equipamiento == {'C'}
    assert gestor.get_equipamientos_existentes() == ['A', 'B', 'C']

    gestor.borrar_equipamiento_de_clase(0, 0, 0, 'A')
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['equipamiento_necesario']) == {'B'}
    assert gestor.get_equipamientos_existentes() == ['A', 'B', 'C'] # No se borra de la lista global

    gestor.borrar_equipamiento_de_aula(1, 0, 'A')
    assert gestor.get_aula(1, 0).equipamiento == set()
    assert gestor.get_equipamientos_existentes() == ['B', 'C'] # Ahora si se borra de la lista global
