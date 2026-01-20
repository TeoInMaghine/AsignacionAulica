import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

Popup {
    id: popup
    closePolicy: Popup.NoAutoClose
    modal: true

    topPadding: 40
    bottomPadding: 40
    leftPadding: 100
    rightPadding: 100
    margins: 1
    anchors.centerIn: Overlay.overlay

    ColumnLayout {
        spacing: 20

        Label {
            text: "Asignando Aulas..."
            font.pointSize: FontSize.big
        }

        AnimatedImage {
            source: assets_path + "/thinking.gif"
            fillMode: Image.PreserveAspectFit
        }

    }

    // TODO: Cancel button maybe?
}
