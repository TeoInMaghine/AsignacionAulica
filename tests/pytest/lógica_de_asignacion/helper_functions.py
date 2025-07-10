from ortools.sat.python import cp_model

def predicado_es_not_equals_entre_variable_y_constante(predicado, constante):
    '''
    Devuelve `True` si `predicado` es una expresión de la forma `variable != constante`,
    donde `variable` es una variable de un `CpModel`.
    '''
    return isinstance(predicado, cp_model.BoundedLinearExpression) \
        and len(predicado.vars) == 1 \
        and predicado.coeffs == [1] \
        and predicado.offset == 0 \
        and predicado.bounds.complement().flattened_intervals() == [constante, constante]

def predicado_es_not_equals_entre_dos_variables(predicado):
    '''
    Devuelve `True` si `predicado` es una expresión de la forma `variable1 != variable2`,
    donde `variable1` y `variable2` son variables de un `CpModel`.
    '''
    return isinstance(predicado, cp_model.BoundedLinearExpression) \
        and len(predicado.vars) == 2 \
        and predicado.coeffs == [1, -1] \
        and predicado.offset == 0 \
        and predicado.bounds.complement().flattened_intervals() == [0, 0]

def predicado_es_nand_entre_dos_variables_bool(predicado):
    '''
    Devuelve `True` si `predicado` es una expresión de la forma
    `variable1 + variable2 <= 1`, donde `variable1` y `variable2` son variables
    booleanas de un `CpModel`.
    '''
    return isinstance(predicado, cp_model.BoundedLinearExpression) \
        and len(predicado.vars) == 2 \
        and predicado.coeffs == [1, 1] \
        and predicado.offset == 0 \
        and predicado.bounds.max() == 1
