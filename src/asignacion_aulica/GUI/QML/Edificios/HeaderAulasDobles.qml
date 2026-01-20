import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    Button {
        id: headerAulaGrande
        Layout.preferredWidth: Constantes.width_editor_aula

        contentItem: MultiEffect {
            source: label_con_ícono
            anchors.fill: label_con_ícono
            brightness: headerAulaGrande.highlighted ? 1.0 : 0.1
        }

        RowLayout {
            id: label_con_ícono
            visible: false // Para renderizar solo el MultiEffect
            anchors.centerIn: parent
            spacing: 6

            Label {
                leftPadding: 5
                text: "Aula grande"
            }
            Image {
                width: 17
                fillMode: Image.PreserveAspectFit
                sourceSize.width: width
                source: assets_path + "/iconos/ordenar.png"
            }
        }

        highlighted: hovered
        onClicked: {
            aulasDobles.ordenar()
        }
    }

    Item { width: 10 } // Espacio vacío, separar aula grande de las chicas

    RowLayout {
        Layout.preferredWidth:
            2*Constantes.width_editor_aula + visualHeader.spacing

        Label {
            Layout.preferredWidth: 2*Constantes.width_editor_aula
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

            horizontalAlignment: Text.AlignHCenter
            text: "Aulas chicas"
        }
    }
}
