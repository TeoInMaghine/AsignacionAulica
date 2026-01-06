import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

RowLayout {
    required property int indexCarrera
    required property int indexMateria
    required property int indexClase
    
    SelectorDeEdificioConAulas{
        id: selectorEdificio
        Layout.preferredWidth: Constantes.width_editor_edificio

        textoCuandoNoSeleccionado: "Sin edificio"

        onActivated: index => {
            if (index == 0) { // Se borró la selección
                // Borrar también la selección de aula
                selectorAula.currentIndex = 0
                selectorAula.activated(0)
            }
            else { // Se seleccionó un edificio
                // Seleccionar la primer aula del edificio
                selectorAula.currentIndex = 1
                selectorAula.activated(1)
            }
        }
    }

    SelectorDeAula{
        id: selectorAula
        Layout.preferredWidth: Constantes.width_editor_aula

        textoCuandoNoSeleccionado: "Sin aula"

        enabled: selectorEdificio.hayEdificioSeleccionado // No se puede elegir aula sin elegir edificio
        indexEdificio: selectorEdificio.currentValue

        onActivated: index => {
            if (index == 0){ // Se borró la selección
                // Borrar selección de edificio
                selectorEdificio.currentIndex = 0

                ProxyGestorDeDatos.borrarAulaDeUnaClase(
                    indexCarrera, indexMateria, indexClase
                )
            }
            else {
                ProxyGestorDeDatos.asignarAulaDeUnaClase(
                    indexCarrera, indexMateria, indexClase,
                    selectorEdificio.currentValue, selectorAula.currentValue
                )
            }
        }
    }
}
