import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

RowLayout {
    required property var clase
    
    SelectorDeEdificioConAulas {
        id: selectorEdificio
        Layout.preferredWidth: Constantes.width_editor_edificio

        Component.onCompleted: selectorEdificio.model.actualizar()

        textoCuandoNoSeleccionado: "Sin edificio"
        currentIndex: clase.index_edificio_asignado
        onActivated: index => {
            clase.index_edificio_asignado = index
            console.log("edificio " + clase.index_edificio_asignado + " aula " + clase.index_aula_asignada)
        }
    }

    SelectorDeAula{
        id: selectorAula
        Layout.preferredWidth: Constantes.width_editor_aula

        Component.onCompleted: selectorAula.model.actualizar()

        textoCuandoNoSeleccionado: "Sin aula"
        enabled: selectorEdificio.hayEdificioSeleccionado // No se puede elegir aula sin elegir edificio
        indexEdificio: selectorEdificio.currentValue
        currentIndex: clase.index_aula_asignada
        onActivated: index => {
            clase.index_aula_asignada = index
            console.log("edificio " + clase.index_edificio_asignado + " aula " + clase.index_aula_asignada)
        }
    }
}
