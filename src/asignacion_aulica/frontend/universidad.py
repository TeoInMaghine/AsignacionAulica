import pandas as pd
from datetime import time

from asignacion_aulica.frontend.excepciones_universidad import *
from asignacion_aulica.get_asset_path import get_asset_path



class Universidad:
    def __init__(self, 
        edificios=pd.read_excel(get_asset_path('efdificios_default/edificios.xlsx')), 
        aulas = pd.read_excel(get_asset_path('edificios_default/aulas.xlsx'))
    ):        
        self.edificios = edificios
        self.aulas = aulas


    # Sector de edificios:

    def columnas_edificios(self): 
        """
        Metodo que retorna lista de nombres de columnas, del dataframe de Edificios

        Parameters
        -None
        Returns
            La lista de columnas de los edificios
        TYPE
            List[str]
        """
        return self.edificios.columns.tolist()
        
    def mostrar_edificios(self):
        """
        Retorna el dataframe de los edificios instanciados

        Parameters
        -None
        Returns
            La lista de columnas de los edificios
        TYPE
            DataFrame
        """
        return self.edificios

    def nombres_edificios(self):
        """
        Metodo para mostrar los nombres de los edificios instanciados.
        Sirve para el menu dropdown al intentar crear aulas.

        Parameters
        -None
        Returns
            La lista de nombres de los edificios instanciados
        TYPE
            List[str]
        """
        return self.edificios.iloc[:,0].tolist()

    def agregar_edificio(self, nombre_edificio:str):
        """
        Metodo para agregar un edificio a la universidad.

        Parameters
        ----------
        nombre_edificio : str
            El nombre del edificio a agregar. Funciona como clave primaria.
        Returns
            None
        Throws:
            ElementoYaExistenteException , si se trata de agregar un edificio ya existente.
        """

        if nombre_edificio in self.nombres_edificios():
            raise(ElementoDuplicadoException("Ya existe un edificio con ese nombre"))

        aux_dict = {self.edificios.columns[0]:nombre_edificio}
        for col in self.edificios.columns[1:-1]:
            aux_dict[col] = "9:00-23:00"
        aux_dict[self.edificios.columns[-1]] = "CERRADO"
        aux_row = pd.DataFrame([aux_dict])
        self.edificios = pd.concat([self.edificios, aux_row], ignore_index=True)


    def eliminar_edificio(self, nombre_edificio:str): #TODO Prohibir si hay aulas que usan el edificio
        """
        Metodo para eliminar un edificio existente de la universidad

        Parameters
        ----------
        nombre_edificio : str
            El nombre del edificio a eliminar. Funciona como clave primaria.
        Returns
            None
        Throws:
            EdificioTieneAulasException , si se trata de agregar un edificio ya existente.
        """
        ### TODO DOCUMENTAR
        ### TODO prohibir si hay aulas instanciadas que usen ese edificio
        self.edificios = self.edificios[self.edificios.iloc[:, 0] != nombre_edificio].reset_index(drop=True)

    
    
    def modificar_edificio(self, nombre_edificio:str, columna_a_modificar:str, valor_nuevo:str):
        """
        Modifica el valor de una columna específica para el edificio dado.

        Parameters
        ----------
        nombre_edificio : str
            Nombre del edificio a modificar (clave primaria, debe estar en la primera columna).
        columna_a_modificar : str
            Nombre de la columna a modificar.
        valor_nuevo : str
            Valor nuevo a establecer en la celda correspondiente.
        
        Returns
        -------
        None

        """

        # Buscar la fila donde la primera columna (nombre de edificio) coincide
        filtro = self.edificios[self.edificios.iloc[:, 0] == nombre_edificio]
        # Obtener el índice de esa fila
        index = filtro.index[0]
        # Modificar el valor
        self.edificios.at[index, columna_a_modificar] = valor_nuevo

    
    def modificar_horario_edificio(self, nombre_edificio:str, dia:str, 
        hora1:int, hora2:int, minuto1:int, minuto2:int):

        if time(hora1, minuto1) < time(hora2, minuto2):
            self.modificar_edificio(nombre_edificio, dia, f"{hora1}:{minuto1:02}-{hora2}:{minuto2:02}")
        else:
            raise(HorarioInvalidoException("La hora de cierre no puede ser menor que la de apertura"))


    



    # Sector de aulas
    def columnas_aulas(self): # Retorna lista de columnnames
        return self.aulas.columns.tolist()
    def mostrar_aulas(self): # Retorna el dataframe de aulas
        return self.aulas
    def agregar_aula(self, row): #TODO implementar. Que no permita aulas huerfanas.
        print("A IMPLEMENTAR")
    def eliminar_aula(self, id_aula): #TODO implementar
        print("A IMPLEMENTAR")
    def modificar_aula(self, row_aula): #TODO implementar
        print("A IMPLEMENTAR")
    """Metodo para recuperar el horario de un aula.
    Si el valor es null en el aula, devuelve el del edificio.
    Si el edificio esta cerrado en ese horario, #TODO decidir que hacer"""
    def horario_aula_entrada(self, id_aula): #TODO
        print("A IMPLEMENTAR")
    def horario_aula_salida(self, id_aula): #TODO
        print("A IMPLEMENTAR")


def main():
    uni = Universidad()

    print("Edificios antes del eliminar:")
    print(uni.mostrar_edificios())

    
    uni.modificar_edificio("Anasagasti 1", "Sábado", "CERRADO")
    uni.modificar_edificio("Anasagasti 1", "Nombre del Edificio", "Viedma 1")
    uni.modificar_horario_edificio("Mitre 1", "Domingo", 10, 11, 00, 00)

    try:
        uni.modificar_horario_edificio("Mitre1", "Lunes", 11, 5, 00, 00)
    except HorarioInvalidoException as e:
        print(e)


    print("Edificios despues del eliminar:")
    print(uni.mostrar_edificios())



if __name__ == '__main__':
    main()






