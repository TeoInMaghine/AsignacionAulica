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

    Materias { }
}
