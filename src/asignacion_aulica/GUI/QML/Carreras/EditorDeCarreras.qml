import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

ColumnLayout {
    anchors.fill: parent
    anchors.margins: 15
    spacing: 10
    
    Botonera { }
    SelectorDeCarrera { id: selector }
    Label { text: "Carrera seleccionada: " + selector.índiceDeLaCarreraActual }

    Loader {
        active: selector.índiceDeLaCarreraActual >= 0
        sourceComponent: Materias {
            indexCarrera: selector.índiceDeLaCarreraActual
        }
    }
}
