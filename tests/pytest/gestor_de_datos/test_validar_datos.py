from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

def test_todo_ok_con_gestor_vacío(gestor: GestorDeDatos):
    assert gestor.validar_datos() is None

def test_todo_ok_con_un_par_de_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    for i in range(8):
        gestor.agregar_aula(0)
    aulas = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    gestor.agregar_aula_doble(0)
    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_grande'], aulas[5])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_1'], aulas[3])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_2'], aulas[6])

    assert gestor.validar_datos() is None

def test_fata_elegir_el_aula_grande(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'Mitre')
    for i in range(3):
        gestor.agregar_aula(0)
    aulas = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    gestor.agregar_aula_doble(0)
    #gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'aula doble' in mensaje
    assert 'seleccionar' in mensaje

def test_fata_elegir_el_aula_chica1(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'Mitre')
    for i in range(3):
        gestor.agregar_aula(0)
    aulas = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    #gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'aula doble' in mensaje
    assert 'seleccionar' in mensaje

def test_fata_elegir_el_aula_chica2(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'Mitre')
    for i in range(3):
        gestor.agregar_aula(0)
    aulas = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    #gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])

    mensaje = gestor.validar_datos().lower()
    assert 'mitre' in mensaje
    assert 'aula doble' in mensaje
    assert 'seleccionar' in mensaje
