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

    Materias {
        enabled: selector.hayCarreraSeleccionada
        indexCarrera: selector.indexCarrera
    }
}
