import QtQuick
import QtQuick.Controls
import QtQuick.Effects

Switch {
    id: colapsador

    indicator: MultiEffect {
        id: efecto
        source: imagenColapsador
        anchors.fill: imagenColapsador
        colorization: 1.0
        brightness: hovered ? -0.2 : 0.0

        state: colapsador.checked ? "expandido" : "colapsado"
        states: [
            State {
                name: "colapsado"
                PropertyChanges {
                    target: efecto
                    rotation: -90
                    colorizationColor: "#dbdbdb"
                }
            },
            State {
                name: "expandido"
                PropertyChanges {
                    target: efecto
                    rotation: 0
                    colorizationColor: "#6b6b6b"
                }
            }
        ]

        transitions: Transition {
            RotationAnimation {
                duration: 200
                easing.type: Easing.OutSine
            }
        }
    }

    Image {
        id: imagenColapsador
        visible: false // Para renderizar solo el MultiEffect

        width: 32
        anchors.centerIn: parent
        fillMode: Image.PreserveAspectFit
        sourceSize.width: width
        source: Constantes.logo_colapsador_path
    }
}
