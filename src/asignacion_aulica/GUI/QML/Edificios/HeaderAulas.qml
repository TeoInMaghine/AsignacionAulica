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

    RowLayout {
        id: headerNombre
        spacing: 2
        Label {
            Layout.alignment: Qt.AlignCenter
            leftPadding: 5
            text: "Aula"
        }
        Button {
            id: botónOrdenar

            Layout.preferredWidth: 20
            Layout.preferredHeight: 30

            contentItem: MultiEffect {
                source: imagenOrdenar
                anchors.fill: imagenOrdenar
                brightness: botónOrdenar.highlighted ? 1.0 : 0.1
            }

            Image {
                id: imagenOrdenar
                visible: false // Para renderizar solo el MultiEffect

                width: 12
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
                sourceSize.width: width
                source: assets_path + "/iconos/Ordenar.svg"
            }

            highlighted: hovered
            onClicked: {
                aulas.ordenar()
            }
        }
    }
    Label {
        id: headerCapacidad
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Capacidad"
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

    HeaderHorariosSemanales { }

    Item { } // Espacio vacío de 2 * spacing de ancho

    Label {
        id: headerEquipamiento
        leftPadding: 50
        rightPadding: 50
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Equipamiento"
    }
}
