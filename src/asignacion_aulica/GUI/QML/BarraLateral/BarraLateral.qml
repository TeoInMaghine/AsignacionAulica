import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic
import QML.ComponentesUI as ComponentesUI
import ModelosAsignaciónÁulica

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
        BotónPestaña {
            nombre: "Guardar"
            onClicked: {
                var error_result = ProxyGestorDeDatos.guardar();
                if (error_result !== "") {
                    popupErrorGuardar.texto = error_result;
                    popupErrorGuardar.open();
                }
            }
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

    // Popup de error al cargar
    ComponentesUI.PopupConTexto {
        id: popupErrorCargar
        // Esta propiedad se setea desde pyqt
        texto: mensaje_de_error_al_cargar
        textoBotón: "Cerrar"
        Component.onCompleted: {
            if (mensaje_de_error_al_cargar !== "") popupErrorCargar.open()
        }
    }
    // Popup de error al guardar
    ComponentesUI.PopupConTexto {
        id: popupErrorGuardar
        texto: ""
        textoBotón: "Cerrar"
    }
}

