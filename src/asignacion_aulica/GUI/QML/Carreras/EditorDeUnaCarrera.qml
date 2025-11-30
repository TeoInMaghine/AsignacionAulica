import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

ColumnLayout {
    required property int índiceDeLaCarreraActual
    property bool hayCarreraSeleccionada: índiceDeLaCarreraActual >= 0
    
    spacing: 15

    RowLayout{
        spacing: 15
        BotónRedondeadoConTexto {
            text: "Cambiar Nombre"
            enabled: hayCarreraSeleccionada
        }
        BotónRedondeadoConTexto {
            text: "Borrar Carrera"
            enabled: hayCarreraSeleccionada
        }
    }

    //SelectorDeEdificioPreferido{ }
}
