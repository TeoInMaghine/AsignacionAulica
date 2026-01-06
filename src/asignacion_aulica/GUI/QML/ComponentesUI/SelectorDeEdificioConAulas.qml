import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica

ComboBox {
    id: comboBox

    // El índice 0 indica que no hay edificio seleccionado.
    property bool hayEdificioSeleccionado: currentIndex > 0

    model: ListSelectorDeEdificiosConAulas {
        id: edificios
        textoCuandoNoSeleccionado: "Ninguno"
    }
    textRole: "nombre"
    valueRole: "índice"

    onPressedChanged: if (pressed && !popup.visible) edificios.actualizar()

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
