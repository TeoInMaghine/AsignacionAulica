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

        // Necesario para que se vean los valores correctos del aula asignada
        Component.onCompleted: {
            selectorEdificio.model.actualizar()
            ProxyGestorDeDatos.ordenarAulas(currentValue)
        }

        textoCuandoNoSeleccionado: "Sin edificio"
        currentIndex: clase.index_edificio_asignado
        onActivated: index => {
            if (index > 0) {
                // Obtener el índice real del edificio que se seleccionó, y ordenar
                // las aulas de ese edificio *antes* de actualizar lo demás
                let actualIndex = selectorEdificio.model.__getitem__(index)
                ProxyGestorDeDatos.ordenarAulas(actualIndex)
            }

            clase.index_edificio_asignado = index
        }
    }

    SelectorDeAula {
        id: selectorAula
        Layout.preferredWidth: Constantes.width_editor_aula

        textoCuandoNoSeleccionado: "Sin aula"
        enabled: selectorEdificio.hayEdificioSeleccionado // No se puede elegir aula sin elegir edificio
        indexEdificio: selectorEdificio.currentValue
        currentIndex: clase.index_aula_asignada
        onActivated: index => {
            clase.index_aula_asignada = index
        }
    }
}
