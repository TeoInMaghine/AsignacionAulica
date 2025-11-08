import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RoundButton {
    Layout.preferredWidth: 35
    Layout.preferredHeight: 35

    padding: 0
    bottomPadding: 3

    text: "+"
    font.pointSize: 20
    font.bold: true

    highlighted: hovered
}
