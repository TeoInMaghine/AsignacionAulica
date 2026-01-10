import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica

ComboBox {
    id: comboBox

    required property var indexEdificio // int or undefined

    // El índice 0 indica que no hay aula seleccionada.
    property bool hayAulaSeleccionada: currentIndex > 0

    property alias textoCuandoNoSeleccionado: aulas.textoCuandoNoSeleccionado

    model: ListSelectorDeAula {
        id: aulas
        indexEdificio: comboBox.indexEdificio
        textoCuandoNoSeleccionado: "Ninguna"
    }
    textRole: "nombre"
    valueRole: "índice"

    onPressedChanged: if (pressed && !popup.visible) aulas.ordenar()

    // Toggle items with the space key
    Keys.onSpacePressed: (event) => {
        if (comboBox.popup.visible) {
            var currentItem = comboBox.popup.contentItem.currentItem
            if (currentItem) {
                currentItem.toggle()
                event.accepted = true
            }
        }
    }
    Keys.onReleased: (event) => {
        if (comboBox.popup.visible)
            event.accepted = (event.key === Qt.Key_Space)
    }
}
