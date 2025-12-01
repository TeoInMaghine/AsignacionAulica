import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QML.ComponentesUI as ComponentesUI

Rectangle {
    Layout.preferredWidth: Constantes.ancho_de_la_barra
    Layout.fillHeight: true
    color: ComponentesUI.Constantes.rojo_unrn

    property string pestaña_actual: "Aulas"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Título
        Text{
            text: Constantes.título_texto
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            Layout.fillWidth: true
            Layout.topMargin: 15
            font.pointSize: ComponentesUI.FontSize.huge
            font.bold: true
            lineHeight: 1.1
            color: "white"
        }

        MenuSeparator {
            Layout.fillWidth: true
            leftPadding: 7
            rightPadding: 7
            topPadding: 0
            bottomPadding: 0
        }

        // Botones de las pestañas
        BotónPestaña {
            nombre: "Aulas"
            onClicked: () => pestaña_actual = nombre
        }
        BotónPestaña {
            nombre: "Materias"
            onClicked: () => pestaña_actual = nombre
        }

        // Spacer to push tabs to the top
        Item {
            Layout.fillHeight: true
        }

        Image {
            id: logoUNRN
            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
            Layout.margins: Constantes.logo_unrn_margen
            Layout.fillWidth: true
            fillMode: Image.PreserveAspectFit
            source: Constantes.logo_unrn_path
        }
    }
}

