import QtQuick
import QtQuick.Controls

RoundButton {
    id: reestablecer

    background: Rectangle {
        anchors.fill: reestablecer
        color: reestablecer.enabled && reestablecer.hovered ?
               reestablecer.palette.dark : reestablecer.palette.light
        border.width: reestablecer.activeFocus ? 2 : 1
        border.color: reestablecer.activeFocus ?
                      reestablecer.palette.highlight :
                      reestablecer.palette.mid
        radius: 4
    }

    icon.source: Constantes.ícono_reestablecer_path
}
