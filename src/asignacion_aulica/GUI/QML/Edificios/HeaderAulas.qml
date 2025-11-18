import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    property alias widthNombre: headerNombre.width
    property alias widthCapacidad: headerCapacidad.width
    property alias widthEquipamiento: headerEquipamiento.width

    Button {
        id: headerNombre
        Layout.preferredWidth: 120 // Para que entre el texto "Sin nombre 1"

        contentItem: MultiEffect {
            source: label_con_ícono
            anchors.fill: label_con_ícono
            brightness: headerNombre.highlighted ? 1.0 : 0.1
        }

        RowLayout {
            id: label_con_ícono
            visible: false // Para renderizar solo el MultiEffect
            anchors.centerIn: parent
            spacing: 2

            Label {
                Layout.alignment: Qt.AlignCenter
                leftPadding: 5
                text: "Aula"
            }
            Image {
                width: 12
                fillMode: Image.PreserveAspectFit
                sourceSize.width: width
                source: assets_path + "/iconos/Ordenar.svg"
            }
        }

        highlighted: hovered
        onClicked: {
            aulas.ordenar()
        }
    }
    Label {
        id: headerCapacidad
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Capacidad"
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

    Label {
        id: headerEquipamiento
        leftPadding: 40
        rightPadding: 40
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Equipamiento"
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

    HeaderHorariosSemanales { }
}
