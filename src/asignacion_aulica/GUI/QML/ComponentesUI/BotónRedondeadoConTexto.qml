import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RoundButton {
    Layout.preferredWidth: 35
    Layout.preferredHeight: 35

    //padding: 10
    bottomPadding: 0
    topPadding: 0
    leftPadding: 13
    rightPadding: 13

    font.pointSize: 13
    font.bold: true

    highlighted: hovered
}
