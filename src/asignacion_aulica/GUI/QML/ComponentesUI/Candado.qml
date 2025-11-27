import QtQuick
import QtQuick.Controls
import QtQuick.Effects

Switch {
    id: candado

    indicator: MultiEffect {
        id: efecto
        source: candado.checked ? imagenCandadoCerrado : imagenCandadoAbierto
        anchors.fill: imagenCandadoCerrado
        brightness: hovered ? 1.0 :
            candado.checked ? 0.0 :
                              0.2
    }

    background: Rectangle {
        anchors.fill: parent
        color:      hovered ? candado.palette.dark :
            candado.checked ? candado.palette.mid  :
                              candado.palette.light
        radius: 4
    }

    Image {
        id: imagenCandadoCerrado
        visible: false // Para renderizar solo el MultiEffect

        width: 16
        anchors.centerIn: parent
        fillMode: Image.PreserveAspectFit
        sourceSize.width: width
        source: Constantes.ícono_candado_cerrado_path
    }
    Image {
        id: imagenCandadoAbierto
        visible: false // Para renderizar solo el MultiEffect

        anchors.fill: imagenCandadoCerrado
        fillMode: Image.PreserveAspectFit
        sourceSize.width: width
        source: Constantes.ícono_candado_abierto_path
    }
}
