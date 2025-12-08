import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

ColumnLayout {
    anchors.fill: parent
    anchors.margins: 15
    spacing: 20
    
    Botonera { }
    SelectorYEditorDeCarrera {
        id: selector
    }

    Loader {
        active: selector.hayCarreraSeleccionada
        Layout.preferredWidth: width
        Layout.preferredHeight: height
        sourceComponent: Materias {
            indexCarrera: selector.indexCarrera
        }
    }
}
