import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RoundButton {
    bottomPadding: 0
    topPadding: 0
    leftPadding: radius/2
    rightPadding: radius/2

    font.pointSize: FontSize.base
    font.bold: true

    highlighted: hovered
}
