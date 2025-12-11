import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

Popup {
    id: popup

    required property string díasSinAsignar

    modal: true

    topPadding: 40
    bottomPadding: 40
    leftPadding: 100
    rightPadding: 100

    ColumnLayout {
        spacing: 20

        Label {
            text: popup.díasSinAsignar.length > 0
                ? "No se pudieron asignar aulas a las clases de los días " + popup.díasSinAsignar
                : "Se asignaron aulas a todas las clases."
            font.pointSize: FontSize.base
        }

        BotónRedondeadoConTexto{
            text: 'Cerrar'
            onClicked: popup.close()
        }
    }
}
