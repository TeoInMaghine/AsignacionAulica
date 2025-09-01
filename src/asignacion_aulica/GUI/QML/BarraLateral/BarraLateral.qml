import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic

Rectangle {
    Layout.preferredWidth: Constantes.ancho_de_la_barra
    Layout.fillHeight: true
    color: Constantes.rojo_unrn

    property string pestaña_actual: "Edificios"

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
            font.pointSize: Constantes.título_tamaño
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
        BotónPestaña{ nombre: "Edificios" }
        BotónPestaña{ nombre: "Aulas"     }
        BotónPestaña{ nombre: "Carreras"  }
        BotónPestaña{ nombre: "Materias"  }
        BotónPestaña{ nombre: "Horarios"  }

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

