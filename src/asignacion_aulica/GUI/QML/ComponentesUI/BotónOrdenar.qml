import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Button {
    id: botónOrdenar

    property alias labelText: label.text

    contentItem: MultiEffect {
        source: label_con_ícono
        anchors.fill: label_con_ícono
        brightness: botónOrdenar.highlighted ? 1.0 : 0.1
    }

    RowLayout {
        id: label_con_ícono
        visible: false // Para renderizar solo el MultiEffect
        anchors.centerIn: parent
        spacing: 6

        Label {
            id: label
            leftPadding: 5
        }
        Image {
            width: 17
            fillMode: Image.PreserveAspectFit
            sourceSize.width: width
            source: assets_path + "/iconos/ordenar.png"
        }
    }

    highlighted: hovered
}
