import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

ColumnLayout {
    anchors.fill: parent
    anchors.margins: 15
    spacing: 20
    
    Botonera { }
    SelectorDeCarrera { id: selector }
    EditorDeUnaCarrera { índiceDeLaCarreraActual: selector.índiceDeLaCarreraActual }
}
