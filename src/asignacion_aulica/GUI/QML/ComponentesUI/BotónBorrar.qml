import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RoundButton {
    Layout.preferredHeight: 40
    Layout.preferredWidth: 40
    radius: 5

    contentItem: Image {
        Layout.alignment: Qt.AlignCenter
        fillMode: Image.PreserveAspectFit
        source: assets_path + "/iconos/Borrar.svg"
    }

    highlighted: hovered
}
