# -*- coding: utf-8 -*-
"""
Definiciones de las clases de objetos necesarios.

@author: Cristian
"""

from enum import Enum, auto
from datetime import datetime, time, timedelta
from typing import Optional, List


class Modalidad(Enum):
    PRESENCIAL = auto()
    VIRTUAL = auto()
    INDEFINIDO = auto()


class Día(Enum):
    LUNES = auto()
    MARTES = auto()
    MIÉRCOLES = auto()
    JUEVES = auto()
    VIERNES = auto()
    SÁBADO = auto()
    DOMINGO = auto()
    INDEFINIDO = auto()


class Horario:
    def validar_horario(hora_inicio: datetime.time, hora_fin: datetime.time):
        if (type(hora_inicio) != datetime.time):
            raise TypeError("Tipo de hora_comienzo debe ser datetime.time")
        
        if (type(hora_fin) != datetime.time):
            raise TypeError("Tipo de hora_fin debe ser datetime.time")
        
        if (hora_inicio == hora_fin):
            raise ValueError("Valores de hora_inicio y hora_fin deben ser distintos")
            
        if (hora_inicio > hora_fin):
            raise ValueError("Valor de hora_inicio debe ser anterior a hora_fin")
        pass
    
    def __init__(
            self,
            dia: Día, # Día de la semana (lunes, martes, ...)
            hora_inicio: datetime.time, # Hora de inicio, por ejemplo: 18 (hs)
            hora_fin: datetime.time, # Hora de fin o cierre, por ejemplo: 19 (hs)
            modalidad: Optional[Modalidad] = Modalidad.INDEFINIDO # Modalidad virtual, presencial, o indefinido
            ):
        self.dia: Día = dia
        self.hora_inicio: datetime.time = hora_inicio
        self.hora_fin: datetime.time = hora_fin
        self.modalidad: Modalidad = modalidad
        
        self.validar_horario(hora_inicio, hora_fin)


class Objeto:
    def __init__(
            self,
            nombre: str, # Nombre del objeto (por ejemplo, Pizarrón)
            cantidad: Optional[int] = None # Cantidad de objetos
            ):
        self.nombre: str = nombre
        self.cantidad: int = cantidad


class Equipamiento:
    def __init__(
            self,
            objetos: List[Objeto] = None
            ):
        self.objetos: List[Objeto] = objetos


class Aula:
    def __init__(
            self,
            identificador: str, # Identificador del aula (por ejemplo: 102B)
            capacidad: int = None, # Capacidad máxima
            equipamiento: Equipamiento = None, # Equipamiento disponible (lista)
            horario: Optional[Horario] = None # Rango horario de disponibilidad (opcional, por defecto se usa el horario del edificio)
            ):
        self.identificador: str = identificador
        self.capacidad: int = capacidad
        self.equipamiento: Equipamiento = equipamiento
        self.horario: Horario = horario


class Edificio:
    def __init__(
            self,
            nombre: str, # Nombre del edificio
            horarios: List[Horario] = None, # Horarios del edificio
            aulas: List[Aula] = None # Aulas disponibles en el edificio
            ):
        self.nombre: str = nombre
        self.horarios: List[Horario] = horarios
        self.aulas: List[Aula] = aulas
        
        self.verificar()

    def verificar(self):
        if (self.aulas != None):
            if (type(self.aulas) != list):
                raise TypeError("Tipo de aulas distinto de lista")
        else:
            i = 0
            for elemento in self.aulas:
                if (type(elemento) != Aula):
                    raise TypeError(f"Tipo de aulas[{i}] distinto de Aula")
                i += 1
                
        if (self.horarios != None):
            if (type(self.horarios) != list):
                raise TypeError("Tipo de aulas distinto de lista")
        else:
            i = 0
            for elemento in self.horarios:
                if (type(elemento) != Horario):
                    raise TypeError(f"Tipo de horarios[{i}] distinto de Horario")
                i += 1
    
    def agregar_aula(self, nueva: Aula):
        if (type(nueva) != Aula):
            raise TypeError("Tipo de nueva distinto de Aula")
        
        if (self.aulas == None):
            self.aulas = [nueva]


class Carrera:
    def __init__(
            self,
            nombre: str, # Nombre de la carrera
            preferencia: Optional[Edificio] = None # Preferencia de edificio (opcional)
            ):
        self.nombre: str = nombre
        self.preferencia: Edificio = preferencia


class Actividad: # Actividad o materia dictada en la Universidad
    def __init__(
            self,
            identificador: str, # Identificador de la materia (por ejemplo: B6024)
            nombre: str, # Nombre de la materia (por ejemplo: Programación 1)
            comision: Optional[str] = None, # Comisión
            horarios: Optional[List[Horario]] = None, # Horario de cada clase (día de la semana, horario de inicio y horario de fin) en conjunto con la modalidad (presencial, virtual)
            carrera: Optional[Carrera] = None, # Carrera
            anio: Optional[int] = None, # Año en el plan de estudios
            cant_alumnos: Optional[int] = 0, # Cantidad de alumnos
            equipamiento: Optional[Equipamiento] = None # Equipamiento necesario para cada clase (en forma de lista, opcional)
            ):
        self.identificador: str = identificador
        self.nombre: str = nombre
        self.comision: str = comision
        self.carrera: Carrera = carrera
        self.anio: int = anio
        self.horarios: List[Horario] = horarios
        self.cant_alumnos: int = cant_alumnos
        self.equipamiento: Equipamiento = equipamiento


class Universidad:
    def __init__(
            self,
            edificios: Optional[List[Edificio]] = None, # Edificios con los que cuenta la Universidad
            carreras: Optional[List[Carrera]] = None, # Carreras de la Universidad
            actividades: Optional[List[Actividad]] = None # Actividades o materias para cursar en la Universidad
            ):
        self.edificios: List[Edificio] = edificios
        self.carreras: List[Carrera] = carreras
        self.actividades: List[Actividad] = actividades
    
    def crear_edificio(self, nombre_edificio: str):
        if (self.edificios == None):
            nuevo_edificio: Edificio = Edificio()
            self.edificios = [nuevo_edificio]
