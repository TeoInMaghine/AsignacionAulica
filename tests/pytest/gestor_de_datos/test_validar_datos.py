from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

def test_todo_ok_con_gestor_vacío(gestor: GestorDeDatos):
    assert gestor.validar_datos() is None

def test_todo_ok_con_un_par_de_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    for i in range(8):
        gestor.agregar_aula(0)
    aulas = gestor.get_edificio(0).aulas

    gestor.agregar_aula_doble(0)
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[1]
    gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[2]
    gestor.get_aula_doble(0, 1).aula_grande = aulas[5]
    gestor.get_aula_doble(0, 1).aula_chica_1 = aulas[3]
    gestor.get_aula_doble(0, 1).aula_chica_2 = aulas[6]

    assert gestor.validar_datos() is None

def test_falta_elegir_el_aula_grande(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'Mitre'
    for i in range(3):
        gestor.agregar_aula(0)
    aulas = gestor.get_edificio(0).aulas

    gestor.agregar_aula_doble(0)
    #gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[1]
    gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[2]

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'aula doble' in mensaje
    assert 'seleccionar' in mensaje

def test_falta_elegir_el_aula_chica1(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'Mitre'
    for i in range(3):
        gestor.agregar_aula(0)
    aulas = gestor.get_edificio(0).aulas

    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    #gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[1]
    gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[2]

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'aula doble' in mensaje
    assert 'seleccionar' in mensaje

def test_falta_elegir_el_aula_chica2(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'Mitre'
    for i in range(3):
        gestor.agregar_aula(0)
    aulas = gestor.get_edificio(0).aulas

    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[1]
    #gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[2]

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'aula doble' in mensaje
    assert 'seleccionar' in mensaje

def test_aula_repetida_en_aula_doble(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'Mitre'
    for i in range(2):
        gestor.agregar_aula(0)
    aulas = gestor.get_edificio(0).aulas

    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[1]
    gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[1] # Repetida

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'repetida' in mensaje

def test_aula_repetida_en_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'Mitre'
    for i in range(5):
        gestor.agregar_aula(0)
    aulas = gestor.get_edificio(0).aulas

    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[1]
    gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[2]
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 1).aula_grande = aulas[3]
    gestor.get_aula_doble(0, 1).aula_chica_1 = aulas[1] # Repetida
    gestor.get_aula_doble(0, 1).aula_chica_2 = aulas[4]

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'repetida' in mensaje
