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
        active: selector.índiceDeLaCarreraActual >= 0
        sourceComponent: Materias {
            indexCarrera: selector.índiceDeLaCarreraActual
        }
    }
}
