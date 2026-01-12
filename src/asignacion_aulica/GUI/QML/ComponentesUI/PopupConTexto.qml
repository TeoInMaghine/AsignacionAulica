import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica

/**
 * Un popup con un mensaje y con un botón.
 */
Popup {
    id: popup

    required property string texto
    required property string textoBotón
    signal botónClicked

    modal: true

    topPadding: 20
    bottomPadding: 20
    leftPadding: 60
    rightPadding: 60
    margins: 1

    anchors.centerIn: Overlay.overlay

    ColumnLayout {
        spacing: 20

        Label {
            text: texto
            font.pointSize: FontSize.base
        }

        BotónRedondeadoConTexto{
            id: botón
            text: textoBotón
            onClicked: {
                popup.botónClicked()
                popup.close()
            }
        }
    }
}
