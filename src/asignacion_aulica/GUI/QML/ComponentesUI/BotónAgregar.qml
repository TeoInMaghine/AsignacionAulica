import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

RoundButton {
    id: botónAgregar

    Layout.preferredHeight: 40
    Layout.preferredWidth: 40

    contentItem: MultiEffect {
        source: imagenAgregar
        anchors.fill: imagenAgregar
        brightness: botónAgregar.highlighted ? 1.0 : 0.2
    }

    Image {
        id: imagenAgregar
        visible: false // Para renderizar solo el MultiEffect

        width: 0.45 * botónAgregar.width
        anchors.centerIn: parent
        fillMode: Image.PreserveAspectFit
        sourceSize.width: width
        source: assets_path + "/iconos/+.svg"
    }

    highlighted: hovered
}
