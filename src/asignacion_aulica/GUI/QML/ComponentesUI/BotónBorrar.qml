import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

RoundButton {
    id: botónBorrar

    Layout.preferredHeight: 40
    Layout.preferredWidth: 40
    radius: 5

    contentItem: MultiEffect {
        source: imagenBorrar
        anchors.fill: imagenBorrar
        brightness: botónBorrar.highlighted ? 1.0 : 0.2
    }

    Image {
        id: imagenBorrar
        visible: false // Para renderizar solo el MultiEffect

        width: 26
        anchors.centerIn: parent
        fillMode: Image.PreserveAspectFit
        sourceSize.width: width
        source: assets_path + "/iconos/Borrar.svg"
    }

    highlighted: enabled ? hovered : false
}
