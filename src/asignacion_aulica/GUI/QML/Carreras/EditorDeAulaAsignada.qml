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

        onActivated: index => {
            // Des-seleccionar el aula cuando cambia el edificio
            selectorAula.currentIndex = 0
        }
    }

    SelectorDeAula{
        id: selectorAula
        enabled: selectorEdificio.hayEdificioSeleccionado // No se puede elegir aula sin elegir edificio
        indexEdificio: selectorEdificio.currentValue
        Layout.preferredWidth: Constantes.width_editor_aula

        onActivated: index => {
            if (index == 0){ // Se seleccionó "Ninguna"
                // Borrar selección de edificio
                selectorEdificio.currentIndex = 0
            }
        }
    }
}
