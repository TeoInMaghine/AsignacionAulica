import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

ColumnLayout {
    required property int índiceDeLaCarreraActual
    property bool hayCarreraSeleccionada: índiceDeLaCarreraActual >= 0
    
    spacing: 15

    SelectorEdificio{}
    //SelectorDeEdificioPreferido{ índiceDeLaCarreraActual: índiceDeLaCarreraActual }
}
