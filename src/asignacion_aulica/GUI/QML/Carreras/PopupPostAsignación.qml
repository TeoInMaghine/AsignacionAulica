import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

Popup {
    id: popup

    required property var info

    modal: true

    topPadding: 40
    bottomPadding: 40
    leftPadding: 100
    rightPadding: 100

    ColumnLayout {
        spacing: 20

        Label {
            text: popup.info
            font.pointSize: FontSize.base
        }

        BotónRedondeadoConTexto{
            text: 'Cerrar'
            onClicked: popup.close()
        }
    }
}
